#!/usr/bin/env python3

import io
import unittest.mock
from hamming_code import *
from stack_machine import *


class TestRobot(unittest.TestCase):
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_example(self, mock_stdout):
        """
            Example implementation of whole workflow:
                - Decode valid/correctable codes and
                - Execute the opcodes on the stack machine
                - Checking the final result afterwards
        """
        self.fail('implement me!')


if __name__ == '__main__':
    unittest.main()
