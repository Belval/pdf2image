"""
    Define exceptions specific to pdf2image
"""


class PopplerNotInstalledError(Exception):
    """Raised when poppler is not installed"""

    pass


class PDFInfoNotInstalledError(PopplerNotInstalledError):
    """Raised when pdfinfo is not installed"""

    pass


class PDFPageCountError(Exception):
    """Raised when the pdfinfo was unable to retrieve the page count"""

    pass


class PDFSyntaxError(Exception):
    """Raised when a syntax error was thrown during rendering"""

    pass


class PDFPopplerTimeoutError(Exception):
    """Raised when the timeout is exceeded while converting a PDF"""

    pass
