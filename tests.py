import os
import sys
import errno
import pathlib
import tempfile
import unittest
import time
import shutil
import subprocess
from inspect import signature
from subprocess import Popen, PIPE
from tempfile import TemporaryDirectory
from multiprocessing.dummy import Pool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pdf2image import (
    convert_from_bytes,
    convert_from_path,
    pdfinfo_from_bytes,
    pdfinfo_from_path,
)
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFPopplerTimeoutError,
)

from functools import wraps

PROFILE_MEMORY = os.environ.get("PROFILE_MEMORY", False)
if PROFILE_MEMORY:
    from memory_profiler import profile as profile_memory

try:
    subprocess.call(
        ["pdfinfo", "-h"], stdout=open(os.devnull, "w"), stderr=open(os.devnull, "w")
    )
    POPPLER_INSTALLED = True
except OSError as e:
    if e.errno == errno.ENOENT:
        POPPLER_INSTALLED = False


def profile(f):
    if PROFILE_MEMORY:

        @wraps(f)
        @profile_memory
        def wrapped(*args, **kwargs):
            r = f(*args, **kwargs)
            return r

        return wrapped
    else:

        @wraps(f)
        def wrapped(*args, **kwargs):
            r = f(*args, **kwargs)
            return r

        return wrapped


def get_poppler_path():
    return pathlib.Path(
        Popen(["which", "pdftoppm"], stdout=PIPE).communicate()[0].strip().decode()
    ).parent


class PDFConversionMethods(unittest.TestCase):
    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 1)
        print("test_conversion_from_bytes: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf")
        self.assertTrue(len(images_from_path) == 1)
        print("test_conversion_from_path: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path("./tests/test.pdf", output_folder=path)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 14)
        print(
            "test_conversion_from_bytes_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf")
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_14.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path
                )
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path
            )
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    def test_conversion_from_bytes_241(self):  # pragma: no cover
        start_time = time.time()
        with open("./tests/test_241.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 241)
        print(
            "test_conversion_from_bytes_241: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    def test_conversion_from_path_241(self):  # pragma: no cover
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_241.pdf")
        self.assertTrue(len(images_from_path) == 241)
        print(
            "test_conversion_from_path_241: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    def test_conversion_from_bytes_using_dir_241(self):  # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_241.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path
                )
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_241: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    def test_conversion_from_path_using_dir_241(self):  # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_241.pdf", output_folder=path
            )
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_241: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_not_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path("./tests/test.jpg")
        print("test_empty_if_not_pdf: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_file_not_found(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path("./tests/totally_a_real_file_in_folder.xyz")
        print("test_empty_if_file_not_found: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_empty_if_corrupted_pdf(self):
        start_time = time.time()
        with self.assertRaises(Exception):
            convert_from_path("./tests/test_corrupted.pdf")
        print("test_empty_if_corrupted_pdf: {} sec".format(time.time() - start_time))

    ## Test first page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_first_page_12(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), first_page=12)
            self.assertTrue(len(images_from_bytes) == 3)
        print(
            "test_conversion_from_bytes_14_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf", first_page=12)
        self.assertTrue(len(images_from_path) == 3)
        print(
            "test_conversion_from_path_14_first_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_first_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_14.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, first_page=12
                )
                self.assertTrue(len(images_from_bytes) == 3)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_14_first_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_first_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path, first_page=12
            )
            self.assertTrue(len(images_from_path) == 3)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14_first_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test last page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_last_page_12(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), last_page=12)
            self.assertTrue(len(images_from_bytes) == 12)
        print(
            "test_conversion_from_bytes_14_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf", last_page=12)
        self.assertTrue(len(images_from_path) == 12)
        print(
            "test_conversion_from_path_14_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_14.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, last_page=12
                )
                self.assertTrue(len(images_from_bytes) == 12)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_14_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path, last_page=12
            )
            self.assertTrue(len(images_from_path) == 12)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test first and last page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(), first_page=2, last_page=12
            )
            self.assertTrue(len(images_from_bytes) == 11)
        print(
            "test_conversion_from_bytes_14_first_page_2_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_2_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test_14.pdf", first_page=2, last_page=12
        )
        self.assertTrue(len(images_from_path) == 11)
        print(
            "test_conversion_from_path_14_first_page_2_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_14.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, first_page=2, last_page=12
                )
                self.assertTrue(len(images_from_bytes) == 11)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path, first_page=2, last_page=12
            )
            self.assertTrue(len(images_from_path) == 11)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14_first_page_2_last_page_12: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test output as jpeg

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_jpeg_from_bytes(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt="jpg")
            self.assertTrue(images_from_bytes[0].format == "JPEG")
        print(
            "test_conversion_to_jpeg_from_bytes_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_jpeg_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, fmt="jpeg"
            )
            self.assertTrue(images_from_path[0].format == "JPEG")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_jpeg_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test output as png

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_png_from_bytes(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt="png")
            self.assertTrue(images_from_bytes[0].format == "PNG")
        print(
            "test_conversion_to_png_from_bytes_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_png_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, fmt="png"
            )
            self.assertTrue(images_from_path[0].format == "PNG")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_png_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test output with not-empty output_folder

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_non_empty_output_folder(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf", output_folder="./tests/"
        )
        self.assertTrue(len(images_from_path) == 1)
        [im.close() for im in images_from_path]
        [os.remove(im.filename) for im in images_from_path]
        print(
            "test_non_empty_output_folder: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test format that starts with a dot

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_format_that_starts_with_a_dot(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_format_that_starts_with_a_dot: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test locked PDF

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_userpw_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_locked_user_only.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg", userpw="pdf2image"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_locked_pdf_with_userpw_only: {} sec".format(time.time() - start_time)
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_not_locked_pdf(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg", userpw="pdf2image"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_locked_pdf_with_userpw_only: {} sec".format(time.time() - start_time)
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_ownerpw_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_locked_owner_only.pdf", "rb") as pdf_file:
                # No need to pass a ownerpw because the absence of userpw means we can read it anyway
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_locked_pdf_with_ownerpw_only: {} sec".format(time.time() - start_time)
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_ownerpw_and_userpw(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_locked_both.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg", userpw="pdf2image"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_locked_pdf_with_ownerpw_and_userpw: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_locked_pdf_with_ownerpw_and_userpw_forgotten(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_locked_both_user_forgotten.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, fmt=".jpg", ownerpw="pdf2image"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_locked_pdf_with_ownerpw_and_userpw_forgotten: {} sec".format(
                time.time() - start_time
            )
        )

    ## Tests cropbox

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_cropbox(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), use_cropbox=True)
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_using_cropbox: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_cropbox(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", use_cropbox=True)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_using_cropbox: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_and_cropbox(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, use_cropbox=True
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_and_cropbox: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_and_cropbox(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, use_cropbox=True
            )
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_and_cropbox: {} sec".format(
                time.time() - start_time
            )
        )

    ## Tests multithreading

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_with_4_threads(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=4)
            self.assertTrue(len(images_from_bytes) == 14)
        print(
            "test_conversion_from_bytes_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_with_4_threads(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf", thread_count=4)
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_14_with_15_threads(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=15)
            self.assertTrue(len(images_from_bytes) == 14)
        print(
            "test_conversion_from_bytes_14_with_15_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_with_0_threads(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf", thread_count=0)
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_path_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_14_with_4_threads(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_14.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, thread_count=4
                )
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_with_4_threads(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path, thread_count=4
            )
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14_with_4_thread: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_241_with_4_threads(self):  # pragma: no cover
        start_time = time.time()
        with open("./tests/test_241.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), thread_count=4)
            self.assertTrue(len(images_from_bytes) == 241)
        print(
            "test_conversion_from_bytes_241_with_4_thread: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_241_with_4_threads(self):  # pragma: no cover
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_241.pdf", thread_count=4)
        self.assertTrue(len(images_from_path) == 241)
        print(
            "test_conversion_from_path_241_with_4_thread: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_241_with_4_threads(
        self,
    ):  # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_241.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, thread_count=4
                )
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_241_with_4_thread: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    @profile
    @unittest.skipIf(
        "CIRCLECI" in os.environ and os.environ["CIRCLECI"] == "true",
        "Skipping this test on CircleCI.",
    )
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_241_with_4_threads(
        self,
    ):  # pragma: no cover
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_241.pdf", output_folder=path, thread_count=4
            )
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_241_with_4_thread: {} sec".format(
                (time.time() - start_time) / 241.0
            )
        )

    # Testing custom exceptions

    @unittest.skipIf(POPPLER_INSTALLED, "Poppler is installed, skipping.")
    def test_pdfinfo_not_installed_throws(self):
        start_time = time.time()
        try:
            images_from_path = convert_from_path("./tests/test_14.pdf")
            raise Exception("This should not happen")
        except PDFInfoNotInstalledError as ex:
            pass

        print(
            "test_pdfinfo_not_installed_throws: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_missingfonterror_throws(self):
        start_time = time.time()
        try:
            images_from_path = convert_from_path("./tests/test_strict.pdf", strict=True)
            raise Exception("This should not happen")
        except PDFSyntaxError as ex:
            pass

        print("test_syntaxerror_throws: {} sec".format(time.time() - start_time))

    # Test transparent

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_transparent(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(), transparent=True, fmt="png"
            )
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_using_transparent: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_transparent(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf", transparent=True, fmt="png"
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_using_transparent: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_and_transparent(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), output_folder=path, transparent=True, fmt="png"
                )
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_and_transparent: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_and_transparent(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, transparent=True, fmt="png"
            )
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_and_transparent: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_transparent_without_png(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", transparent=True)
        self.assertTrue(len(images_from_path) == 1)
        [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_transparent_without_png: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test output as TIFF

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_tiff_from_bytes(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt="tiff")
            self.assertTrue(images_from_bytes[0].format == "TIFF")
        print(
            "test_conversion_to_tiff_from_bytes_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_tiff_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, fmt="tiff"
            )
            self.assertTrue(images_from_path[0].format == "TIFF")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_tiff_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test hanging file handles

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(not os.name == "posix", "This test only works on posix systems")
    def test_close_tempfile_after_conversion(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            fd_count_before = len(
                subprocess.check_output(
                    ["ls", "-l", "/proc/" + str(os.getpid()) + "/fd"]
                )
                .decode("utf8")
                .split("\n")
            )
            pdf_data = pdf_file.read()
            images_from_bytes = []
            for i in range(50):
                images_from_bytes.extend(convert_from_bytes(pdf_data))
            # Closing the images
            [im.close() for im in images_from_bytes]
            pid = os.getpid()
            fd_count_after = len(
                subprocess.check_output(
                    ["ls", "-l", "/proc/" + str(os.getpid()) + "/fd"]
                )
                .decode("utf8")
                .split("\n")
            )
            # Add an error margin
            self.assertTrue(abs(fd_count_before - fd_count_after) <= 3)
        print(
            "test_close_tempfile_after_conversion: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test poppler_path

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(not os.name == "posix", "This test only works on posix systems")
    def test_use_poppler_path(self):
        os.mkdir("./bin")
        shutil.copy("/usr/bin/pdftoppm", "./bin")
        shutil.copy("/usr/bin/pdfinfo", "./bin")
        start_time = time.time()
        try:
            images_from_path = convert_from_path(
                "./tests/test.pdf", poppler_path="./bin"
            )
        finally:
            shutil.rmtree("./bin")
        self.assertTrue(len(images_from_path) == 1)
        [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_poppler_path: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    @unittest.skipIf(not os.name == "posix", "This test only works on posix systems")
    def test_use_poppler_path_with_trailing_slash(self):
        os.mkdir("./bin")
        shutil.copy("/usr/bin/pdftoppm", "./bin")
        shutil.copy("/usr/bin/pdfinfo", "./bin")
        start_time = time.time()
        try:
            images_from_path = convert_from_path(
                "./tests/test.pdf", poppler_path="./bin/"
            )
        finally:
            shutil.rmtree("./bin")
        self.assertTrue(len(images_from_path) == 1)
        [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_poppler_path_with_trailing_slash: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test first page greater or equal to last_page

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_1_last_page_1(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test_14.pdf", first_page=1, last_page=1
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_14_first_page_1_last_page_1: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_14_first_page_12_last_page_1(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test_14.pdf", first_page=12, last_page=1
        )
        self.assertTrue(len(images_from_path) == 0)
        print(
            "test_conversion_from_path_14_first_page_12_last_page_1: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test singlefile

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_using_dir_single_file(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test.pdf", "rb") as pdf_file:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(),
                    output_folder=path,
                    output_file="test",
                    single_file=True,
                )
                self.assertTrue(len(images_from_bytes) == 1)
                self.assertTrue(
                    images_from_bytes[0].filename == os.path.join(path, "test.ppm")
                )
                [im.close() for im in images_from_bytes]
        print(
            "test_conversion_from_bytes_using_dir_single_file: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_single_file(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf",
                output_folder=path,
                output_file="test",
                single_file=True,
            )
            self.assertTrue(len(images_from_path) == 1)
            self.assertTrue(
                images_from_path[0].filename == os.path.join(path, "test.ppm")
            )
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_single_file: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_14_single_file(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf",
                output_folder=path,
                output_file="test",
                single_file=True,
            )
            self.assertTrue(len(images_from_path) == 1)
            self.assertTrue(
                images_from_path[0].filename == os.path.join(path, "test.ppm")
            )
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_14_single_file: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test file with same name in directory

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_with_containing_file_with_same_name(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            shutil.copyfile("./tests/test.pdf", os.path.join(path, "test.pdf"))
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, output_file="test"
            )
            self.assertTrue(len(images_from_path) == 1)
            self.assertTrue(
                images_from_path[0].filename == os.path.join(path, "test0001-1.ppm")
            )
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_path_using_dir_single_file: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test grayscale option

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_grayscale_from_bytes(self):
        start_time = time.time()
        with open("./tests/test_14.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), grayscale=True)
            self.assertTrue(images_from_bytes[0].mode == "L")
        print(
            "test_conversion_to_grayscale_from_bytes_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_grayscale_from_path(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test_14.pdf", grayscale=True)
        self.assertTrue(images_from_path[0].mode == "L")
        [im.close() for im in images_from_path]
        print(
            "test_conversion_to_grayscale_from_path_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_to_grayscale_from_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test_14.pdf", output_folder=path, grayscale=True
            )
            self.assertTrue(images_from_path[0].mode == "L")
            [im.close() for im in images_from_path]
        print(
            "test_conversion_to_grayscale_from_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test pathlib support

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_pathlib_path_using_dir(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                pathlib.Path("./tests/test.pdf"),
                output_folder=pathlib.Path(path),
                poppler_path=get_poppler_path(),
            )
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_pathlib_path_using_dir: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_pathlib_path_14(self):
        start_time = time.time()
        images_from_path = convert_from_path(pathlib.Path("./tests/test_14.pdf"))
        self.assertTrue(len(images_from_path) == 14)
        print(
            "test_conversion_from_pathlib_path_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_pathlib_path_using_dir_14(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                pathlib.Path("./tests/test_14.pdf"),
                output_folder=pathlib.Path(path),
                poppler_path=get_poppler_path(),
            )
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print(
            "test_conversion_from_pathlib_path_using_dir_14: {} sec".format(
                (time.time() - start_time) / 14.0
            )
        )

    ## Test jpegopt parameter

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_quality(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf", fmt="jpeg", jpegopt={"quality": 100}
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_quality: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_quality(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(), fmt="jpg", jpegopt={"quality": 100}
            )
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_with_quality: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_quality_and_progressive(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf",
            fmt="jpeg",
            jpegopt={"quality": 100, "progressive": True},
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_quality_and_progressive: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_quality_and_not_progressive(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf",
            fmt="jpeg",
            jpegopt={"quality": 100, "progressive": False},
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_quality_and_progressive: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_quality_and_progressive(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(),
                fmt="jpg",
                jpegopt={"quality": 100, "progressive": True},
            )
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_with_quality_and_progressive: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_quality_and_not_progressive(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            try:
                images_from_bytes = convert_from_bytes(
                    pdf_file.read(), fmt="jpg", jpegopt={"quality": 100}
                )
            except PDFInfoNotInstalledError:
                pass
        print(
            "test_conversion_from_bytes_with_quality_and_poppler_not_installed: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_quality_and_progressive_and_optimize(self):
        start_time = time.time()
        images_from_path = convert_from_path(
            "./tests/test.pdf",
            fmt="jpeg",
            jpegopt={"quality": 100, "progressive": True, "optimize": True},
        )
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_quality_and_progressive_and_optimize: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_quality_and_progressive_and_optimize(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(),
                fmt="jpg",
                jpegopt={"quality": 100, "progressive": True, "optimize": True},
            )
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_with_quality_and_progressive_and_optimize: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test size parameter

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_int_size(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", size=400)
        self.assertTrue(images_from_path[0].size[1] == 400)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_int_size: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_1d_tuple_size(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", size=(400,))
        self.assertTrue(images_from_path[0].size[1] == 400)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_1d_tuple_size: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_2d_tuple_size(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", size=(400, 400))
        self.assertTrue(images_from_path[0].size == (400, 400))
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_2d_tuple_size: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_invalid_size(self):
        start_time = time.time()
        try:
            images_from_path = convert_from_path("./tests/test.pdf", size="bad value")
            raise Exception("This should not happen")
        except ValueError:
            pass
        print(
            "test_conversion_from_path_with_invalid_size: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_2d_tuple_size_with_None_width(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", size=(None, 400))
        self.assertTrue(images_from_path[0].size[0] == 310)
        self.assertTrue(images_from_path[0].size[1] == 400)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_2d_tuple_size_with_None_width: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_2d_tuple_size_with_None_height(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", size=(400, None))
        self.assertTrue(images_from_path[0].size[0] == 400)
        self.assertTrue(images_from_path[0].size[1] == 518)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_2d_tuple_size_with_None_height: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test hide annotations parameter

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_hide_annotations(self):
        images_from_path = convert_from_path(
            "./tests/test_annotations.pdf", hide_annotations=True
        )
        start_time = time.time()
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_hide_annotations: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_hide_annotations(self):
        start_time = time.time()
        with open("./tests/test_annotations.pdf", "rb") as pdf_file:
            images_from_bytes = convert_from_bytes(
                pdf_file.read(),
                hide_annotations=True,
            )
            self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_with_hide_annotations: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_hide_annotations_with_invalid_arg_combination(
        self,
    ):
        start_time = time.time()
        try:
            images_from_path = convert_from_path(
                "./tests/test_annotations.pdf",
                hide_annotations=True,
                use_pdftocairo=True,
            )
            raise Exception("This should not happen")
        except NotImplementedError:
            pass
        print(
            "test_conversion_from_path_with_hide_annotations_with_invalid_arg_combination: {} sec".format(
                time.time() - start_time
            )
        )

    ## Test pdfinfo

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_path(self):
        start_time = time.time()
        info = pdfinfo_from_path("./tests/test.pdf")
        self.assertTrue(info.get("Pages", 0) == 1)
        print("test_pdfinfo_from_path: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_bytes(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as fh:
            info = pdfinfo_from_bytes(fh.read())
        self.assertTrue(info.get("Pages", 0) == 1)
        print("test_pdfinfo_from_bytes: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_path_241(self):
        start_time = time.time()
        info = pdfinfo_from_path("./tests/test_241.pdf")
        self.assertTrue(info.get("Pages", 0) == 241)
        print("test_pdfinfo_from_path_241: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_bytes_241(self):
        start_time = time.time()
        with open("./tests/test_241.pdf", "rb") as fh:
            info = pdfinfo_from_bytes(fh.read())
        self.assertTrue(info.get("Pages", 0) == 241)
        print("test_pdfinfo_from_bytes_241: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_path_invalid(self):
        start_time = time.time()
        try:
            info = pdfinfo_from_path("./tests/test.jpg")
            raise Exception("This should not happen")
        except PDFPageCountError:
            pass
        print("test_pdfinfo_from_path_241: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_from_bytes_invalid(self):
        start_time = time.time()
        try:
            with open("./tests/test.jpg", "rb") as fh:
                info = pdfinfo_from_bytes(fh.read())
            raise Exception("This should not happen")
        except PDFPageCountError:
            pass
        print("test_pdfinfo_from_path_241: {} sec".format(time.time() - start_time))

    # Test conversion with paths_only

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_using_dir_paths_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            images_from_path = convert_from_path(
                "./tests/test.pdf", output_folder=path, paths_only=True
            )
            self.assertTrue(len(images_from_path) == 1)
            self.assertTrue(type(images_from_path[0]) == str)
        print(
            "test_conversion_from_path_using_dir: {} sec".format(
                time.time() - start_time
            )
        )

    # Test for issue #125
    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed")
    def test_multithread_conversion(self):
        start_time = time.time()
        files = [
            "./tests/test.pdf",
        ] * 50
        with Pool(10) as p:
            res = p.map(convert_from_path, files)
        self.assertTrue(len(res) == 50)
        print("test_multithread_conversion: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_path_with_use_pdftocairo(self):
        start_time = time.time()
        images_from_path = convert_from_path("./tests/test.pdf", use_pdftocairo=True)
        self.assertTrue(len(images_from_path) == 1)
        print(
            "test_conversion_from_path_with_use_pdftocairo: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_conversion_from_bytes_with_use_pdftocairo(self):
        start_time = time.time()
        with open("./tests/test.pdf", "rb") as fh:
            images_from_bytes = convert_from_bytes(fh.read(), use_pdftocairo=True)
        self.assertTrue(len(images_from_bytes) == 1)
        print(
            "test_conversion_from_bytes_with_use_pdftocairo: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_rawdates(self):
        start_time = time.time()
        info = pdfinfo_from_path("./tests/test.pdf", rawdates=True)
        self.assertTrue("D:" in info["CreationDate"])
        print("test_pdfinfo_rawdates: {} sec".format(time.time() - start_time))

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_locked_pdf_with_userpw_only(self):
        start_time = time.time()
        with TemporaryDirectory() as path:
            with open("./tests/test_locked_user_only.pdf", "rb") as pdf_file:
                info = pdfinfo_from_bytes(pdf_file.read(), userpw="pdf2image")
                self.assertTrue("CreationDate" in info)
        print(
            "test_pdfinfo_locked_pdf_with_userpw_only: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    def test_convert_from_functions_same_number_of_parameters(self):
        start_time = time.time()
        self.assertEqual(
            len(signature(convert_from_path).parameters),
            len(signature(convert_from_bytes).parameters),
        )
        print(
            "test_convert_from_functions_same_number_of_parameters: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    def test_pdfinfo_functions_same_number_of_parameters(self):
        start_time = time.time()
        self.assertEqual(
            len(signature(pdfinfo_from_path).parameters),
            len(signature(pdfinfo_from_bytes).parameters),
        )
        print(
            "test_pdfinfo_functions_same_number_of_parameters: {} sec".format(
                time.time() - start_time
            )
        )

    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_timeout_pdfinfo_from_path_241(self):
        start_time = time.time()
        with self.assertRaises(PDFPopplerTimeoutError):
            info = pdfinfo_from_path("./tests/test_241.pdf", timeout=0.00001)
        print(
            "test_timeout_pdfinfo_from_path_241: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_timeout_convert_from_path_241(self):
        start_time = time.time()
        with self.assertRaises(PDFPopplerTimeoutError):
            imgs = convert_from_path("./tests/test_241.pdf", timeout=1)
        print(
            "test_timeout_convert_from_path_241: {} sec".format(
                time.time() - start_time
            )
        )

    @profile
    @unittest.skipIf(not POPPLER_INSTALLED, "Poppler is not installed!")
    def test_pdfinfo_first_and_last_page(self):
        start_time = time.time()
        info_first_path = pdfinfo_from_path("./tests/test_14.pdf", first_page=1, last_page=2)

        self.assertIn("Page    1 rot", info_first_path)

        print(
            "test_pdfinfo_first_and_last_page: {} sec".format(
                time.time() - start_time
            )
        )


if __name__ == "__main__":
    unittest.main()
