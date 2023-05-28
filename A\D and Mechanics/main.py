#!/usr/bin/env python3
from robot import *
from hamming_code import *
from stack_machine import *
from time import sleep

robot = Robot()  # initiate
hc = HammingCode()  # initiate
sm = StackMachine()  # initiate


def countdown(time_sec):
    print(' ')
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        time_format = '{:02d}'.format(secs)
        print(f'Insert new page in {time_format}', end='\r')
        sleep(1)
        time_sec -= 1
    print('                     \r')


def sensed_value() -> list:
    scanned_codewords: list = []
    count_to_11bits = 0
    first_bit = int(robot.read_value())  # read red value
    scanned_codewords.append(first_bit)  # append '0' for red

    while count_to_11bits < 11:
        robot.sensor_step()  # move one step to next bit
        sleep(0.5)
        value = robot.read_value()
        if value == '1':
            scanned_codewords.append(1)
        elif value == '0':
            scanned_codewords.append(0)
        count_to_11bits = count_to_11bits + 1
    robot.sensor_reset()  # after scanning 11bit , reset
    return scanned_codewords  # return 12bit value for further processing


def run():
    # the execution of all code shall be started from within this function
    try:
        page_counter = 1
        run_brick: bool = True

        while run_brick:

            if page_counter > 10:
                robot.text_to_speach('Insert the next page in 15 seconds.')
                countdown(15)
                print('Scanning next page. \n')
                robot.text_to_speach('Scan Starting.')
                page_counter = 1
            else:
                twelve_bit_read_value: list = sensed_value()  # transfer the 12bit scanned value
                twelve_bit_read_value.pop(0)  # removing the 'red' or first signed bit
                eleven_bits = tuple(twelve_bit_read_value)  # goes to hc
                print(' ')
                print(f'Scanned codes : {eleven_bits}')
                decoded_codeword = hc.decode(eleven_bits)  # ((1, 0, 1, 0, 1, 0), <HCResult.VALID: 'OK'>)
                print(f'Decoded : {decoded_codeword}')
                if decoded_codeword[1] == HCResult('ERROR'):
                    print('Uncorrectable code. Scanning again..')
                    robot.text_to_speach('Uncorrectable code. Scanning again.')
                    twelve_bit_read_value: list = sensed_value()  # transfer the 12bit scanned value
                    twelve_bit_read_value.pop(0)  # removing the 'red' or first signed bit
                    eleven_bits = tuple(twelve_bit_read_value)  # goes to hc
                    print(' ')
                    print(f'Scanned codes : {eleven_bits}')
                    decoded_codeword = hc.decode(eleven_bits)  # ((1, 0, 1, 0, 1, 0), <HCResult.VALID: 'OK'>)
                    print(f'Decoded : {decoded_codeword}')
                    if decoded_codeword[1] == HCResult('FIXED') or decoded_codeword[1] == HCResult('OK'):
                        opcodes = decoded_codeword[0]   # Goes to stack machine
                        smstate_tuple = sm.do(opcodes)  # output as a tuple :  ('[Operation]' , Smstate)
                        operation = smstate_tuple[0]
                        smstate = smstate_tuple[1]
                        if SMState(smstate).name == 'ERROR':
                            if operation == 'SPEAK':
                                print(f'Operation : {operation} , Invalid length.')
                                robot.text_to_speach('Invalid length')
                                print(SMState(smstate).name)
                            else:
                                print(f'Operation Error: {operation} , Not Enough Items.')
                                robot.text_to_speach('Not enough items. Programme stopping.')
                                print(f'Stack TOP : {sm.stack_top()}')
                                print(f'Stack : {sm.stack_check()}')
                                print(SMState(smstate).name)
                                run_brick = False
                        elif SMState(smstate).name == 'STOPPED':
                            print(f'Operation : {operation}')
                            print('Scanning Completed')
                            robot.text_to_speach('Scan Completed.')
                            print(f'Stack : {sm.stack_check()}')
                            print(SMState(smstate).name)
                            run_brick = False
                        else:
                            if opcodes[0] == 0 and opcodes[1] == 0:
                                print(f'Pushing : {operation}')
                                robot.text_to_speach(f'Pushing : {sm.stack_top()}')
                                print(f'Stack TOP : {sm.stack_top()}')
                                print(f'Stack : {sm.stack_check()}')
                                print(SMState(smstate).name)
                            elif opcodes[0] == 0 and opcodes[1] == 1:
                                print(f'Instruction : {operation}')
                                robot.text_to_speach(f'Implementing: {operation}')
                                print(f'Stack : {sm.stack_check()}')
                                print(SMState(smstate).name)
                            elif opcodes[0] == 1:
                                if operation == 'NOP':
                                    print(f'Command : {operation} , Continuing.')
                                    robot.text_to_speach('No operation. Continuing programme.')
                                    print(SMState(smstate).name)
                                elif operation == 'SPEAK':
                                    print(f'Command : {operation}')
                                    robot.text_to_speach(f'Implementing: {operation}')
                                    tts: str = sm.text_to_speach()
                                    robot.text_to_speach(tts)
                                    print(f'TTS : {sm.text_to_speach()}')  # Replace by robot speak
                                    print(f'Stack TOP : {sm.stack_top()}')
                                    print(f'Stack : {sm.stack_check()}')
                                    print(SMState(smstate).name)
                                else:
                                    print(f'Pushing : {operation}')
                                    robot.text_to_speach(f'Pushing : {sm.stack_top()}')
                                    print(f'Stack TOP : {sm.stack_top()}')
                                    print(f'Stack : {sm.stack_check()}')
                                    print(SMState(smstate).name)
                            else:
                                print('Programme Error')
                                robot.text_to_speach('Programme Error')
                                run_brick = False
                        page_counter = page_counter + 1
                        robot.scroll_step()

                    else:
                        print('Uncorrectable code. Scan aborted.')
                        robot.text_to_speach('Uncorrectable code. Scan aborted.')
                        run_brick = False

                elif decoded_codeword[1] == HCResult('OK') or decoded_codeword[1] == HCResult('FIXED'):
                    opcodes = decoded_codeword[0]  # Goes to stack machine
                    smstate_tuple = sm.do(opcodes)  # output as a tuple :  ('[Operation]' , State)
                    operation = smstate_tuple[0]
                    smstate = smstate_tuple[1]
                    if SMState(smstate).name == 'ERROR':
                        if operation == 'SPEAK':
                            print(f'Operation : {operation} , Invalid length.')
                            robot.text_to_speach('Invalid length')
                            print(SMState(smstate).name)
                        else:
                            print(f'Operation Error: {operation} , Not Enough Items.')
                            robot.text_to_speach('Not enough items. Programme stopping.')
                            print(f'Stack TOP : {sm.stack_top()}')
                            print(f'Stack : {sm.stack_check()}')
                            print(SMState(smstate).name)
                            run_brick = False
                    elif SMState(smstate).name == 'STOPPED':
                        print(f'Operation : {operation}')
                        print('Scanning Completed')
                        robot.text_to_speach('Scan Completed.')
                        print(f'Stack : {sm.stack_check()}')
                        print(SMState(smstate).name)
                        run_brick = False
                    else:
                        if opcodes[0] == 0 and opcodes[1] == 0:
                            print(f'Pushing : {operation}')
                            robot.text_to_speach(f'Pushing : {sm.stack_top()}')
                            print(f'Stack TOP : {sm.stack_top()}')
                            print(f'Stack : {sm.stack_check()}')
                            print(SMState(smstate).name)
                        elif opcodes[0] == 0 and opcodes[1] == 1:
                            print(f'Instruction : {operation}')
                            print(f'Stack : {sm.stack_check()}')
                            print(SMState(smstate).name)
                        elif opcodes[0] == 1:
                            if operation == 'NOP':
                                print(f'Command : {operation} , Continuing.')
                                robot.text_to_speach('No operation. Continuing programme.')
                                print(SMState(smstate).name)
                            elif operation == 'SPEAK':
                                print(f'Command : {operation}')
                                robot.text_to_speach(f'Implementing: {operation}')
                                tts: str = sm.text_to_speach()
                                robot.text_to_speach(tts)
                                print(f'TTS : {sm.text_to_speach()}')  # Replace by robot speak
                                print(f'Stack TOP : {sm.stack_top()}')
                                print(f'Stack : {sm.stack_check()}')
                                print(SMState(smstate).name)
                            else:
                                print(f'Pushing : {operation}')
                                robot.text_to_speach(f'Pushing : {sm.stack_top()}')
                                print(f'Stack TOP : {sm.stack_top()}')
                                print(f'Stack : {sm.stack_check()}')
                                print(SMState(smstate).name)
                        else:
                            print('Programme Error')
                            robot.text_to_speach('Programme Error')
                            run_brick = False
                    page_counter = page_counter + 1
                    robot.scroll_step()
                else:
                    print('Programme Error')
                    robot.text_to_speach('Programme Error')
                    run_brick = False

    except IndexError:  # ValueError AttributeError
        print('Invalid Length')
        robot.text_to_speach('Invalid Length')
        run_brick = False


if __name__ == '__main__':
    run()
