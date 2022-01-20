# pdf2image
[![CircleCI](https://circleci.com/gh/Belval/pdf2image/tree/master.svg?style=svg)](https://circleci.com/gh/Belval/pdf2image/tree/master) [![PyPI version](https://badge.fury.io/py/pdf2image.svg)](https://badge.fury.io/py/pdf2image) [![codecov](https://codecov.io/gh/Belval/pdf2image/branch/master/graph/badge.svg)](https://codecov.io/gh/Belval/pdf2image) [![Downloads](https://pepy.tech/badge/pdf2image/month)](https://pepy.tech/project/pdf2image) [![Documentation Status](https://readthedocs.org/projects/pdf2image/badge/?version=latest)](https://pdf2image.readthedocs.io/en/latest/?badge=latest)

A python (3.6+) module that wraps pdftoppm and pdftocairo to convert PDF to a PIL Image object

## How to install

`pip install pdf2image`

### Windows

Windows users will have to build or download poppler for Windows. I recommend [@oschwartz10612 version](https://github.com/oschwartz10612/poppler-windows/releases/) which is the most up-to-date. You will then have to add the `bin/` folder to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) or use `poppler_path = r"C:\path\to\poppler-xx\bin" as an argument` in `convert_from_path`.

### Mac

Mac users will have to install [poppler for Mac](http://macappstore.org/poppler/).

### Linux

Most distros ship with `pdftoppm` and `pdftocairo`. If they are not installed, refer to your package manager to install `poppler-utils`

### Platform-independant (Using `conda`)

1. Install poppler: `conda install -c conda-forge poppler`
2. Install pdf2image: `pip install pdf2image`

## How does it work?

`from pdf2image import convert_from_path, convert_from_bytes`

```py
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
```

Then simply do:

```py
images = convert_from_path('/home/belval/example.pdf')
```

OR

```py
images = convert_from_bytes(open('/home/belval/example.pdf', 'rb').read())
```

OR better yet

```py
import tempfile

with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path('/home/belval/example.pdf', output_folder=path)
    # Do something here
```

`images` will be a list of PIL Image representing each page of the PDF document.

Here are the definitions:

`convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, grayscale=False, size=None, paths_only=False, use_pdftocairo=False, timeout=600)`

`convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', jpegopt=None, thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, single_file=False, output_file=str(uuid.uuid4()), poppler_path=None, grayscale=False, size=None, paths_only=False, use_pdftocairo=False, timeout=600)`

## What's new?

- Allow users to hide attributes when using pdftoppm with `hide_attributes` (Thank you @StaticRocket)
- Fix console opening on Windows (Thank you @OhMyAgnes!)
- Add `timeout` parameter which raises `PDFPopplerTimeoutError` after the given number of seconds.
- Add `use_pdftocairo` parameter which forces `pdf2image` to use `pdftocairo`. Should improve performance.
- Fixed a bug where using `pdf2image` with multiple threads (but not multiple processes) would cause and exception
- `jpegopt` parameter allows for tuning of the output JPEG when using `fmt="jpeg"` (`-jpegopt` in pdftoppm CLI) (Thank you @abieler)
- `pdfinfo_from_path` and `pdfinfo_from_bytes` which expose the output of the pdfinfo CLI
- `paths_only` parameter will return image paths instead of Image objects, to prevent OOM when converting a big PDF
- `size` parameter allows you to define the shape of the resulting images (`-scale-to` in pdftoppm CLI)
    - `size=400` will fit the image to a 400x400 box, preserving aspect ratio
    - `size=(400, None)` will make the image 400 pixels wide, preserving aspect ratio
    - `size=(500, 500)` will resize the image to 500x500 pixels, not preserving aspect ratio
- `grayscale` parameter allows you to convert images to grayscale (`-gray` in pdftoppm CLI)
- `single_file` parameter allows you to convert the first PDF page only, without adding digits at the end of the `output_file`
- Allow the user to specify poppler's installation path with `poppler_path`

## Performance tips

- Using an output folder is significantly faster if you are using an SSD. Otherwise i/o usually becomes the bottleneck.
- Using multiple threads can give you some gains but avoid more than 4 as this will cause i/o bottleneck (even on my NVMe SSD!).
- If i/o is your bottleneck, using the JPEG format can lead to significant gains.
- PNG format is pretty slow, this is because of the compression.
- If you want to know the best settings (most settings will be fine anyway) you can clone the project and run `python tests.py` to get timings.

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
