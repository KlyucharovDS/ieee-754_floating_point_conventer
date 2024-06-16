# High Level Requirements

## Number range requirements

`requirements for computing equivalent class values`

1. The application shall receive and performed input numbers in range from -3.40282346639e+38 (min) to 3.40282346639e+38(max) inclusive (**equivalent class** or **range of acceptable values**). 

2. The least positive number that shall processed by the application is 1.40129846432e-45.
   
   Number format and processing are performed in accordance with the IEEE-754 standard.

3. The biggest negative number that shall processed by the application is -1.40129846432e-45. Number format and processing are performed in accordance with the IEEE-754 standard.

## Data type conversion

1. The application shall receive numbers in following data types:
   
   * integer (123456)
   
   * float point number (single and double precision) (1.123456789)
   
   * binary (0b0_01111111_00011111100110101101111 = 1.123456789)

2. The application shall transform received number to binary representation in string format.

3. The application shall transform received number to single precision number.

## Data conversion

1. The application shall data coverts to hex format.

2. The application shall perform following operations:
*  sum

* subtraction

* multiply

* division
  with float point numbers in the range of valid values.
3. The application shall modify some of 32 bit in the range of valid values.

4. The application shall perform increase or decrease received number (within the range of valid values) on any amount of the minimal value (equal to one bit).

5. The application shall display the accuracy conversion error (precision degradation) up or down (with the corresponding sign)

6. The application shall perform equal operations of two numbers in single precision type (IEEE-754).

7. The equal result shall have following items:
   
   - perform equal two numbers (<, ==, >)
   - difference between two numbers in single precision type format (IEEE-754).
   - difference between two numbers in double precision type format (IEEE-754).

## Behavior then input values are out of the range (non-condition)

1. If you enter numbers that are outside the acceptable values, the application converts the values of those numbers to the nearest acceptable number.
2. If conversion operation is performed  with outside a acceptable values result, the application shall convert the result to to the nearest acceptable number. Natural number shall be displayed to user.
3. The application shall display following error message when it receiving data with an unsupported data type: "ERROR! You are entering data in unsupported format.  The application accept data in integer, float point and binary format."    
