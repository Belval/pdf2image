"""
    Define exceptions specific to pdf2image
"""

class PageCountError(Exception):
    "Happens when the pdfinfo tool is not installed on the host"
    pass

class MissingFontError(Exception):
    "Happens when a font is missing from the host"
    pass
