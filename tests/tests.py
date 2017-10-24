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
        with open('./test.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 1)
        print('test_conversion_from_bytes: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_path(self):
        start_time = time.time()
        images_from_path = convert_from_path('./test.pdf')
        self.assertTrue(len(images_from_path) == 1)
        print('test_conversion_from_path: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_bytes_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./test.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 1)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_path_using_dir(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./test.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 1)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir: {} sec'.format(time.time() - start_time))

    @profile
    def test_conversion_from_bytes_14(self):
        start_time = time.time()
        with open('./test_14.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 14)
        print('test_conversion_from_bytes_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_14(self):
        start_time = time.time()
        images_from_path = convert_from_path('./test_14.pdf')
        self.assertTrue(len(images_from_path) == 14)
        print('test_conversion_from_path_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_bytes_using_dir_14(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./test_14.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 14)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    def test_conversion_from_path_using_dir_14(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./test_14.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 14)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_14: {} sec'.format((time.time() - start_time) / 14.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_241(self):
        start_time = time.time()
        with open('./test_241.pdf', 'rb') as pdf_file:
            images_from_bytes = convert_from_bytes(pdf_file.read())
            self.assertTrue(len(images_from_bytes) == 241)
        print('test_conversion_from_bytes_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_241(self):
        start_time = time.time()
        images_from_path = convert_from_path('./test_241.pdf')
        self.assertTrue(len(images_from_path) == 241)
        print('test_conversion_from_path_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_bytes_using_dir_241(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            with open('./test_241.pdf', 'rb') as pdf_file:
                images_from_bytes = convert_from_bytes(pdf_file.read(), output_folder=path)
                self.assertTrue(len(images_from_bytes) == 241)
                [im.close() for im in images_from_bytes]
        print('test_conversion_from_bytes_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    @unittest.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
    def test_conversion_from_path_using_dir_241(self):
        start_time = time.time()
        with tempfile.TemporaryDirectory() as path:
            images_from_path = convert_from_path('./test_241.pdf', output_folder=path)
            self.assertTrue(len(images_from_path) == 241)
            [im.close() for im in images_from_path]
        print('test_conversion_from_path_using_dir_241: {} sec'.format((time.time() - start_time) / 241.))

    @profile
    def test_empty_if_not_pdf(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./test.jpg')) == 0)
        print('test_empty_if_not_pdf: {} sec'.format(time.time() - start_time))

    @profile
    def test_empty_if_file_not_found(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./totally_a_real_file_in_folder.xyz')) == 0)
        print('test_empty_if_file_not_found: {} sec'.format(time.time() - start_time))

    @profile
    def test_empty_if_corrupted_pdf(self):
        start_time = time.time()
        self.assertTrue(len(convert_from_path('./test_corrupted.pdf')) == 0)
        print('test_empty_if_corrupted: {} sec'.format(time.time() - start_time))

if __name__=='__main__':
    unittest.main()
