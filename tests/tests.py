import os
import sys
import unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pdf2image import convert_from_bytes, convert_from_path

class PDFConversionMethods(unittest.TestCase):
    def test_conversion_from_bytes(self):
        images_from_bytes = convert_from_bytes(open('./test.pdf', 'rb').read())
        self.assertTrue(len(images_from_bytes) == 1)

    def test_conversion_from_path(self):
        images_from_path = convert_from_path('./test.pdf')
        self.assertTrue(len(images_from_path) == 1)

    def test_empty_if_not_pdf(self):
        self.assertTrue(len(convert_from_path('./test.jpg')) == 0)

    def test_empty_if_file_not_found(self):
        self.assertTrue(len(convert_from_path('./totally_a_real_file_in_folder.xyz')) == 0)

    def test_empty_if_corrupted_pdf(self):
        self.assertTrue(len(convert_from_path('./test_corrupted.pdf')) == 0)
        
if __name__=='__main__':
    unittest.main()