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

if __name__=='__main__':
    unittest.main()