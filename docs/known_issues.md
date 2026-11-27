# Limitations / Known Issues

## DocuSign PDFs 

If you have this [error](https://stackoverflow.com/questions/66636441/pdf2image-library-failing-to-read-pdf-signed-using-docusign):

```bash
pdf2image.exceptions.PDFPageCountError: Unable to get page count.
Syntax Error: Gen inside xref table too large (bigger than INT_MAX)
Syntax Error: Invalid XRef entry 3
Syntax Error: Top-level pages object is wrong type (null)
Command Line Error: Wrong page range given: the first page (1) can not be after the last page (0).
```

You are using a poppler version older than **21.01.0**, which is when the fix for
these broken xref tables landed in `poppler/XRef.cc` (see the
[21.01.0 release notes](https://gitlab.freedesktop.org/poppler/poppler/-/blob/poppler-21.01.0/NEWS),
entry "Fix various issues handling broken files"). Check your version with
`pdfinfo -v`. Known affected distro packages include Debian 11 (`poppler-utils`
20.09) and Ubuntu 20.04 (0.86); Debian 12 and Ubuntu 22.04 ship fixed versions.

Solutions, in order of preference:

1. **Use a base image that ships poppler ≥ 21.01.0** (Debian 12, Ubuntu 22.04+).

2. **Compile poppler from source** — no OS upgrade required. pdf2image only
   shells out to `pdfinfo` and `pdftoppm`, so installing into `/usr/local`
   is picked up automatically:

   ```dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends \
       build-essential cmake pkg-config wget xz-utils libboost-dev \
       libfontconfig1-dev libfreetype6-dev libjpeg8-dev liblcms2-dev \
       libopenjp2-7-dev libpng-dev libtiff-dev zlib1g-dev \
       && rm -rf /var/lib/apt/lists/*
   RUN wget -q https://poppler.freedesktop.org/poppler-24.02.0.tar.xz \
       && tar -x -f poppler-24.02.0.tar.xz \
       && cd poppler-24.02.0 && mkdir build && cd build \
       && cmake -DCMAKE_BUILD_TYPE=Release \
                -DENABLE_QT5=OFF -DENABLE_QT6=OFF -DENABLE_GLIB=OFF -DENABLE_CPP=OFF \
                -DENABLE_NSS3=OFF -DENABLE_LIBCURL=OFF -DENABLE_GPGME=OFF \
                -DBUILD_MANUAL_TESTS=OFF -DENABLE_GTK_DOC=OFF .. \
       && make -j$(nproc) && make install && ldconfig
   ```

   Notes: `libboost-dev` is required by the Splash backend, and
   `-DENABLE_GPGME=OFF` avoids the Gpgmepp ≥ 1.19 requirement that older
   distros cannot satisfy. Pin the tarball version and verify its SHA256
   for reproducible builds.

3. Verify with `pdfinfo your-document.pdf` — it should print the page count
   and exit 0.

More details [here](https://github.com/Belval/pdf2image/issues/234).
