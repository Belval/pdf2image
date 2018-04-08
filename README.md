# pdf2image [![TravisCI](https://travis-ci.org/Belval/pdf2image.svg?branch=master)](https://travis-ci.org/Belval/pdf2image) [![PyPI version](https://badge.fury.io/py/pdf2image.svg)](https://badge.fury.io/py/pdf2image) [![codecov](https://codecov.io/gh/Belval/pdf2image/branch/master/graph/badge.svg)](https://codecov.io/gh/Belval/pdf2image)
A python3 module that wraps the pdftoppm utility to convert PDF to a PIL Image object

## How to install

` pip3 install pdf2image `

Install `Pillow` if you don't have it already with `pip3 install pillow`

###

pdftoppm is the piece of software that does the actual magic. It is distributed as part of a greater package called [poppler](https://poppler.freedesktop.org/).

Windows users will have to install [poppler for Windows](http://blog.alivate.com.au/poppler-windows/).

Mac users will have to install [poppler for Mac](http://macappstore.org/poppler/).

Linux users will have pdftoppm pre-installed with the distro (Tested on Ubuntu and Archlinux) if it's not, run `sudo apt install poppler-utils`

## How does it work?
` from pdf2image import convert_from_path, convert_from_bytes `

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

`convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm')`

`convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm')`

## What's new?
- `userpw` parameter allows you to set a password to unlock the converted PDF (`-upw` in the cli of pdftoppm)
- `thread_count` parameter allows you to set how many thread will be used for conversion.
- `first_page` parameter allows you to set a first page to be processed by pdftoppm (`-f` in the cli of pdftoppm)
- `last_page` parameter allows you to set a last page to be processed by pdftoppm (`-l` in the cli of pdftoppm)
- `fmt` parameter allows you to specify an output format. Currently supported formats are `jpg`, `png`, and `ppm`

## Performance tips

- Using an output folder is significantly faster if you are using an SSD. Otherwise i/o usually becomes the bottleneck.
- Using multiple threads can give you some gains but avoid more than 4 as this will cause i/o bottleneck (even on my NVMe SSD!).
- If i/o is your bottleneck, using the JPEG format can lead to significant gains.
- PNG format is pretty slow, I am investigating the issue.
- If you want to know the best settings (most settings will be fine anyway) you can clone the project and run `python tests.py` to get timings.

## Exception handling

There are no exception thrown by pdftoppm therefore any file that couldn't be convert/processed will return an empty Image list. The philosophy behind this choice is simple, if the file was corrupted / not found, no image could be extracted and returning an empty list makes sense. (This is up for discussion)

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
