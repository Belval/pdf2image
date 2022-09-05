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

You are possibly using an old version of poppler. The solution is to update to the latest version. Similarly, if you are working with Docker (Debian 11 Image), maybe you can not update poppler because is not available. So, you have to use an image in ubuntu, install Python and then what you need.

More details [here](https://github.com/Belval/pdf2image/issues/234).