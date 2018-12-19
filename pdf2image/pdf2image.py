"""
    pdf2image is a light wrapper for the poppler-utils tools that can convert your
    PDFs into Pillow images.
"""

import os
import re
import tempfile
import uuid

from io import BytesIO
from subprocess import Popen, PIPE
from PIL import Image

from .exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False):
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
    """

    page_count = __page_count(pdf_path, userpw)

    if thread_count < 1:
        thread_count = 1

    if first_page is None:
        first_page = 1

    if last_page is None or last_page > page_count:
        last_page = page_count

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
        args, parse_buffer_func = __build_command(['pdftoppm', '-r', str(dpi), pdf_path], output_folder, current_page, current_page + thread_page_count - 1, fmt, uid, userpw, use_cropbox)
        # Update page values
        current_page = current_page + thread_page_count
        reminder -= int(reminder > 0)
        # Spawn the process and save its uuid
        processes.append((uid, Popen(args, stdout=PIPE, stderr=PIPE)))

    images = []

    for uid, proc in processes:
        data, err = proc.communicate()

        if b"Syntax Error" in err and strict:
            raise PDFSyntaxError(err.decode("utf8", "ignore"))

        if output_folder is not None:
            images += __load_from_output_folder(output_folder, uid)
        else:
            images += parse_buffer_func(data)

    return images

def convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False):
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
    """

    with tempfile.NamedTemporaryFile('wb') as f:
        f.write(pdf_file)
        f.flush()
        return convert_from_path(f.name, dpi=dpi, output_folder=output_folder, first_page=first_page, last_page=last_page, fmt=fmt, thread_count=thread_count, userpw=userpw, use_cropbox=use_cropbox, strict=strict)

def __build_command(args, output_folder, first_page, last_page, fmt, uid, userpw, use_cropbox):
    if use_cropbox:
        args.append('-cropbox')

    if first_page is not None:
        args.extend(['-f', str(first_page)])

    if last_page is not None:
        args.extend(['-l', str(last_page)])

    parsed_format, parse_buffer_func = __parse_format(fmt)

    if parsed_format != 'ppm':
        args.append('-' + parsed_format)

    if output_folder is not None:
        args.append(os.path.join(output_folder, uid))

    if userpw is not None:
        args.extend(['-upw', userpw])

    return args, parse_buffer_func

def __parse_format(fmt):
    if fmt[0] == '.':
        fmt = fmt[1:]
    if fmt == 'jpeg' or fmt == 'jpg':
        return 'jpeg', __parse_buffer_to_jpeg
    if fmt == 'png':
        return 'png', __parse_buffer_to_png
    # Unable to parse the format so we'll use the default
    return 'ppm', __parse_buffer_to_ppm

def __parse_buffer_to_ppm(data):
    images = []

    index = 0

    while index < len(data):
        code, size, rgb = tuple(data[index:index + 40].split(b'\n')[0:3])
        size_x, size_y = tuple(size.split(b' '))
        file_size = len(code) + len(size) + len(rgb) + 3 + int(size_x) * int(size_y) * 3
        images.append(Image.open(BytesIO(data[index:index + file_size])))
        index += file_size

    return images

def __parse_buffer_to_jpeg(data):
    return [
        Image.open(BytesIO(image_data + b'\xff\xd9'))
        for image_data in data.split(b'\xff\xd9')[:-1] # Last element is obviously empty
    ]

def __parse_buffer_to_png(data):
    images = []

    index = 0

    while index < len(data):
        file_size = data[index:].index(b'IEND') + 8 # 4 bytes for IEND + 4 bytes for CRC
        images.append(Image.open(BytesIO(data[index:index+file_size])))
        index += file_size

    return images

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

def __load_from_output_folder(output_folder, uid):
    return [Image.open(os.path.join(output_folder, f)) for f in sorted(os.listdir(output_folder)) if uid in f]
