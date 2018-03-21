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

`convert_from_path(pdf_path, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm')`

`convert_from_bytes(pdf_file, dpi=200, output_folder=None, first_page=None, last_page=None, fmt='ppm')`


## What's new?
- `first_page` parameter allows you to set a first page to be processed by pdftoppm (`-f` in the cli of pdftoppm)
- `last_page` parameter allows you to set a last page to be processed by pdftoppm (`-l` in the cli of pdftoppm)
- `fmt` parameter allows you to specify an output format. Currently supported formats are `jpg`, `png`, and `ppm`

## Timing

You can reproduce those results by running the provided tests. The process' peak memory usage was added to help the comparison and was gathered using the `memory_profiler` module.

The time in second is on a per-page basis. The suffix \_X is how many page were converted.

All tests were ran with the default 200 dpi resolution.

My computer has an SSD. Run `python3 tests.py` for the timing on your machine.

| Test name | sec/page | Peak memory usage |
| --- | --- | --- |
| test_conversion_from_bytes | 0.08025979995727539 sec | 69.7 MiB
| test_conversion_from_bytes_14 | 0.07791144507271903 sec | 348.1 MiB
| test_conversion_from_bytes_14_last_page_12 | 0.015511631965637207 sec | 219.9 MiB
| test_conversion_from_bytes_14_first_page_2_last_page_12 | 0.053603836468287876 sec | 283.9 MiB
| test_conversion_from_bytes_14_last_page_12 | 0.05721770014081683 sec | 305.3 MiB
| test_conversion_from_bytes_241 | 0.040824553778557364 sec | 5210.9 MiB
| test_conversion_from_bytes_using_dir | 0.13207364082336426 sec | 2643.0 MiB
| test_conversion_from_bytes_using_dir_14 | 0.05664423533848354 sec | 2643.0 MiB
| test_conversion_from_bytes_using_dir_14_first_page_12 | 0.0180361270904541 sec | 2643.0 MiB
| test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12 | 0.07084715366363525 sec | 2643.0 MiB
| test_conversion_from_bytes_using_dir_14_last_page_12 | 0.06571905953543526 sec | 2643.0 MiB
| test_conversion_from_bytes_using_dir_241 | 0.03664693001394945 sec | 177.4 MiB
| test_conversion_from_path | 0.041847944259643555 sec | 177.4 MiB
| test_conversion_from_path_14 | 0.06815803050994873 sec | 347.7 MiB
| test_conversion_from_path_14_first_page_12 | 0.013361079352242606 sec | 177.4 MiB
| test_conversion_from_path_14_first_page_2_last_page_12 | 0.06226999419076102 sec | 284.3 MiB
| test_conversion_from_path_14_last_page_12 | 0.06276893615722656 sec | 305.7 MiB
| test_conversion_from_path_241 | 0.04187167630650691 sec | 5210.2 MiB
| test_conversion_from_path_using_dir | 0.1171102523803711 sec | 2642.3 MiB
| test_conversion_from_path_using_dir_14 | 0.05710525172097342 sec | 2642.3 MiB
| test_conversion_from_path_using_dir_14_first_page_12 | 0.0152871949332101 sec | 2642.3 MiB
| test_conversion_from_path_using_dir_14_first_page_2_last_page_12 | 0.04539140633174351 sec | 2642.3 MiB
| test_conversion_from_path_using_dir_14_last_page_12 | 0.05119928291865757 sec | 2642.3 MiB
| test_conversion_from_path_using_dir_241 | 0.03425470724145407 sec | 177.4 MiB
| test_conversion_to_jpeg_from_bytes_14 | 0.0022412879126412527 sec | 177.4 MiB
| test_conversion_to_jpeg_from_path_using_dir_14 | 0.002368075507027762 sec | 177.4 MiB
| test_conversion_to_png_from_bytes_14 | 0.010121209280831473 sec | 177.4 MiB
| test_conversion_to_png_from_path_using_dir_14 | 0.010833195277622767 sec | 177.4 MiB
| test_empty_if_corrupted_pdf | 0.008587360382080078 sec | 177.4 MiB
| test_empty_if_file_not_found | 0.008152961730957031 sec | 177.4 MiB
| test_empty_if_not_pdf | 0.01006937026977539 sec | 177.4 MiB


Bottom line: Use an output folder

## Exception handling

There are no exception thrown by pdftoppm therefore any file that couldn't be convert/processed will return an empty Image list. The philosophy behind this choice is simple, if the file was corrupted / not found, no image could be extracted and returning an empty list makes sense. (This is up for discussion)

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed (unless you use an output folder)
