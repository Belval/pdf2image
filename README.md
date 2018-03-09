# pdf2image [![TravisCI](https://travis-ci.org/Belval/pdf2image.svg?branch=master)](https://travis-ci.org/Belval/pdf2image) [![PyPI version](https://badge.fury.io/py/pdf2image.svg)](https://badge.fury.io/py/pdf2image) [![codecov](https://codecov.io/gh/Belval/pdf2image/branch/master/graph/badge.svg)](https://codecov.io/gh/Belval/pdf2image)
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

Here are the definitions:

`convert_from_path(pdf_path, dpi=200, output_folder=None, max_page_count=None, fmt='ppm')`

`convert_from_bytes(pdf_file, dpi=200, output_folder=None, max_page_count=None, fmt='ppm')`


## What's new?

- `max_page_count` parameter allows you to limit how many pages will be processed by pdftoppm (`-l` in the cli)
- `fmt` parameter allows you to specify an output format. Currently supported formats are `jpg`, `png`, and `ppm`

## Timing

You can reproduce those results by running the provided tests. The process' peak memory usage was added to help the comparison and was gathered using the `memory_profiler` module.

The time in second is on a per-page basis. The suffix \_X is how many page were converted.

All tests were ran with the default 200 dpi resolution.

My computer has an SSD. Run `python3 tests.py` for the timing on your machine.

| Test name | sec/page | Peak memory usage |
| --- | --- | --- |
| test_conversion_from_bytes | 0.1403517723083496 sec | 23.4 MiB |
| test_conversion_from_bytes_14 | 0.08628017561776298 sec | 289.6 MiB |
| test_conversion_from_bytes_14_max_page_count_12 | 0.07760441303253174 sec | 85.5 MiB |
| test_conversion_from_bytes_241 | 0.05936517952883392 sec | 5033.9 MiB |
| test_conversion_from_bytes_using_dir | 0.06892609596252441 sec | 0.0 MiB |
| test_conversion_from_bytes_using_dir_14 | 0.05760715688977923 sec | 0.0 MiB |
| test_conversion_from_bytes_using_dir_14_max_page_count_12 | 0.05288205827985491 sec | 0.0 MiB |
| test_conversion_from_bytes_using_dir_241 | 0.02622196882097553 sec | 0.1 MiB |
| test_conversion_from_path | 0.08991026878356934 sec | 0.0 MiB |
| test_conversion_from_path_14 | 0.09094854763575963 sec | 0.0 MiB |
| test_conversion_from_path_14_max_page_count_12 | 0.07591407639639718 sec | 0.0 MiB |
| test_conversion_from_path_241 | 0.05391744953962777 sec | 2568.0 MiB |
| test_conversion_from_path_using_dir | 0.06876587867736816 sec | 0.0 MiB |
| test_conversion_from_path_using_dir_14 | 0.057496104921613424 sec | 0.0 MiB |
| test_conversion_from_path_using_dir_14_max_page_count_12 | 0.05267822742462158 sec | 0.0 MiB |
| test_conversion_from_path_using_dir_241 | 0.026008206284392425 sec | 0.0 MiB |
| test_conversion_to_jpeg_from_bytes_14 | 0.0049211808613368446 sec | 0.0 MiB |
| test_conversion_to_jpeg_from_path_using_dir_14 | 0.005251186234610421 sec | 0.0 MiB |
| test_conversion_to_png_from_bytes_14 | 0.014363850866045271 sec | 0.1 MiB |
| test_conversion_to_png_from_path_using_dir_14 | 0.014109304973057337 sec | 0.0 MiB |
| test_empty_if_corrupted_pdf | 0.04371809959411621 sec | 0.0 MiB |
| test_empty_if_file_not_found | 0.04585576057434082 sec | 0.0 MiB |
| test_empty_if_not_pdf | 0.048310041427612305 sec | 0.0 MiB |


Bottom line: Use an output folder

## Exception handling

There are no exception thrown by pdftoppm therefore any file that couldn't be convert/processed will return an empty Image list. The philosophy behind this choice is simple, if the file was corrupted / not found, no image could be extracted and returning an empty list makes sense. (This is up for discussion)

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
