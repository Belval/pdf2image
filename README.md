# pdf2image
A python3 module that wraps the pdftoppm utility to convert PDF to the PIL image formatt

## How to install

` pip install pdf2image `

Windows users will have to install [pdftoppm](https://sourceforge.net/projects/poppler-win32/)

Linux users will have pdftoppm pre-installed with the distro (Tested on Ubuntu and Archlinux)

## How does it work?
` from pdf2image import convert_from_path, convert_from_bytes `

Then simply do:

` images = convert_from_path('/home/kankroc/example.pdf') `

OR

` images = convert_from_bytes(open('/home/kankroc/example.pdf', 'rb').read()) `

`images` will be a list of PIL Image representing each page of the PDF document.

## Limitations / known issues

- A relatively big PDF will use up all your memory and cause the process to be killed
- pdftoppm errors are not handled
- Not Python 2 compatible
