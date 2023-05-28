# !/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 0  # n
        self.data_bits = 0  # k
        self.parity_bits = 0  # r

        # Predefined non-systematic generator matrix G'
        gns = [[1,1,1,0,0,0,0,1,0,0],
               [0,1,0,0,1,0,0,1,0,0],
               [1,0,0,1,0,1,0,0,0,0],
               [0,0,0,1,0,0,1,1,0,0],
               [1,1,0,1,0,0,0,1,1,0],
               [1,0,0,1,0,0,0,1,0,1]]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List):

     g = gns                                                                                                    #final output

     for i in range (0, 10):
        g[2][i]=g[2][i]^g[0][i]
        g[4][i]=g[4][i]^g[0][i]
        g[5][i]=g[5][i]^g[0][i]

        g[0][i]=g[0][i]^g[1][i]
        g[2][i]=g[2][i]^g[1][i]
        g[5][i]=g[5][i]^g[1][i]

        g[0][i]=g[0][i]^g[2][i]
        g[4][i]=g[4][i]^g[2][i]
        g[5][i]=g[5][i]^g[2][i]

        g[0][i]=g[0][i]^g[3][i]
        g[2][i]=g[2][i]^g[3][i]

        g[1][i]=g[1][i]^g[4][i]
        g[2][i]=g[2][i]^g[4][i]

        g[0][i]=g[0][i]^g[5][i]
        g[1][i]=g[1][i]^g[5][i]
        g[4][i]=g[4][i]^g[5][i]
     return g                                                                                       #Return Z matrix

    def __derive_h(self, g: List):
        g_Data = []
        g_Parity = []

        for k in range(0,len(g)):
            g_Data.append(g[k][0:6])


        for j in range(0,len(g)):
            g_Parity.append(g[j][6:10])

        Transpose_g_Parity_Tuples= list(zip(*g_Parity))
        Transpose_g_Parity = [list(tup) for tup in Transpose_g_Parity_Tuples]

        tempSh=[]

        for m in range(0,len(Transpose_g_Parity)): 
            tempSh.append(Transpose_g_Parity[m]+ g_Data[m])

        h=tempSh                                                                            #final output

        for n in h:
            del n[-(len(g_Data)-len(Transpose_g_Parity)):]
        return h                                                                            # Return H matrix

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        sourceWord =[]
        sourceWord.append(list(source_word))
        def matrix_mul(a, b):
            return [[sum(i * j for i, j in zip(r, c)) for c in zip(*self.g)]
                for r in a]

    # Final output is in 2D Matrix format or <list> in a <list> 
        c = matrix_mul(sourceWord,self.g)
        # print(c)

    #Converting output in a single flat list
        flat_list = []
        for sublist in c:
            for item in sublist:
                flat_list.append(item)

    #taking modulus 2 of the output
        final_list = []
        for i in flat_list:
            final_list.append(i%2)
        # print('Final output without Even Parity')
        # print(final_list)

    # Procedure to add parity bit based on even or odd numbers of '1'
        odd = 0
        even = 0

        parity_list = final_list

        for j in range (len(parity_list)):
            if parity_list[j] % 2 == 0:
                even = even + 1
            else:
                odd = odd + 1
        if odd%2 == 0:
            parity_list.insert(len(parity_list),0)
        else:
            parity_list.insert(len(parity_list),1)

        # print('Our Final Output of encoded word with Even Parity')
        # print(parity_list)

        return tuple(parity_list)

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        encode = list(encoded_word)
        # print('Given Encode word : ',encode)

        ad_parity = encode.pop(-1) #Getting the last bit and removing
        # if ad_parity == 0:                                                     
        #     print('Additional parity :', ad_parity ,' or Even Parity.') #Return added P5 parity type
        # else:
        #     print('Additional parity :', ad_parity,' or Odd Parity.') #Return added P5 parity type

        # print('Given Encode word without Addditional Parity :',encode)
        temp_given_a= [encode[x:x+1] for x in range(0, len(encode))]                   # We need to multiply the a(10x1) matrix  with Sh(4x10) so converting a into sublist.

        def matrix_mul(a,b):                                                          #Matrix Mul Function
            return [[sum(i * j for i, j in zip(r, c)) for c in zip(*a)]
                for r in self.h]

        z = matrix_mul(temp_given_a,self.h)                                  # Final output is in 2D Matrix format or <list> in a <list> or Z syndrome matrix
        # print('Z Vector matrix : ',z)

    # find modulus of Z matrix

        flat_list = []
        for sublist in z:
            for item in sublist:
                flat_list.append(item)                                  #Converting Z vector output in a single flat list

        final_list = []
        for i in flat_list:
            final_list.append(i%2)                                       #taking modulus 2 of the Z vector matrix
        # print('Syndrome matrix : ' , final_list)

        columns = []  

        if final_list.count(final_list[0]) == len(final_list):          # if syndrome matrix all zero no error
            # print('No Error Occurred. ')
            # print('Decoded word : ',encode[:6])
            return(tuple(encode[:6]),HCResult.VALID)
        elif final_list.count(1) == 1:                                  # if syndrome matrix has single error
            # print('Single Error Occurred!!')
            i = 0                                                       # Comparing with H matrix column
            while i < len(self.h[0]):
                temp = []
                for row in self.h:
                    temp.append(row[i])
                i = i +1 
                columns.append(temp)

            if final_list in columns:
                # print('Match found in',columns.index(final_list)+1,'th columns of H matrix')       # Get the matching column number
                Cng_Bit = columns.index(final_list)
                if encode[Cng_Bit]==0:                                                               # Change the bit of decoded word at matched position
                    encode[Cng_Bit]=1
                else:
                    encode[Cng_Bit]=0
                # print('Corrected Code : ',encode)
                # print('Decoded word : ',encode[:6])
                return(tuple(encode[:6]),HCResult.CORRECTED)
            else:
                # print('No match found in H matrix')
                return(HCResult.UNCORRECTABLE)

        elif final_list.count(1) > 1:
            # print('Multiple Error Occurred!!!')
            if final_list in columns:
                # print('Match found in',columns.index(final_list),'th columns of H matrix')
                return(None,HCResult.UNCORRECTABLE)
            else:
                # print('Match not found in H matrix')
                return(None,HCResult.UNCORRECTABLE)



