import os
import sys
import tempfile
import unittest
import time

from memory_profiler import profile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf2image import convert_from_bytes, convert_from_path

class PDFConversionMethods(unittest.TestCase):
    @profile
    def test_conversion_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 1)
        print('test_conversion_from_bytes: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_path(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test.pdf')
        self.assertTrue(len(images_from_path) == 1)
        print('test_conversion_from_path: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_bytes_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_path_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_bytes_14(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 14)
        print('test_conversion_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_14(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf')
        self.assertTrue(len(images_from_path) == 14)
        print('test_conversion_from_path_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_bytes_using_dir_14(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_using_dir_14(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_241(self): # pragma: no cover
        start_time = time.time()
        with open('./tests/test_241.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 241)
        print('test_conversion_from_bytes_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_241(self): # pragma: no cover
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_241.pdf')
        self.assertTrue(len(images_from_path) == 241)
        print('test_conversion_from_path_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_using_dir_241(self): # pragma: no cover
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test_241.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_using_dir_241(self): # pragma: no cover
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_241.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    def test_empty_if_not_pdf(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./tests/test.jpg')) == 0)
        print('test_empty_if_not_pdf: {} sec'.format(time.time() - start_time))

    @profile
    def test_empty_if_file_not_found(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./tests/totally_a_real_file_in_folder.xyz')) == 0)
        print('test_empty_if_file_not_found: {} sec'.format(time.time() - start_time))

    @profile
    def test_empty_if_corrupted_pdf(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./tests/test_corrupted.pdf')) == 0)
        print('test_empty_if_corrupted_pdf: {} sec'.format(time.time() - start_time))

    ## Test first page

    @profile
    def test_conversion_from_bytes_14_first_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), first_page=12)
            self.assertTrue(len(images_from_bytes) == 3)
        print('test_conversion_from_bytes_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_14_first_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', first_page=12)
        self.assertTrue(len(images_from_path) == 3)
        print('test_conversion_from_path_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_bytes_using_dir_14_first_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, first_page=12)
                self.assertTrue(len(images_from_bytes) == 3)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_using_dir_14_first_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, first_page=12)
            self.assertTrue(len(images_from_path) == 3)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_first_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test last page

    @profile
    def test_conversion_from_bytes_14_last_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), last_page=12)
            self.assertTrue(len(images_from_bytes) == 12)
        print('test_conversion_from_bytes_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_14_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', last_page=12)
        self.assertTrue(len(images_from_path) == 12)
        print('test_conversion_from_path_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_bytes_using_dir_14_last_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, last_page=12)
                self.assertTrue(len(images_from_bytes) == 12)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_using_dir_14_last_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, last_page=12)
            self.assertTrue(len(images_from_path) == 12)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test first and last page

    @profile
    def test_conversion_from_bytes_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with open('./tests/test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), first_page=2, last_page=12)
            self.assertTrue(len(images_from_bytes) == 11)
        print('test_conversion_from_bytes_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_14_first_page_2_last_page_12(self):
        start_time = time.time()
        images_from_path = convert_from_path('./tests/test_14.pdf', first_page=2, last_page=12)
        self.assertTrue(len(images_from_path) == 11)
        print('test_conversion_from_path_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./tests/test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path, first_page=2, last_page=12)
                self.assertTrue(len(images_from_bytes) == 11)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_using_dir_14_first_page_2_last_page_12(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test_14.pdf', output_folder=path, first_page=2, last_page=12)
            self.assertTrue(len(images_from_path) == 11)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14_first_page_2_last_page_12: {} sec'.format((time.time() - start_time) / 14.))

    ## Test output as jpeg

    @profile
    def test_conversion_to_jpeg_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt='jpg')
            self.assertTrue(images_from_bytes[0].format == 'JPEG')
        print('test_conversion_to_jpeg_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_to_jpeg_from_path_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path, fmt='jpeg')
            self.assertTrue(images_from_path[0].format == 'JPEG')
            [im.close() for im in images_from_path]
        print('test_conversion_to_jpeg_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    ## Test output as png

    @profile
    def test_conversion_to_png_from_bytes(self):
        start_time = time.time()
        with open('./tests/test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read(), fmt='png')
            self.assertTrue(images_from_bytes[0].format == 'PNG')
        print('test_conversion_to_png_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_to_png_from_path_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./tests/test.pdf', output_folder=path, fmt='png')
            self.assertTrue(images_from_path[0].format == 'PNG')
            [im.close() for im in images_from_path]
        print('test_conversion_to_png_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

if __name__=='__main__':
    unittest.main()
