# Reference

## Functions

### convert_from_path & convert_from_bytes

Converts a PDF into image(s)

```py
convert_from_path(
    pdf_path,
    dpi=200,
    output_folder=None,
    first_page=None,
    last_page=None,
    fmt="ppm",
    jpegopt=None,
    thread_count=1,
    userpw=None,
    use_cropbox=False,
    strict=False,
    transparent=False,
    single_file=False,
    output_file=uuid_generator(),
    poppler_path=None,
    grayscale=False,
    size=None,
    paths_only=False,
    mono=False,
)

convert_from_bytes(
    pdf_bytes,
    dpi=200,
    output_folder=None,
    first_page=None,
    last_page=None,
    fmt="ppm",
    jpegopt=None,
    thread_count=1,
    userpw=None,
    use_cropbox=False,
    strict=False,
    transparent=False,
    single_file=False,
    output_file=uuid_generator(),
    poppler_path=None,
    grayscale=False,
    size=None,
    paths_only=False,
    mono=False,
)
```

**pdf_path**

Path to the PDF file. Can be a string or a `pathlib.Path` object

**pdf_bytes**

Bytes of the PDF file.

**dpi**

Dots per inch, can be seen as the relative resolution of the output PDF, higher is better but anything above 300 is usually not discernable to the naked eye. Keep in mind that this is directly related to the ouput images size when using file formats without compression (like PPM)

**output_folder**

Output directory for the generated files, should be seen more as a "working directory" than an output folder. The converted images will be written there to save system memory.

**first_page**

First page that will be converted. `first_page=2` will skip page 1.

**last_page**

Last page that will be converted. `last_page=2` will skip all pages after page 2.

**fmt**

File format or the output images. Supported values are `ppm`, `jpeg`, `png` and `tiff`.

**jpegopt**

Configuration for the jpeg output format. As such, only used with `fmt='jpeg'`.

```
jpegopt={
    "quality": 100,
    "progressive": True,
    "optimize": True
}
```

- `quality`: Selects the JPEG quality value. The value must be an integer between 0 and 100.
- `progressive`: Select progressive JPEG output. The possible values are `True`, `False`, indicating progressive (yes) or non-progressive (no), respectively.
- `optimize`: Sets whether to compute optimal Huffman coding tables for the JPEG output, which will create smaller files but make an extra pass over the data. The value must be `True` or `False`, with `True` performing optimization, otherwise the default Huffman tables are used.

**thread_count**

Number of threads to use when converting the PDF. Limited to the actual number of pages.

**userpw**

Password for the PDF if it is password-protected.

**use_cropbox**

Uses the PDF cropbox instead of the default mediabox. This is a rather dark feature that should be set to true when the module does not seem to work with your data.

**strict**

Raises PDFSyntaxError when the PDF is partially malformed. Most PDF are partially malformed and that parameter should be kept to `False`, unless standard compliance is paramount to your use case.

**transparent**

Instead of returning a white background, make the PDF background transparent. Only compatible with file formats that support transparency.

**single_file**

Only convert the PDF first page and does not append an index to the output file name.

**output_file**

Output filename, normally string, but can take a string generator.

**poppler_path**

Path to the poppler directory containing librairies and executable files.

**grayscale**

Returns grayscale images

**size**

Size of output images, using `None` as any of the dimension will resize and preserve aspect ratio.

Examples of valid sizes are:

- `size=400` will fit the image to a 400x400 box, preserving aspect ratio
- `size=(400, None)` will make the image 400 pixels wide, preserving aspect ratio
- `size=(500, 500)` will resize the image to 500x500 pixels, not preserving aspect ratio

This behavior is derived directly from the `-scale-to`, `-scale-to-x`, and `-scale-to-y` parameters.

**paths_only**

A list of image paths rather than preloaded images are returned.

**jpegopt**

Provide additional options for jpeg format conversions. Requires `fmt="jpeg"` and is provided as dict, with all
optinal keywords:
`jpegopt={"quality": 100, "optimize": True, "progressive": False}

## Exceptions

```py
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
```

### PDFInfoNotInstalledError

Exception raised when `pdfinfo`, which is part of poppler-utils, was not found on your system. This can be tested by trying to call it from your command line.

When this error is raised, the error is almost always installation related.

### PDFPageCountError

Exception raised when `pdfinfo`, which is part of poppler-utils, was unable to get the page count from the PDF file. This is usually due to:

- An invalid PDF file path
- A malformed or invalid PDF

### PDFSyntaxError

Exception raised when `convert_from_path` or `convert_from_bytes` is called using `strict=True` and the input PDF contained a syntax error. Simply use `strict=False` will usually solve this issue.

Note that most PDF contain syntax errors and you can safely ignore strict mode.
