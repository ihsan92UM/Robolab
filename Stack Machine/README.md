# Hamming Code
## Requirements 
Python  3.9  <br />
``
To use Switch & Case feature instead of if else statement Python 3.10 is required. However, We need Python 3.9 to run Lego Brick for Assignment 5.
Switch & Case itself good for Assignment 4 but not for Assignment 5. So, i have added another file swapping switch & case to if else statements to suit Assignemnt 5.
``
## Dependencies 
Enum , Typing , ctypes , Math , Unittest <br />
## Environments 
[Sublime text 4](https://www.sublimetext.com/)  ,  [PyCharm Professional by JetBrains](https://www.jetbrains.com/pycharm) <br />

## Feedback 

Hello, 

looks good now, A4 is passed. But please have a look again on the 
overflow state, some tests are failing due to an incorrect overflow state. 

- ADD/FAC/MUL/SHL/XOR 
- SPEAK/T4: Stack should be empty after our sequence, found whole string 
(RES 64). We do not push anything for SPEAK. 
- Exceptions: For DIV/0, both operands should be popped and checked 
afterwards. Expected empty stack, found '0'. 


Best regards, 

Samuel Knobloch.

