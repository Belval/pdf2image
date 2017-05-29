from subprocess import Popen, PIPE
from PIL import Image
from io import BytesIO

def convert_from_path(pdf_path, save_path=None, dpi=200):
    """
        Description: Convert PDF to Image
        Parameters:
            pdf_path -> Path to the PDF that you want to convert
            dpi -> Image quality in DPI (default 200)
    """

    proc = Popen(['pdftoppm', '-r', str(dpi), pdf_path, ], stdout=PIPE)

    data, err = proc.communicate()

    images = []
    
    index = 0

    while(index < len(data)):
        code, size, rgb, _ = tuple(data[index:index + 40].split(b'\n'))
        size_x, size_y = tuple(size.split(b' '))
        file_size = len(code) + len(size) + len(rgb) + 3 + int(size_x) * int(size_y) * 3
        images.append(Image.open(BytesIO(data[index:index + file_size])))
        index += file_size

    return images

def convert_from_bytes(pdf_file, save_path=None, dpi=200):
    """
        Description: Convert PDF to Image
        Parameters:
            pdf_file -> Bytes representing the PDF file
            dpi -> Image quality in DPI
    """

    proc = Popen(['pdftoppm', '-r', str(dpi), ], stdout=PIPE, stdin=PIPE)

    proc.stdin.write(pdf_file)

    data, err = proc.communicate()

    images = []
    
    index = 0

    while(index < len(data)):
        code, size, rgb, _ = tuple(data[index:index + 40].split(b'\n'))
        size_x, size_y = tuple(size.split(b' '))
        file_size = len(code) + len(size) + len(rgb) + 3 + int(size_x) * int(size_y) * 3
        images.append(Image.open(BytesIO(data[index:index + file_size])))
        index += file_size

    return images
