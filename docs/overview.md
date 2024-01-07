# Overview

pdf2image subscribes to the Unix philosophy of "Do one thing and do it well", and is only used to convert PDF into images.

You can convert from a path or from bytes with aptly named `convert_from_path` and `convert_from_bytes`.

```py
from pdf2image import convert_from_path, convert_from_bytes

images = convert_from_path("/home/user/example.pdf")

# OR

with open("/home/user/example.pdf","rb") as pdf:
    images = convert_from_bytes(pdf.read())
```

This is the most basic usage, but the converted images will exist in memory and that may not be what you want since you can exhaust resources quickly with big PDF.

Instead, use an `output_folder` to avoid using the memory directly. The images will stil be readable and Pillow takes care of loading them on demand.

```py
import tempfile

from pdf2image import convert_from_path


with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path("/home/user/example.pdf", output_folder=path)
```

Got it? Now by default `pdf2image` uses PPM as its file format. While the logic if abstracted by Pillow, this is still a raw file format that has no compression and is therefore quite big. Why not use good old JPEG?

`images_from_path = convert_from_path("/home/user/example.pdf", fmt="jpeg")`

Supported file formats are jpeg, png, tiff and ppm.

For a more in depth description of every parameters, see the [reference page](./reference.md).
