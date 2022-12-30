# !/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
from math import factorial

# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):

    RUNNING = 1
    STOPPED = 0
    ERROR = -1

class instructions(MultiValueEnum):
    #Instruction

    STP = '010000'  #done
    DUP = '010001'  #done
    DEL = '010010'  #done
    SWP = '010011'  #done
    ADD = '010100'  #done
    SUB = '010101'  #done
    MUL = '010110'  #done
    DIV = '010111'  #done
    EXP = '011000'  #done
    MOD = '011001'  #done
    SHR = '011011'  #done
    SHL = '011010'  #done    
    HEX = '011100'  #done
    FAC = '011101'  #done
    NOT = '011110'  #done
    XOR = '011111'  #done

    #Character

    NOP   = '100000','100011','111110'  #done
    SPEAK = '100001'    #done
    SPACE = '100010'    #done

    A = '100100'
    B = '100101'
    C = '100110'
    D = '100111'
    E = '101000'
    F = '101001'
    G = '101010'
    H = '101011'
    I = '101100'
    J = '101101'
    K = '101110'
    L = '101111'
    M = '110000'
    N = '110001'
    O = '110010'
    P = '110011'
    Q = '110100'
    R = '110101'
    S = '110110'
    T = '110111'
    U = '111000'
    V = '111001'
    W = '111010'
    X = '111011'
    Y = '111100'
    Z = '111101'



class StackMachine:          #change name to 'StackMachine' from 'stackMachine' to match with unit test

    def __init__(self) -> None:

        self.overflow = False
        self.data_fit_range = (0,255) #8bit range
        self.stack = []
        self.TTS=[]

    def do(self, code_word: Tuple[int, ...]) -> SMState:

        if code_word[0] == 0 and code_word[1]==0:
            x = list(map(str, code_word))
            x = "".join(x)
            result = int(x, 2)
            into8bit = c_ubyte(result)
            self.stack.append(into8bit.value)
            self.overflow == False
            # return (into8bit.value, SMState.RUNNING)
            return (self.stack[-1] , SMState.RUNNING)

        elif code_word[0] == 1:
            result = str(''.join(str(i) for i in code_word))
            if result in instructions._value2member_map_:
                inst_char = instructions(result).name
                match inst_char:
                    case 'NOP':
                        return SMState.STOPPED
                    case 'SPEAK':
                        if self.stack :
                            if isinstance(self.stack[-1],int):
                                if len(self.stack)>self.stack[-1]:
                                    first_item = self.stack.pop(-1)
                                    for i in range(1,first_item+1):
                                        self.TTS.append(self.stack[-i])
                                        popped_from_stack = ''.join(map(str, self.TTS))
                                    del self.stack[- first_item :]
                                    self.stack.append(popped_from_stack)  
                                else:
                                    return SMState.ERROR                  
                            else:
                                return SMState.ERROR              
                        else:
                            return SMState.ERROR
                            
                    case 'SPACE' :
                        self.stack.append(' ')
                        return (self.stack[-1], SMState.RUNNING)

                    case _:
                        self.stack.append(inst_char)
                        return (self.stack[-1], SMState.RUNNING)
            else:
                return SMState.ERROR  #check this again      



        elif code_word[0] == 0 and code_word[1]==1:

            inst_result = str(''.join(str(i) for i in code_word))
            inst_char = instructions(inst_result).name

            match inst_char:

                case 'MUL' :
                    if len(self.stack) >= 2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = (operand_2 * operand_1)
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if push_To_stack not in self.data_fit_range : self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR

                
                case 'STP' :
                    return SMState.STOPPED

                case 'DUP' :
                    if len(self.stack) >= 1:
                        item_dup = self.stack[-1]
                        self.stack.append(item_dup)
                        return SMState.RUNNING
                    else:
                        return SMState.ERROR

                case 'DEL' :
                    if len(self.stack) >= 1:
                        self.stack.pop(-1)
                        return SMState.RUNNING
                    else:
                        return SMState.ERROR

                case 'SWP' :
                    if len(self.stack) >= 2:
                        self.stack[-1] , self.stack[-2] = self.stack[-2] , self.stack[-1]
                        return SMState.RUNNING
                    else:
                        return SMState.ERROR
                
                case 'ADD' :
                    if len(self.stack) >= 2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = (operand_2 + operand_1)
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if push_To_stack not in self.data_fit_range : self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR


                case 'SUB' :
                    if len(self.stack) >= 2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = (operand_2 - operand_1)
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if push_To_stack not in self.data_fit_range : self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR

                case 'DIV' :                                                                       
                    if len(self.stack) >= 2:
                        if isinstance(self.stack[-1],int) and self.stack[-1] !=0 and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = int(operand_2//operand_1)
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR


                case 'EXP' :
                    if len(self.stack)>=2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = operand_2**operand_1
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if push_To_stack not in self.data_fit_range : self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR
                    
                case 'MOD' :
                    if len(self.stack)>=2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = operand_2%operand_1
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR
                  

                case 'SHL' :
                    if len(self.stack)>=2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = operand_2<<operand_1
                            toBin_operand_2 = bin(operand_2)            #check no of 1's in Ok-1
                            toBin_push_To_stack = bin(push_To_stack)    #check no of 1's after SHL
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if toBin_operand_2.count('1') != toBin_push_To_stack.count('1'): self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR 
                    else:
                        return SMState.ERROR
   
                case 'SHR' :
                    if len(self.stack)>=2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = operand_2>>operand_1
                            toBin_operand_2 = bin(operand_2)            #check no of 1's in Ok-1
                            toBin_push_To_stack = bin(push_To_stack)    #check no of 1's after SHL
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR 
                    else:
                        return SMState.ERROR
   

                case 'HEX' :
                    if len(self.stack)>=2:
                        operand_1 = self.stack[-1]   #ok
                        operand_2 = self.stack[-2]   #ok-1
                        hex_list = [0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F']
                        if operand_1 and operand_2 in hex_list:
                            hex_number = str(operand_1) + str(operand_2)
                            hex_to_Int = int(hex_number,16)
                            into8bit = c_ubyte(hex_to_Int)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR                   

                case 'FAC' :
                    if len(self.stack)>=1:
                        if isinstance(self.stack[-1],int):
                            operand_1 = self.stack.pop(-1)
                            push_To_stack = factorial(operand_1)
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            if push_To_stack not in self.data_fit_range : self.overflow = True
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR

                case 'NOT' :
                    if len(self.stack)>=1:
                        if isinstance(self.stack[-1],int):
                            operand_1 = self.stack.pop(-1)
                            push_To_stack = ~operand_1
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR

                case 'XOR' :
                    if len(self.stack)>=2:
                        if isinstance(self.stack[-1],int) and isinstance(self.stack[-2],int):
                            operand_1 = self.stack.pop(-1)
                            operand_2 = self.stack.pop(-1)
                            push_To_stack = operand_2^operand_1
                            into8bit = c_ubyte(push_To_stack)
                            self.stack.append(into8bit.value)
                            return SMState.RUNNING
                        else:
                            return SMState.ERROR
                    else:
                        return SMState.ERROR

        else :
            return SMState.ERROR
           



    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:

        if not self.stack: return None  #empty stack 

        elif isinstance(self.stack[-1],int):
            self.tobin = format(self.stack[-1],'08b')
            self.bin_tuple = tuple(int(i) for i in self.tobin)
            return self.bin_tuple       # binary tuple

        elif isinstance(self.stack[-1],str):
            return self.stack[-1]  #return strings

        else: return None         #any other conditions


    def to_terminal(self):
        return self.stack[-1]

    def check_stack(self):
        return self.stack
