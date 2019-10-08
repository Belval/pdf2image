# Installation

## Official package

pdf2image has a pip package with a matching name.

`pip install pdf2image`

## From source

If you want to add a new language The easiest way
to use the tool is by cloning the official repo.

`git clone https://github.com/Belval/pdf2image`

Then install the package with `python3 setup.py install`

## Installing poppler

Poppler is the underlying project that does the magic in pdf2image. You can check if you already have it installed by calling `pdftoppm -h` in your terminal/cmd.

### Ubuntu

`sudo apt-get install poppler-utils`

### Archlinux

`sudo pacman -S poppler`

### MacOS

`brew install poppler`

### Windows

1. Download the latest package from http://blog.alivate.com.au/poppler-windows/
2. Extract the package
3. Move the extracted directory to the desired place on your system
4. Add the `bin/` directory to your [PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
5. Test that all went well by opening `cmd` and making sure that you can call `pdftoppm -h`
