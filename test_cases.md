# Test Cases

## 1. Name

Verify data type conversion

### Description

Enter different data type of numbers and read output numbers in binary representation format and in single precision format. In case entering non-supporting data type numbers, the application print error message about this.

### Test Cases table for equivalent class values:

| Test Cases | Specification                                     | Expected result       |
| ---------- | ------------------------------------------------- | --------------------- |
| Case 01    | Entering an integer positive number: 12345        | binary: "0b"; single: |
| Case 02    | Entering an integer negative number: -7453        |                       |
| Case 03    | Entering an float point positive number: 12345.67 |                       |
| Case 04    | Entering an float point negative number: -7453.93 |                       |
| Case 05    | Entering an binary positive number: 0b0101_1010   |                       |
| Case 06    | Entering an binary negative number: 0b1000_1101   |                       |
| Case 07    | Entering an integer zero number                   |                       |

### Test Cases table for non-equivalent class values:

| Test Cases | Specification                                                    | Expected result |
| ---------- | ---------------------------------------------------------------- | --------------- |
| Case 01    | Entering the max positive integer number: 2147483647             |                 |
| Case 02    | Entering the max negative integer number: -2147483647            |                 |
| Case 03    | Entering the max positive float point number:                    |                 |
| Case 04    | Entering the max negative float point number:                    |                 |
| Case 05    | Entering the max positive binary representation  number(32 bit): |                 |
| Case 06    | Entering the max negative binary representation number(32 bit):  |                 |
| Case 07    | Entering an array                                                |                 |
| Case 08    |                                                                  |                 |

## N.Name:

### Description

### Test Cases table for equivalent class values

| Test Cases | Specification | Expected result |
| ---------- | ------------- | --------------- |
| Case 01    |               |                 |
| Case 02    |               |                 |
| Case 03    |               |                 |

### Test Cases table for non-equivalent class values:

| Test Cases | Specification | Expected result |
| ---------- | ------------- | --------------- |
| Case 01    |               |                 |
| Case 02    |               |                 |
| Case 03    |               |                 |

# Study

| #   | in value (dec) | in single | in binary | add min | sub  min | change bit to ... | out single | out binary | out hex | Note             |
|:---:|:--------------:| --------- | --------- | ------- | -------- | ----------------- | ---------- | ---------- | ------- | ---------------- |
| 1   | 1.0            |           |           |         |          |                   |            |            |         | equivalent range |
|     | -0.1234        |           |           |         |          |                   |            |            |         | equivalent range |
|     | 1e8            |           |           |         |          |                   |            |            |         | equivalent range |
|     | -4e12          |           |           |         |          |                   |            |            |         | equivalent range |
|     | 0              |           |           |         |          |                   |            |            |         | zero  bounds     |
|     | 0+little       |           |           |         |          |                   |            |            |         | near zero bounds |
|     | 0-little       |           |           |         |          |                   |            |            |         |                  |
|     | min + little   |           |           |         |          |                   |            |            |         |                  |
|     | max -little    |           |           |         |          |                   |            |            |         |                  |
|     | min            |           |           |         |          |                   |            |            |         |                  |
|     | max            |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |
|     |                |           |           |         |          |                   |            |            |         |                  |

# Test Cases

1. text

2. next