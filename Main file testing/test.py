from hamming_code import *
from stack_machine import *

def main():
	hc = HammingCode()  # initiate
	sm = StackMachine()  # initiate

	checkredavailibility = 'Continue'
	codeword_list: list = []

	if checkredavailibility == 'Continue':  # checks for red

		# 12bit code =  readvalue()  # reads value

		# 11bit code = readvalue().pop(0)  # pops 1st red value		
		codeword: tuple = (1,0,1,0,0,0,1,1,1,1,1)

		# output = hc.decode(11bit code)  # hamming code processing
		output = hc.decode(codeword)

		print(output) 

		if output[1] == HCResult('ERROR'):
			print('UNCORRECTABLE')
			'''

			*** Note that, in case the result is UNCORRECTABLE, you need to re-read the line and decode it again! ***
			
			'''
			# sensor.reset()   # reset the sensor and start again
			# checkredavailibility = 'Continue'

			check_red_again = 'Continue'

			if check_red_again == 'Continue':  # checks for red agaim
				#readvalue()  # reads value again
				# 12bit code =  readvalue()  # reads value

				# 11bit code = readvalue().pop(0)  # pops 1st red value		
				codeword: tuple = (1,0,1,0,0,0,1,1,1,1,1)

				# output = hc.decode(11bit code)  # hamming code processing
				output = hc.decode(codeword)

				print(output) 

				if  output[1] == HCResult('ERROR'):
					print('UNCORRECTABLE')
					# sensor.reset()
					# run_brick = False
				if output[1] == HCResult('FIXED') or output[1] == HCResult('OK') :
					print('Corrected')
					# sensor.reset()
					opcodes: tuple = output[0]             # taking tuple(0) value from tuple ((1, 0, 1, 0, 0, 0), <HCResult.CORRECTED: 'FIXED'>)
														   # 00 operand , 01 instruction , 1 character
					smstate = sm.do(opcodes)
					if SMState(smstate).name == 'ERROR':
							print('error')
					else:
						if opcodes[0] == 0 and opcodes[1] == 0 :
							print(SMState(smstate).name)
							print(f'Pusing Operand : {sm.stack_top()}')
						elif opcodes[0] == 0 and opcodes[1] == 1:
							print(SMState(smstate).name)
							print(f'Instruction : {sm.stack_top()}')
						elif opcodes[0] == 1:
							print(SMState(smstate).name)
							print(f'Pusing Character : {sm.stack_top()}')
						else:
							print('error')

					# 1. at this point the codeword goes to stack machine
					# 2. Make sure to check the state after each opcode and abort everything if an exception occurs.
					# 3. print the instructuions ('XYZ')
					# 4. Print the top element of the stack if it has changed.
					# 5. Print (or use TTS) exception messages (e.g. not enough items, invalid range, …)

				else:
					# run_brick = False
					# sensor.reset()
					print('error')

		elif output[1] == HCResult('FIXED'):
			print(f'Fixed {output[0]}')
			opcodes: tuple = output[0]             # taking tuple(0) value from tuple ((1, 0, 1, 0, 0, 0), <HCResult.CORRECTED: 'FIXED'>)
			smstate = sm.do(opcodes)
			#print(SMState(smstate).name)
			if SMState(smstate).name == 'ERROR':
					print('error')
			else:
				if opcodes[0] == 0 and opcodes[1] == 0 :
					print(SMState(smstate).name)
					print(f'Pusing Operand : {sm.stack_top()}')
				elif opcodes[0] == 0 and opcodes[1] == 1:
					print(SMState(smstate).name)
					print(f'Instruction : {sm.stack_top()}')
				elif opcodes[0] == 1:
					print(SMState(smstate).name)
					print(f'Pusing Character : {sm.stack_top()}')
				else:
					print('error')

		else:
			print(f'OK {output[0]}')
			opcodes: tuple = output[0]             # taking tuple(0) value from tuple ((1, 0, 1, 0, 0, 0), <HCResult.CORRECTED: 'FIXED'>)
			smstate = sm.do(opcodes)
			if SMState(smstate).name == 'ERROR':
					print('error')
			else:
				if opcodes[0] == 0 and opcodes[1] == 0 :
					print(f'Pusing Operand : {sm.stack_top()}')
					print(SMState(smstate).name)
				elif opcodes[0] == 0 and opcodes[1] == 1:
					print(f'Instruction : {sm.stack_top()}')
					print(SMState(smstate).name)
				elif opcodes[0] == 1:
					print(f'Pusing Character : {sm.stack_top()}')
					print(SMState(smstate).name)
				else:
					print('error')


if __name__ == '__main__':
	main()