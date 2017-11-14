import os
import sys
import tempfile

from subprocess import Popen, PIPE
from PIL import Image
from io import BytesIO

def convert_from_path(pdf_path, dpi=200, output_folder=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
    """

    args = ['pdftoppm', '-r', str(dpi), pdf_path, ]

    if output_folder is not None:
        args.append(output_folder if output_folder[-1] == '/' else output_folder + '/')

    proc = Popen(args, stdout=PIPE, stderr=PIPE)

    data, err = proc.communicate()

    if output_folder is not None:
        return __load_from_output_folder(output_folder)
    else:
        return __parse_pdftoppm_buffer(data)

def convert_from_bytes(pdf_file, dpi=200, output_folder=None):
    """
        Description: Convert PDF to Image will throw whenever one of the condition is reached
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
            output_folder -> Write the resulting images to a folder (instead of directly in memory)
    """


    args = ['pdftoppm', '-r', str(dpi),]

    if output_folder is not None:
        with tempfile.NamedTemporaryFile('wb') as f:
            f.write(pdf_file)
            return convert_from_path(f.name, dpi=dpi, output_folder=output_folder)

    proc = Popen(args, stdout=PIPE, stdin=PIPE, stderr=PIPE)

    proc.stdin.write(pdf_file)

    data, err = proc.communicate()

    if output_folder is not None:
        return __load_from_output_folder(output_folder)
    else:
        return __parse_pdftoppm_buffer(data)

def __parse_pdftoppm_buffer(data):
    images = []

    index = 0

    while(index < len(data)):
        code, size, rgb = tuple(data[index:index + 40].split(b'\n')[0:3])
        size_x, size_y = tuple(size.split(b' '))
        file_size = len(code) + len(size) + len(rgb) + 3 + int(size_x) * int(size_y) * 3
        images.append(Image.open(BytesIO(data[index:index + file_size])))
        index += file_size

    return images

def __load_from_output_folder(output_folder):
    return [Image.open(os.path.join(output_folder, f)) for f in sorted(os.listdir(output_folder))]
