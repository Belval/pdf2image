import os
import sys
import tempfile

from subprocess import Popen, PIPE
from PIL import Image
from io import BytesIO

def convert_from_path(pdf_path, dpi=200, output_folder=None, max_page_count=None, fmt='ppm'):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            max_page_count -> Max number of page to process before stopping
            fmt -> Output image format
    """

    args, parse_buffer_func = __build_command(['pdftoppm', '-r', str(dpi), pdf_path], output_folder, max_page_count, fmt)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)

    data, err = proc.communicate()

    if output_folder is not None:
        return __load_from_output_folder(output_folder)
    else:
        return parse_buffer_func(data)

def convert_from_bytes(pdf_file, dpi=200, output_folder=None, max_page_count=None, fmt='ppm'):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
            max_page_count -> Max number of page to process before stopping
            fmt -> Output image format
    """

    if output_folder is not None:
        with tempfile.NamedTemporaryFile('wb') as f:
            f.write(pdf_file)
            f.flush()
            return convert_from_path(f.name, dpi=dpi, output_folder=output_folder, max_page_count=max_page_count, fmt=fmt)

    args, parse_buffer_func = __build_command(['pdftoppm', '-r', str(dpi)], output_folder, max_page_count, fmt)

    proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    proc.stdin.write(pdf_file)

    data, err = proc.communicate()

    return parse_buffer_func(data)

def __build_command(args, output_folder, max_page_count, fmt):
    if max_page_count is not None:
        args.extend(['-l', str(max_page_count)])

    parsed_format, parse_buffer_func = __parse_format(fmt)

    if parsed_format != 'ppm':
        args.append('-' + parsed_format)

    if output_folder is not None:
        args.append(output_folder if output_folder[-1] == '/' else output_folder + '/')

    return args, parse_buffer_func

def __parse_format(fmt):
    if fmt[0] == '.':
        fmt = fmt[1:]
    if fmt == 'jpeg' or fmt == 'jpg':
        return 'jpeg', __parse_buffer_to_jpeg
    elif fmt == 'png':
        return 'png', __parse_buffer_to_png
    else:
        return 'ppm', __parse_buffer_to_ppm

def __parse_buffer_to_ppm(data):
    images = []

    index = 0

    while(index < len(data)):
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

    while(index < len(data)):
        file_size = data[index:].index(b'IEND') + 8 # 4 bytes for IEND + 4 bytes for CRC
        images.append(Image.open(BytesIO(data[index:index+file_size])))
        index += file_size

    return images

def __load_from_output_folder(output_folder):
    return [Image.open(os.path.join(output_folder, f)) for f in sorted(os.listdir(output_folder))]

