# pdf2image [![TravisCI](https://travis-ci.org/Belval/pdf2image.svg?branch=master)](https://travis-ci.org/Belval/pdf2image) [![PyPI version](https://badge.fury.io/py/pdf2image.svg)](https://badge.fury.io/py/pdf2image)
A python3 module that wraps the pdftoppm utility to convert PDF to a PIL Image object

## How to install

` pip3 install pdf2image `

Install `Pillow` if you don't have it already with `pip3 install pillow`

###

pdftoppm is the piece of software that does the actual magic. It is distributed as part of a greater package called [poppler](https://poppler.freedesktop.org/).

Windows users will have to install [poppler for Windows](https://sourceforge.net/projects/poppler-win32/)

Mac users will have to install [poppler for Mac](http://macappstore.org/poppler/)

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

## Timing

You can reproduce those results by running the provided tests. The process' peak memory usage was added to help the comparison and was gathered using the `memory_profiler` module.

The time in second is on a per-page basis. The suffix \_X is how many page were converted.

All tests were ran with the default 200 dpi resolution.

My computer has an SSD. Run `python3 tests.py` for the timing on your machine.

```
conversion_from_bytes: 0.03930950164794922 sec @ 23 MB
conversion_from_bytes_14: 0.05591930661882673 sec @ 289.4 MB
conversion_from_bytes_241: 0.026828476007548605 sec @ 4991.1 MB
conversion_from_bytes_using_dir: 0.06357479095458984 sec @ 0 MB
conversion_from_bytes_using_dir_14: 0.052671926362173896 sec @ 0 MB
conversion_from_bytes_using_dir_241: 0.021176524182078254 sec @ 0.1 MB
conversion_from_path: 0.0684502124786377 sec @ 0 MB
conversion_from_path_14: 0.0592965909412929 sec @ 0 MB
conversion_from_path_241: 0.02652374441692938 sec @ 2568 MB
conversion_from_path_using_dir: 0.061820268630981445 sec @ 0 MB
conversion_from_path_using_dir_14: 0.052453075136457174 sec @ 0 MB
conversion_from_path_using_dir_241: 0.021224186133546947 sec @ 0 MB
empty_if_corrupted: 0.052927494049072266 sec @ 0 MB
empty_if_file_not_found: 0.05123734474182129 sec @ 0 MB
empty_if_not_pdf: 0.0519101619720459 sec @ 0 MB
```

Bottom line: Use an output folder

## Exception handling

There are no exception thrown by pdftoppm therefore any file that couldn't be convert/processed will return an empty Image list. The philosophy behind this choice is simple, if the file was corrupted / not found, no image could be extracted and returning an empty list makes sense. (This is up for discussion)

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
