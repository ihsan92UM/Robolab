import unittest
from hamming_code import *
from typing import List, Tuple, Union


class TestHammingCode(unittest.TestCase):
    def setUp(self):
        self.code_test = HammingCode()

    def test_instance(self):
        self.assertIsInstance(self.code_test, HammingCode)

    def test_decode_valid(self):
        self.assertEqual(self.code_test.decode((0,0,0,0,0,0,0,0,0,0,1)), ((0,0,0,0,0,0), HCResult("OK")),"Not Valid")
        self.assertEqual(self.code_test.decode((1,0,1,1,0,1,1,1,1,0,1)),((1,0,1,1,0,1), HCResult("OK")),"Not Valid")

    def test_decode_corrected(self):
        self.assertEqual(self.code_test.decode((1,1,1,1,1,0,1,0,1,1,1)),((1,1,1,1,1,0), HCResult("FIXED")),"Errror can not be fixed")
        self.assertEqual(self.code_test.decode((0,0,1,0,1,0,1,0,1,1,1)),((0,0,1,0,1,0), HCResult("FIXED")),"Errror can not be fixed") #Additional test case for error corrected.

    def test_decode_uncorrectable(self):
        self.assertEqual(self.code_test.decode((0,0,1,0,1,1,1,1,1,1,0)),((None),HCResult("ERROR")),"Errror is Uncorrectable")
        self.assertEqual(self.code_test.decode((1,0,1,1,1,0,1,0,1,1,1)),((None),HCResult("ERROR")),"Errror is Uncorrectable")  #Additional test case for uncorrectable.
        


    def test_encode(self):
        encoded1 = self.code_test.encode((0,1,1,0,1,1))
        encoded2 = self.code_test.encode((0,0,0,0,0,0))
        encoded3 = self.code_test.encode((1,0,1,1,0,1))
        encoded4 = self.code_test.encode((1,1,1,1,1,0))
        self.assertEqual(encoded1, (0,1,1,0,1,1,1,1,1,1,0),"value does not match expectation")
        self.assertEqual(encoded2, (0,0,0,0,0,0,0,0,0,0,0),"value does not match expectation")
        self.assertEqual(encoded3, (1,0,1,1,0,1,1,1,1,0,1),"value does not match expectation")
        self.assertEqual(encoded4, (1,1,1,1,1,0,1,1,1,1,1),"value does not match expectation")



if __name__ == '__main__':
    unittest.main()

