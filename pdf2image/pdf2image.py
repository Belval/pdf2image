"""
    pdf2image is a light wrapper for the poppler-utils tools that can convert your
    PDFs into Pillow images.
"""

import os
import platform
import re
import uuid
import tempfile
import shutil

from subprocess import Popen, PIPE
from PIL import Image

from .parsers import (
    parse_buffer_to_ppm,
    parse_buffer_to_jpeg,
    parse_buffer_to_png
)

from .exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

TRANSPARENT_FILE_TYPES = ['png', 'tiff']


def convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None,
                      fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False,
                      output_file=str(uuid.uuid4()), poppler_path=None):
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
            output_file -> What is the output filename
            poppler_path -> Path to look for poppler binaries

    """

    page_count = _page_count(pdf_path, userpw, poppler_path=poppler_path)

    # We start by getting the output format, the buffer processing function and if we need pdftocairo
    parsed_fmt, parse_buffer_func, use_pdfcairo_format = _parse_format(fmt)

    # We use pdftocairo is the format requires it OR we need a transparent output
    use_pdfcairo = use_pdfcairo_format or (transparent and parsed_fmt in TRANSPARENT_FILE_TYPES)

    if thread_count < 1:
        thread_count = 1

    if first_page is None:
        first_page = 1

    if last_page is None or last_page > page_count:
        last_page = page_count

    auto_temp_dir = False
    if output_folder is None and use_pdfcairo:
        auto_temp_dir = True
        output_folder = tempfile.mkdtemp()

    # Recalculate page count based on first and last page
    page_count = last_page - first_page + 1

    if thread_count > page_count:
        thread_count = page_count

    reminder = page_count % thread_count
    current_page = first_page
    processes = []
    for i in range(thread_count):
        thread_output_file = output_file + '_' + str(i) if thread_count > 1 else output_file 
        # Get the number of pages the thread will be processing
        thread_page_count = page_count // thread_count + int(reminder > 0)
        # Build the command accordingly
        args = _build_command(['-r', str(dpi), pdf_path], output_folder, current_page, current_page + thread_page_count - 1, parsed_fmt, thread_output_file, userpw, use_cropbox, transparent)

        if use_pdfcairo:
            args = [_get_command_path('pdftocairo', poppler_path)] + args
        else:
            args = [_get_command_path('pdftoppm', poppler_path)] + args

        # Update page values
        current_page = current_page + thread_page_count
        reminder -= int(reminder > 0)
        # Spawn the process and save its uuid
        processes.append((thread_output_file, Popen(args, stdout=PIPE, stderr=PIPE)))

    images = []

    for uid, proc in processes:
        data, err = proc.communicate()

        if b'Syntax Error'in err and strict:
            raise PDFSyntaxError(err.decode("utf8", "ignore"))

        if output_folder is not None:
            images += _load_from_output_folder(output_folder, uid, in_memory=auto_temp_dir)
        else:
            images += parse_buffer_func(data)

    if auto_temp_dir:
        shutil.rmtree(output_folder)

    return images


def convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None,
                       fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False,
                       output_file=str(uuid.uuid4()), poppler_path=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
            poppler_path -> Path to look for poppler binaries
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            first_page -> First page to process
            last_page -> Last page to process before stopping
            fmt -> Output image format
            thread_count -> How many threads we are allowed to spawn for processing
            userpw -> PDF's password
            use_cropbox -> Use cropbox instead of mediabox
            strict -> When a Syntax Error is thrown, it will be raised as an Exception
            transparent -> Output with a transparent background instead of a white one.
            output_file -> What is the output filename
            poppler_path -> Path to look for poppler binaries
    """

    fh, temp_filename = tempfile.mkstemp()
    try:
        with open(temp_filename, 'wb') as f:
            f.write(pdf_file)
            f.flush()
            return convert_from_path(f.name, dpi=dpi, output_folder=output_folder,
                                     first_page=first_page, last_page=last_page, fmt=fmt, thread_count=thread_count,
                                     userpw=userpw, use_cropbox=use_cropbox, strict=strict, transparent=transparent,
                                     output_file=output_file, poppler_path=poppler_path)
    finally:
        os.close(fh)
        os.remove(temp_filename)


def _build_command(args, output_folder, first_page, last_page, fmt, output_file, userpw, use_cropbox, transparent):
    if use_cropbox:
        args.append('-cropbox')

    if transparent and fmt in TRANSPARENT_FILE_TYPES:
        args.append('-transp')

    if first_page is not None:
        args.extend(['-f', str(first_page)])

    if last_page is not None:
        args.extend(['-l', str(last_page)])

    if fmt != 'ppm':
        args.append('-' + fmt)

    if output_folder is not None:
        args.append(os.path.join(output_folder, output_file))

    if userpw is not None:
        args.extend(['-upw', userpw])

    return args


def _parse_format(fmt):
    fmt = fmt.lower()
    if fmt[0] == '.':
        fmt = fmt[1:]
    if fmt in ('jpeg', 'jpg'):
        return 'jpeg', parse_buffer_to_jpeg, False
    if fmt == 'png':
        return 'png', parse_buffer_to_png, False
    if fmt in ('tif', 'tiff'):
        return 'tiff', None, True
    # Unable to parse the format so we'll use the default
    return 'ppm', parse_buffer_to_ppm, False


def _get_command_path(command, poppler_path=None):
    if platform.system() == 'Windows':
        command = command + '.exe'

    if poppler_path is not None:
        command = poppler_path + command

    return command


def _page_count(pdf_path, userpw=None, poppler_path=None):
    try:
        command = [_get_command_path("pdfinfo", poppler_path), pdf_path]

        if userpw is not None:
            command.extend(['-upw', userpw])

        proc = Popen(command, stdout=PIPE, stderr=PIPE)

        out, err = proc.communicate()
    except:
        raise PDFInfoNotInstalledError('Unable to get page count. Is poppler installed and in PATH?')

    try:
        # This will throw if we are unable to get page count
        return int(re.search(r'Pages:\s+(\d+)', out.decode("utf8", "ignore")).group(1))
    except:
        raise PDFPageCountError('Unable to get page count. %s' % err.decode("utf8", "ignore"))


def _load_from_output_folder(output_folder, output_file, in_memory=False):
    images = []
    for f in sorted(os.listdir(output_folder)):
        if output_file in f:
            images.append(Image.open(os.path.join(output_folder, f)))
            if in_memory:
                images[-1].load()
    return images
