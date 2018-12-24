"""
    pdf2image is a light wrapper for the poppler-utils tools that can convert your
    PDFs into Pillow images.
"""

import os
import re
import uuid

# polyfill for python27
try:
    from tempfile import (
        TemporaryDirectory,
        NamedTemporaryFile
    )
except ImportError:
    import tempfile
    import shutil

    class TemporaryDirectory(object):
        def __init__(self):
            self.name = tempfile.mkdtemp()

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            self.cleanup()

        def cleanup(self):
            shutil.rmtree(self.name)

        def __del__(self):
            self.cleanup()

    class NamedTemporaryFile(object):
        def __init__(self):
            self.name = tempfile.mkstemp()

        def __enter__(self):
            return self.name

        def __exit__(self, exc, value, tb):
            os.remove(self.name)

from subprocess import Popen, PIPE
from io import BytesIO
from PIL import Image

from .exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            first_page -> First page to process
            last_page -> Last page to process before stopping
            fmt -> Output image format
            thread_count -> How many threads we are allowed to spawn for processing
            userpw -> PDF's password
            use_cropbox -> Use cropbox instead of mediabox
            strict -> When a Syntax Error is thrown, it will be raised as an Exception
            transparent -> Output with a transparent background instead of a white one.
    """

    page_count = __page_count(pdf_path, userpw)

    if thread_count < 1:
        thread_count = 1

    if first_page is None:
        first_page = 1

    if last_page is None or last_page > page_count:
        last_page = page_count

    temp_dir = None
    if output_folder is None:
        temp_dir = TemporaryDirectory('wb')
        output_folder = temp_dir.name

    # Recalculate page count based on first and last page
    page_count = last_page - first_page + 1

    if thread_count > page_count:
        thread_count = page_count

    reminder = page_count % thread_count
    current_page = first_page
    processes = []
    for _ in range(thread_count):
        # A unique identifier for our files if the directory is not empty
        uid = str(uuid.uuid4())
        # Get the number of pages the thread will be processing
        thread_page_count = page_count // thread_count + int(reminder > 0)
        # Build the command accordingly
        args = __build_command(['pdftocairo', '-r', str(dpi), pdf_path], output_folder, current_page, current_page + thread_page_count - 1, fmt, uid, userpw, use_cropbox, transparent)
        # Update page values
        current_page = current_page + thread_page_count
        reminder -= int(reminder > 0)
        # Spawn the process and save its uuid
        processes.append((uid, Popen(args, stdout=PIPE, stderr=PIPE)))

    images = []

    for uid, proc in processes:
        _, err = proc.communicate()

        if err is not None and strict:
            raise PDFSyntaxError(err.decode("utf8", "ignore"))

        images += __load_from_output_folder(output_folder, uid, in_memory=(temp_dir is not None))

    if temp_dir is not None:
        del temp_dir

    return images

def convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            first_page -> First page to process
            last_page -> Last page to process before stopping
            fmt -> Output image format
            thread_count -> How many threads we are allowed to spawn for processing
            userpw -> PDF's password
            use_cropbox -> Use cropbox instead of mediabox
            strict -> When a Syntax Error is thrown, it will be raised as an Exception
            transparent -> Output with a transparent background instead of a white one.
    """

    with NamedTemporaryFile('wb') as f:
        f.write(pdf_file)
        f.flush()
        return convert_from_path(f.name, dpi=dpi, output_folder=output_folder, first_page=first_page, last_page=last_page, fmt=fmt, thread_count=thread_count, userpw=userpw, use_cropbox=use_cropbox, strict=strict, transparent=transparent)

def __build_command(args, output_folder, first_page, last_page, fmt, uid, userpw, use_cropbox, transparent):
    if use_cropbox:
        args.append('-cropbox')

    parsed_format = __parse_format(fmt)

    if transparent and parsed_format == 'png':
        args.append('-transp')

    if first_page is not None:
        args.extend(['-f', str(first_page)])

    if last_page is not None:
        args.extend(['-l', str(last_page)])

    if parsed_format != 'ppm':
        args.append('-' + parsed_format)

    if output_folder is not None:
        args.append(os.path.join(output_folder, uid))

    if userpw is not None:
        args.extend(['-upw', userpw])

    return args

def __parse_format(fmt):
    if fmt[0] == '.':
        fmt = fmt[1:]
    if fmt == 'jpeg' or fmt == 'jpg':
        return 'jpeg'
    if fmt == 'png':
        return 'png'
    # Unable to parse the format so we'll use the default
    return 'jpeg'

def __page_count(pdf_path, userpw=None):
    try:
        if userpw is not None:
            proc = Popen(["pdfinfo", pdf_path, '-upw', userpw], stdout=PIPE, stderr=PIPE)
        else:
            proc = Popen(["pdfinfo", pdf_path], stdout=PIPE, stderr=PIPE)

        out, err = proc.communicate()
    except:
        raise PDFInfoNotInstalledError('Unable to get page count. Is poppler installed and in PATH?')

    try:
        # This will throw if we are unable to get page count
        return int(re.search(r'Pages:\s+(\d+)', out.decode("utf8", "ignore")).group(1))
    except:
        raise PDFPageCountError('Unable to get page count. %s' % err.decode("utf8", "ignore"))

def __load_from_output_folder(output_folder, uid, in_memory=False):
    images = []
    for f in sorted(os.listdir(output_folder)):
        if uid in f:
            images.append(Image.open(os.path.join(output_folder, f)))
            if in_memory:
                images[-1].load()
