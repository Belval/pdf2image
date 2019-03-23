# pdf2image [![TravisCI](https://travis-ci.org/Belval/pdf2image.svg?branch=master)](https://travis-ci.org/Belval/pdf2image) [![PyPI version](https://badge.fury.io/py/pdf2image.svg)](https://badge.fury.io/py/pdf2image) [![codecov](https://codecov.io/gh/Belval/pdf2image/branch/master/graph/badge.svg)](https://codecov.io/gh/Belval/pdf2image)
A python 2.7 and 3.3+ module that wraps pdftoppm and pdftocairo to convert PDF to a PIL Image object

## How to install

### First you need poppler-utils

pdftoppm and pdftocairo are the piece of software that do the actual magic. It is distributed as part of a greater package called [poppler](https://poppler.freedesktop.org/).

Windows users will have to install [poppler for Windows](http://blog.alivate.com.au/poppler-windows/), then add the `bin/` folder to [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).

Mac users will have to install [poppler for Mac](http://macappstore.org/poppler/).

Linux users will have both tools pre-installed with Ubuntu 16.04+ and Archlinux. If it's not, run `sudo apt install poppler-utils`

### Then you can install the pip package!

`pip install pdf2image`

Install `Pillow` if you don't have it already with `pip install pillow`

## How does it work?

`from pdf2image import convert_from_path, convert_from_bytes`
``` py
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
```

Then simply do:

``` py
images = convert_from_path('/home/kankroc/example.pdf')
```

OR

``` py
images = convert_from_bytes(open('/home/kankroc/example.pdf', 'rb').read())
```

OR better yet

``` py
import tempfile

with tempfile.TemporaryDirectory() as path:
     images_from_path = convert_from_path('/home/kankroc/example.pdf', output_folder=path)
     # Do something here
```

`images` will be a list of PIL Image representing each page of the PDF document.

Here are the definitions:

`convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, poppler_path=None)`

`convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm', thread_count=1, userpw=None, use_cropbox=False, strict=False, transparent=False, poppler_path=None)`

## What's new?
- Allow the user to specify poppler's installation path with `poppler_path`
- Fixed a bug where PNGs buffer with a non-terminating I-E-N-D sequence would throw an exception   
- Fixed a bug that left open file descriptors when using `convert_from_bytes()` (Thank you @FabianUken)
- `fmt='tiff'` parameter allowss you to create .tiff files (You need pdftocairo for this)
- `transparent` parameter allows you to generate images with no background instead of the usual white one (You need pdftocairo for this)
- `strict` parameter allows you to catch pdftoppm syntax error with a custom type `PDFSyntaxError`
- `use_cropbox` parameter allows you to use the crop box instead of the media box when converting (`-cropbox` in pdftoppm's CLI)
- `userpw` parameter allows you to set a password to unlock the converted PDF (`-upw` in pdftoppm's CLI)

## Performance tips

- Using an output folder is significantly faster if you are using an SSD. Otherwise i/o usually becomes the bottleneck.
- Using multiple threads can give you some gains but avoid more than 4 as this will cause i/o bottleneck (even on my NVMe SSD!).
- If i/o is your bottleneck, using the JPEG format can lead to significant gains.
- PNG format is pretty slow, I am investigating the issue.
- If you want to know the best settings (most settings will be fine anyway) you can clone the project and run `python tests.py` to get timings.

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
