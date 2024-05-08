# Test Cases

## 1. Verify data type conversion

### Description

Enter different data type of numbers and read output numbers in binary representation format and in single precision format. In case entering non-supporting data type numbers, the application print error message about this.

### Test Cases table for equivalent class values:

| Test Cases | Specification                                                      | Expected result                                                                                                           |
| ---------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| Case 01    | Entering an integer positive number: 12345                         | **binary**: "0b01000110010000001110010000000000" **single**:12345 **Error due to conversion:** 0                          |
| Case 02    | Entering an integer negative number: -7453                         | **binary**: "0b11000101111010001110100000000000" **single**:-7453 **Error due to conversion:** 0                          |
| Case 03    | Entering an float point positive number: 12345.67                  | **binary**: "0b01000110010000001110011010101110" **single**:12345.669921875 **Error due to conversion:** -0.000078125     |
| Case 04    | Entering an float point negative number: -7453.93                  | **binary**: "0b11000101111010001110111101110001" **single**:-7453.93017578125 **Error due to conversion:** -0.00017578125 |
| Case 05    | Entering an binary positive number: 0b0101_1010                    | **binary**: "0b01000010101101000000000000000000" **single**:90 **Error due to conversion:** 0                             |
| Case 06    | Entering an binary negative number: 0b1000_1101 (Ones' complement) | **binary**: "0b11000010111000100000000000000000"  **single**:-113 **Error due to conversion:** 0                          |
| Case 07    | Entering an integer zero number                                    | **binary**: "0b0" **single**:0 **Error due to conversion:** 0                                                             |

### Test Cases table for non-equivalent class values:

| Test Cases | Specification                                                                                     | Expected result                                                                                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Case 01    | Entering the max positive integer number: 2147483647                                              | **binary**: "0b01001111000000000000000000000000" **single**:2147483648 **Error due to conversion:** 1                                                                                                          |
| Case 02    | Entering the max negative integer number: -2147483647                                             | **binary**: "0b11001111000000000000000000000000" **single**:-2147483648 **Error due to conversion:** -1                                                                                                        |
| Case 03    | Entering the max positive float point number:3.4028235e38                                         | **binary**: "0b01111111011111111111111111111111" **single**:3.402823466385288598117042E+38 **Error due to conversion:** 3361471140188295800000000000000                                                        |
| Case 04    | Entering the max negative float point number:-3.4028235e38                                        | **binary**: "0b11111111011111111111111111111111" **single**: -3.40282346638528859811704E+38  **Error due to conversion:** 3361471140188296000000000000000                                                      |
| Case 05    | Entering the max positive binary representation  number(32 bit):0b1111111111111111111111111111111 | **binary**: "0b01001111000000000000000000000000" **single**:2147483648 **Error due to conversion:** 1                                                                                                          |
| Case 06    | Entering the min negative binary representation number(32 bit):0b10000000000000000000000000000000 | **binary**: "0b11001111000000000000000000000000" **single**:-2147483648 **Error due to conversion:** -1                                                                                                        |
| Case 07    | Entering an array with a size of 5: [0,1,2,3,4]                                                   | **binary**: "0b0" **single**:0 **Error due to conversion:** 0. **Error message:** "ERROR! You are entering data in unsupported format. The application accept data in integer, float point and binary format." |
| Case 08    | Entering an array with a size of 1: [68]                                                          | **binary**: "0b0" **single**:0 **Error due to conversion:** 0 **Error message:** "ERROR! You are entering data in unsupported format. The application accept data in integer, float point and binary format."  |
| Case 09    | Entering a string with letters and numbers: 'abcdefg6Hq0'                                         | **binary**: "0b0" **single**:0 **Error due to conversion:** 0 **Error message:** "ERROR! You are entering data in unsupported format. The application accept data in integer, float point and binary format."  |