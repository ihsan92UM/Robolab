#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []
        self.rev = []
        self.tts = []

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        if code_word[0] == 0 and code_word[1] == 0:
            x = list(map(str, code_word))
            x = "".join(x)
            result = int(x, 2)
            into8bit = c_ubyte(result)
            self.stack.append(into8bit.value)
            return ('DECIMALS' , SMState.RUNNING)

        elif code_word == (0, 1, 0, 0, 0, 1):  # DUP
            if len(self.stack) < 1:
                return ('DUP', SMState.ERROR)
            else:
                ok = self.stack[len(self.stack) - 1]
                self.stack.append(ok)
            return ('DUP', SMState.RUNNING)

        elif code_word == (0, 1, 0, 1, 1, 0): #MUL
            if len(self.stack) < 2:
                return ('MUL', SMState.ERROR)
            else:
                ok_1 = self.stack.pop(len(self.stack) - 1)
                ok_2 = self.stack.pop(len(self.stack) - 1)
                res_1 = ok_1 * ok_2
                self.stack.append(res_1)
                if res_1 > 255:
                    self.overflow = True
                return ('MUL', SMState.RUNNING)

        elif code_word == (0, 1, 1, 1, 1, 1):  # XOR
            if len(self.stack) < 2:
                return  ('XOR', SMState.ERROR)
            else:
                ok_3 = self.stack.pop(len(self.stack) - 1)
                ok_4 = self.stack.pop(len(self.stack) - 1)
                res_2 = ok_3 ^ ok_4
                self.stack.append(res_2)
                if res_2 > 255:
                    self.overflow = True
                return ('XOR', SMState.RUNNING)

        elif code_word == (0, 1, 1, 0, 1, 1):
            if len(self.stack) < 2:
                return ('SHR', SMState.ERROR)
            else:
                ok_5 = self.stack.pop(len(self.stack) - 1)
                ok_6 = self.stack.pop(len(self.stack) - 1)
                res_3 = ok_6 >> ok_5
                self.stack.append(c_ubyte(res_3).value)
                if res_3 > 255:
                    self.overflow = True
                return ('SHR', SMState.RUNNING)

        elif code_word == (0, 1, 1, 0, 0, 1):  # MOD
            if len(self.stack) < 2:
                return ('MOD', SMState.ERROR)
            else:
                ok_7 = self.stack.pop(len(self.stack) - 1)
                ok_8 = self.stack.pop(len(self.stack) - 1)
                res_4 = (ok_8 % ok_7)
                self.stack.append(res_4)
                if res_4 > 255:
                    self.overflow = True
                return ('MOD', SMState.RUNNING)

        elif code_word == (0, 1, 1, 0, 0, 0):  # EXP
            if len(self.stack) < 2:
                return ('EXP', SMState.ERROR)
            else:
                ok_9 = self.stack.pop(len(self.stack) - 1)
                ok_10 = self.stack.pop(len(self.stack) - 1)
                res_5 = ok_10 ** ok_9
                self.stack.append(int(res_5))
                if res_5 > 255:
                    self.overflow = True
                return ('EXP', SMState.RUNNING)

        elif code_word == (0, 1, 0, 0, 1, 0): # DEL
            if len(self.stack) < 1:
                return ('DEL', SMState.ERROR)
            else:
                self.stack.pop(len(self.stack) - 1)
                return ('DEL', SMState.RUNNING)

        elif code_word == (0, 1, 0, 0, 1, 1): # SWP
            if len(self.stack) < 2:
                return ('SWP', SMState.ERROR)
            else:
                self.stack[-1] , self.stack[-2] = self.stack[-2] , self.stack[-1]                                                  # any other combo
                return ('SWP', SMState.RUNNING)

        elif code_word == (0, 1, 0, 1, 0, 0): #ADD
            if len(self.stack) < 2:
                return ('ADD', SMState.ERROR)
            else:
                ok_14 = self.stack.pop(len(self.stack) - 1)
                ok_15 = self.stack.pop(len(self.stack) - 1)
                res_6 = ok_14 + ok_15
                self.stack.append(res_6)
                if res_6 > 255:
                    self.overflow = True
                return ('ADD', SMState.RUNNING)

        elif code_word == (0, 1, 0, 1, 0, 1):  # SUB
            if len(self.stack) < 2:
                return ('SUB', SMState.ERROR)
            else:
                ok_16 = self.stack.pop(len(self.stack) - 1)
                ok_17 = self.stack.pop(len(self.stack) - 1)
                res_7 = ok_17 - ok_16
                self.stack.append(res_7)
                if res_7 > 255:
                    self.overflow = True
                return ('SUB', SMState.RUNNING)

        elif code_word == (0, 1, 0, 1, 1, 1):  # DIV
            if len(self.stack) < 2:
                return ('DIV', SMState.ERROR)
            else:
                ok_18 = self.stack.pop(len(self.stack) - 1)
                ok_19 = self.stack.pop(len(self.stack) - 1)
                res_8 = ok_19 / ok_18
                self.stack.append(int(res_8))
                if res_8 > 255:
                    self.overflow = True
                if ok_18 == 0:
                    return ('DIV', SMState.ERROR)
                else:
                    return  ('DIV', SMState.RUNNING)

        elif code_word == (0, 1, 1, 0, 1, 0): # SHL
            if len(self.stack) < 2:
                return ('SHL', SMState.ERROR)
            else:
                ok_20 = self.stack.pop(len(self.stack) - 1)
                ok_21 = self.stack.pop(len(self.stack) - 1)
                res_9 = ok_21 << ok_20
                self.stack.append(res_9)
                if res_9 > 255:
                    self.overflow = True
                return ('SHL', SMState.RUNNING)

        elif code_word == (0, 1, 1, 1, 0, 1):  # FAC
            if len(self.stack) < 1:
                return ('FAC', SMState.ERROR)
            else:
                ok_24 = self.stack.pop(len(self.stack) - 1)
                if ok_24 < 2:
                    self.stack.append(1)
                else:
                    for i in range(1, ok_24):
                        ok_24 = i * ok_24
                        self.stack.append(ok_24)
                        self.stack.append(ok_24)
                if ok_24 > 255:
                    self.overflow = True
                return ('FAC', SMState.RUNNING)

        elif code_word == (0, 1, 1, 1, 1, 0): # NOT
            if len(self.stack) < 1:
                return ('NOT', SMState.ERROR)
            else:
                ok_25 = self.stack.pop(len(self.stack) - 1)
                res_10 = ~ ok_25
                self.stack.append(c_ubyte(res_10).value)
                if res_10 > 255:
                    self.overflow = True
                return ('NOT', SMState.RUNNING)

        elif code_word == (0, 1, 1, 1, 0, 0):
            if len(self.stack) < 2:
                return ('HEX', SMState.ERROR)
            else:
                ok_26 = self.stack.pop(len(self.stack) - 1)
                ok_27 = self.stack.pop(len(self.stack) - 1)
                if ok_26 == 'A':
                    ok_26 = 10
                if ok_27 == 'A':
                    ok_27 = 10
                if ok_27 == 'B':
                    ok_27 = 11
                if ok_26 == 'B':
                    ok_26 = 11
                if ok_27 == 'C':
                    ok_27 = 12
                if ok_26 == 'C':
                    ok_26 = 12
                if ok_27 == 'D':
                    ok_27 = 13
                if ok_26 == 'D':
                    ok_26 = 13
                if ok_27 == 'E':
                    ok_27 = 14
                if ok_26 == 'E':
                    ok_26 = 14
                if ok_27 == 'F':
                    ok_27 = 15
                if ok_26 == 'F':
                    ok_26 = 15
                hex_int = ok_27 * 16 + ok_26 * 1
                self.stack.append(hex_int)
                if hex_int > 255:
                    self.overflow = True
                return ('HEX', SMState.RUNNING)

        elif code_word == (1, 0, 0, 0, 1, 0): # Space
            self.stack.append(' ')
            return ('SPACE', SMState.RUNNING)

        elif code_word == (1, 1, 1, 1, 1, 0):
            return ('NOP', SMState.RUNNING)

        elif code_word == (1, 1, 1, 1, 1, 1):
            return ('NOP', SMState.RUNNING)

        elif code_word == (1, 0, 0, 0, 0, 0):
            return ('NOP', SMState.RUNNING)

        elif code_word == (1, 0, 0, 0, 1, 1):
            return ('NOP', SMState.RUNNING)

        elif code_word == (1, 0, 0, 0, 0, 1):
            if self.stack:
                if isinstance(self.stack[-1], int):
                    if len(self.stack) > self.stack[-1]:
                        first_item = self.stack.pop(-1)
                        for i in range(1, first_item + 1):
                            self.tts.append(self.stack[-i])
                        del self.stack[- first_item:]
                        return ('SPEAK', SMState.RUNNING)
                    else:
                        print(f'[SPEAK ERROR] Given Value {self.stack[-1]} , Stack Length {len(self.stack)}')
                        return ('SPEAK', SMState.ERROR)
                else:
                    print('Last Item is not an Int')
                    return ('SPEAK', SMState.ERROR)
            else:
                print('Stack Empty')
                return ('SPEAK', SMState.ERROR)

        elif code_word == (0, 1, 0, 0, 0, 0):
            return ('STP', SMState.STOPPED)

        elif code_word[0] == 1:
            if code_word == (1, 0, 0, 1, 0, 0):
                self.stack.append('A')
            elif code_word == (1, 0, 0, 1, 0, 1):
                self.stack.append('B')
            elif code_word == (1, 0, 0, 1, 1, 0):
                self.stack.append('C')
            elif code_word == (1, 0, 0, 1, 1, 1):
                self.stack.append('D')
            elif code_word == (1, 0, 1, 0, 0, 0):
                self.stack.append('E')
            elif code_word == (1, 0, 1, 0, 0, 1):
                self.stack.append('F')
            elif code_word == (1, 0, 1, 0, 1, 0):
                self.stack.append('G')
            elif code_word == (1, 0, 1, 0, 1, 1):
                self.stack.append('H')
            elif code_word == (1, 0, 1, 1, 0, 0):
                self.stack.append('I')
            elif code_word == (1, 0, 1, 1, 0, 1):
                self.stack.append('J')
            elif code_word == (1, 0, 1, 1, 1, 0):
                self.stack.append('K')
            elif code_word == (1, 0, 1, 1, 1, 1):
                self.stack.append('L')
            elif code_word == (1, 1, 0, 0, 0, 0):
                self.stack.append('M')
            elif code_word == (1, 1, 0, 0, 0, 1):
                self.stack.append('N')
            elif code_word == (1, 1, 0, 0, 1, 0):
                self.stack.append('O')
            elif code_word == (1, 1, 0, 0, 1, 1):
                self.stack.append('P')
            elif code_word == (1, 1, 0, 1, 0, 0):
                self.stack.append('Q')
            elif code_word == (1, 1, 0, 1, 0, 1):
                self.stack.append('R')
            elif code_word == (1, 1, 0, 1, 1, 0):
                self.stack.append('S')
            elif code_word == (1, 1, 0, 1, 1, 1):
                self.stack.append('T')
            elif code_word == (1, 1, 1, 0, 0, 0):
                self.stack.append('U')
            elif code_word == (1, 1, 1, 0, 0, 1):
                self.stack.append('V')
            elif code_word == (1, 1, 1, 0, 1, 0):
                self.stack.append('W')
            elif code_word == (1, 1, 1, 0, 1, 1):
                self.stack.append('X')
            elif code_word == (1, 1, 1, 1, 0, 0):
                self.stack.append('Y')
            elif code_word == (1, 1, 1, 1, 0, 1):
                self.stack.append('Z')
            return ('CHARACTERS', SMState.RUNNING)

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION

        length = len(self.stack)
        if type(self.stack[length - 1]) == str:
            print(self.stack[length - 1])
            return self.stack[length - 1]
        elif type(self.stack[length - 1]) == int:
            rev = []
            x = self.stack[length - 1]
            while x > 0:
                bin_rem = x % 2
                rev.append(bin_rem)
                x = int(x / 2)
            print(type(rev))
            a = []
            if len(rev) < 8:
                while len(rev) < 8:
                    rev.append(0)
            for i in range(len(rev) - 1, -1, -1):
                a.append(rev[i])
            print(a)

            return tuple(a)

    def stack_top(self) -> Union[None, str, int]:
        if not self.stack:
            return 'Empty Stack'
        else:
            return self.stack[-1]

    def stack_check(self):
        return self.stack

    def text_to_speach(self):
        speach: str = ''.join(map(str, self.tts))
        return speach

