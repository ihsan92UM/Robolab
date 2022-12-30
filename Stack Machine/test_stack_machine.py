# !/usr/bin/env python3

import unittest
from stack_machine import *
import sys
import io
import unittest.mock
from enum import IntEnum
from aenum import  MultiValueEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
from math import factorial

class TestStackMachine(unittest.TestCase):
    def setUp(self):
        self.sm = StackMachine()
    def test_instance(self):
        self.assertIsInstance(self.sm, StackMachine)

    def test_do_chars_and_operand(self):
        self.assertEqual(self.sm.do((1,0,0,1,0,0)), ('A',SMState(1)),"Not Valid")    #add Char 'A' in stack , check machine state 'SMState.RUNNING : 1'
        self.assertEqual(self.sm.do((1,1,1,1,1,1)), SMState(-1),"Not Valid")        #add Invalid Char in Stack , check machine state 'SMState.ERROR : -1'
        self.assertEqual(self.sm.do((0,0,0,1,1,1)), (7,SMState(1)),"Not Valid")     #Input operand 7 in stack , check machine state 'SMState.RUNNING : 1'

    def test_do_all_Instructions(self):
        self.sm.do((0, 0, 1, 1, 0, 0)) #push 12
        self.sm.do((0, 0, 0, 0, 0, 0)) #push 0
        print(self.sm.check_stack())   # current stack = [12,0]

        self.assertEqual(self.sm.do((0,1,0,1,1,1)), SMState(-1),"Not Valid") #Div 
        print(self.sm.check_stack())     # current stack = [12,0]

        self.assertEqual(self.sm.do((0,1,0,0,0,1)), SMState(1),"Not Valid")  #Dup
        print(self.sm.check_stack())     # current stack = [12,0,0] 

        self.assertEqual(self.sm.do((0,1,0,0,0,0)), SMState(0),"Not Valid") #stp
        print(self.sm.check_stack())     # current stack = [12,0,0] 

        self.assertEqual(self.sm.do((0,1,0,0,1,0)), SMState(1),"Not Valid") #del
        print(self.sm.check_stack())     # current stack = [12,0] 
              
        self.assertEqual(self.sm.do((0,1,0,0,1,1)), SMState(1),"Not Valid") #swp
        print(self.sm.check_stack())    # current stack = [0,12]

        self.assertEqual(self.sm.do((0,1,0,1,0,0)), SMState(1),"Not Valid") #add
        print(self.sm.check_stack())    # current stack = [12]

        #Sub with 1 Operand = Error 
        self.assertEqual(self.sm.do((0,1,0,1,0,1)), SMState(-1),"Not Valid") #sub
        print(self.sm.check_stack())    # current stack = [12]

        #Sub with 2 Operand = return to stack
        self.sm.do((0, 0, 0, 1, 0, 1))  #push 5
        print(self.sm.check_stack())    # current stack = [12,5]                
        self.assertEqual(self.sm.do((0,1,0,1,0,1)), SMState(1),"Not Valid") #sub
        print(self.sm.check_stack())    # current stack = [7]

        self.sm.do((0, 0, 0, 0, 1, 1)) #push 3
        print(self.sm.check_stack())    # current stack = [7,3] 
        self.assertEqual(self.sm.do((0,1,0,1,1,0)), SMState(1),"Not Valid") #mul
        print(self.sm.check_stack())    # current stack = [21]

        self.sm.do((0, 0, 0, 1, 1, 0)) #push 6
        self.sm.do((0, 0, 0, 0, 1, 1)) #push 3
        self.sm.do((0, 0, 1, 0, 0, 0)) #push 8
        print(self.sm.check_stack())    # current stack = [21,6,3,8]

        self.assertEqual(self.sm.do((0,1,1,0,0,0)), SMState(1),"Not Valid") #exp
        print(self.sm.check_stack())    # current stack = [21,6,161]

        self.assertEqual(self.sm.do((0,1,1,0,0,1)), SMState(1),"Not Valid") #mod
        print(self.sm.check_stack())    # current stack = [21,6]

        self.assertEqual(self.sm.do((0,1,1,0,1,1)), SMState(1),"Not Valid") #shr
        print(self.sm.check_stack())    # current stack = [0]  

        #shl with one operand = Error   # current stack = [0]
        self.assertEqual(self.sm.do((0,1,1,0,1,0)), SMState(-1),"Not Valid") #shl

        self.sm.do((0, 0, 1, 0, 0, 0)) #push 8
        self.assertEqual(self.sm.do((0,1,1,0,1,0)), SMState(1),"Not Valid") #shl
        print(self.sm.check_stack())    # current stack = [0]  

        #hex with one operand/char = error
        self.assertEqual(self.sm.do((0,1,1,1,0,0)), SMState(-1),"Not Valid") #hex
        print(self.sm.check_stack())    # current stack = [0] 

        #hex with two operand/char 
        self.sm.do((1,0,0,1,0,0)) #push A 
        print(self.sm.check_stack())    # current stack = [0 , 'A'] 
        self.assertEqual(self.sm.do((0,1,1,1,0,0)), SMState(1),"Not Valid") #hex
        print(self.sm.check_stack())    # current stack = [0 , 'A' ,160] 

        self.assertEqual(self.sm.do((0,1,1,1,0,1)), SMState(1),"Not Valid") #fac
        print(self.sm.check_stack())    # current stack = [0 , 'A' ,0] 

        self.sm.do((0, 0, 1, 0, 0, 0)) #push 8
        print(self.sm.check_stack())    # current stack = [0 , 'A', 0 , 8] 
        self.assertEqual(self.sm.do((0,1,1,1,0,1)), SMState(1),"Not Valid") #fac
        print(self.sm.check_stack())    # current stack = [0 , 'A' ,0 , 128] 

        self.assertEqual(self.sm.do((0,1,1,1,1,0)), SMState(1),"Not Valid") #not
        print(self.sm.check_stack())    # current stack = [0 , 'A' ,0 , 127] 

        self.assertEqual(self.sm.do((0,1,1,1,1,1)), SMState(1),"Not Valid") #xor
        print(self.sm.check_stack())    # current stack = [0 , 'A' ,127] 


    
    def test_top_function(self): #test top function 
        self.sm.do((0, 0, 1, 1, 0, 0))      #push operand 12
        self.assertEqual(self.sm.top(),((0, 0, 0, 0, 1, 1, 0, 0)),"Not Valid") #check output 12 in binary 8bit format

    def test_do_speak(self):   #Speak
        self.instruction_sets = ((0,0,1,0,1,0),(0,1,0,0,0,1),(0,1,0,0,0,1),(0,1,0,1,1,0),(0,1,1,1,1,1),(0,0,0,1,0,0),(0,1,1,0,1,1),
                            (0,0,0,1,0,0),(0,1,1,0,0,1),(0,0,0,1,1,0),(0,1,1,0,0,0),(1,0,0,0,1,0),(1,1,0,1,1,0),(1,0,1,0,0,0),
                            (1,1,0,1,0,1),(0,0,0,1,0,1),(1,0,0,0,0,1),(0,1,0,0,0,0))

        for i in range (0,len(self.instruction_sets)):
            self.sm.do(self.instruction_sets[i])
        print('\n[Speak] ' + self.sm.top())

    def test_input_in_stack(self): #Individual Output
        self.sm.do((1,0,1,0,0,0))    #input E
        try:
            self.assertEqual(self.sm.to_terminal(),'E')
        except IndexError :
            print('\n[Input Error] No Operands/Characters in Stack!')


    # # Put this definition before your test function (annotation) and add a parameter
    # @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    # def test_func(self, mock_stdout):
    #     self.sm.do((0,0,1,0,1,0)) #Input in Stack 
    #     self.sm.check_stack()    #Supposed to print [10]     
    #     mock_stdout = io.StringIO()
    #     self.output = mock_stdout.getvalue()
    #     self.assertEqual(self.output , 10)

if __name__ == '__main__':
    unittest.main()


