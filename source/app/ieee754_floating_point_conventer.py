import math
import re
import struct

import numpy as np
from bitstring import BitArray
from numpy import double
from numpy import single

TRUE = true = True
FALSE = false = False


def format_real_num(num, precision):
    return '{:.{}g}'.format(num, precision)


# ----------------input block ---------------------
def check_format_non_binary(entered_value: str | single) -> tuple[bool, str]:
    """
    The function checks format entered entered_value on integer or single format
    (for example: 123, 123.456789, '0xABCDEF')
    @:param entered_value is string or numpy.float32 data type entered_value entered by a user
    :return: tuple[bool,str], where
        the second item is correct entered entered_value when first item is True,
        otherwise the second item is '' (empty string)
    """
    return_result = (False, '')
    result = re.findall(r'\b(\d+\.\d+|\d+|0[xX][0-9a-fA-F]+)\b', entered_value)
    if result:
        return_result = (True, result)
    return return_result


def check_binary_format(entered_value: str) -> tuple[bool, str]:
    """
    The function checks format entered entered_value on binary format
    (for example: '0b1_01001000_101000100000011000100001')
    :return: tuple[bool,str], where
        the second item is correct entered entered_value when first item is True,
        otherwise the second item is '' (empty string)
    """
    return_result = (False, '')
    result = re.findall(r'^0b{1}[01]{1}_{1}[01]{8}_{1}[01]{23}$', entered_value)
    if result:
        return_result = (True, result)
    return return_result


# -------------------------------------------------
def input_num(text: str) -> single:
    """

    :param text:
    :return:
    """
    return single(input(text))


class Bin2SingleConversion:
    # single
    __MIN_SINGLE = single(-3.40282346639e+38)
    __MAX_SINGLE = single(3.40282346639e+38)
    __MAX_NEGATIVE_SINGLE = single(-1.40129846432481707092373E-45)
    __MIN_POSITIVE_SINGLE = single(1.401298464324817070923730E-45)

    # binary
    __MIN_BINARY = '0b1_11111110_11111111111111111111111'
    __MAX_BINARY = '0b0_11111110_11111111111111111111111'
    __MAX_NEGATIVE_BINARY = '0b1_00000000_00000000000000000000001'
    __MIN_POSITIVE_BINARY = '0b0_00000000_00000000000000000000001'
    __ZERO_BINARY = '0b0_00000000_00000000000000000000000'

    def __init__(self, *, s_value=None, b_value=None):
        """
        Initializing of begin values
        :param s_value: the entered integer or float data type entered_value as the string type
        :param b_value: the entered binary entered_value as the string type (print view)
        """
        if s_value is not None and b_value is not None:
            s_value = None
            b_value = None
        if s_value is not None:
            self.__s_value = single(s_value)
            entered_value = str(self.__s_value)
            # check range
            check_value = self.__check_range_single(self.__s_value)
            self.__s_value = check_value[1]
            self.__print_message(check_value, entered_value)
            self.__conv2bin()
        elif b_value is not None and isinstance(b_value, str):
            # check range
            if b_value[0:1] == '0b':
                self.__b_value = self.__convert_to_normal_view(b_value)
            entered_value = self.__b_value
            check_value = self.__check_range_binary(self.__b_value)
            self.__b_value = check_value[1]
            self.__print_message(check_value, entered_value)
            self.__conv2single()
        else:
            self.__b_value = '0'
            self.__s_value = single(0)

    def __check_range_single(self, value) -> tuple[bool, str]:
        """
        Return a decision of the occurrence of a single number in the range.
        :return: tuple (bool_value, entered_value)
                    bool_value - True when single entered_value within range of acceptable values, otherwise False
                    entered_value - new single entered_value, when bool_value is False
        """

        bool_value = True
        single_value = value

        if not math.isclose(value, self.__MAX_SINGLE) and value > self.__MAX_SINGLE:
            single_value = self.__MAX_SINGLE
            bool_value = False
        elif not math.isclose(value, self.__MIN_SINGLE) and value < self.__MIN_SINGLE:
            single_value = self.__MIN_SINGLE
            bool_value = False
        # elif not isclose(entered_value, self.MAX_NEGATIVE_SINGLE,
        #                  rtol=self.MIN_POSITIVE_SINGLE,
        #                  atol=self.MIN_POSITIVE_SINGLE) and entered_value > self.MAX_NEGATIVE_SINGLE:
        #     entered_value = self.MAX_NEGATIVE_SINGLE
        #     bool_value = False
        # elif not math.isclose(entered_value, self.MIN_POSITIVE_SINGLE,
        #                       abs_tol=self.MIN_POSITIVE_SINGLE) and entered_value < self.MIN_POSITIVE_SINGLE:
        #     entered_value = self.MIN_POSITIVE_SINGLE
        #     bool_value = False
        return (bool_value, single_value)

    def __check_range_binary(self, value: str) -> tuple[bool, str]:
        """
        Return a decision of the occurrence of a binary number in the range
        :return: True when single entered_value within range of acceptable values, otherwise False
        """
        # entered_value = '0b0_11111110_11111111111111111111111' # max
        binary_value = value
        value = value[::-1]
        bool_value = True
        if len(value) == 32 + 2:
            # for the positive & the negative numbers
            if value[30:23] == '1111111':
                if value[23] == '1':
                    if value[31] == '0':
                        # more than the maximum
                        binary_value = self.__MAX_BINARY
                    else:
                        # less than the minimum
                        binary_value = self.__MIN_BINARY
                    bool_value = False
        else:
            binary_value = self.__ZERO_BINARY
            bool_value = False

        return bool_value, binary_value

    def __print_message(self, value: tuple[bool, str], entered_value: str) -> None:
        """
        The function receive entered_value as tuple[bool, str]
            1) if True then don't send error message, otherwise send the error message
            2) entered_value of checked parameter
        :return:
        """
        if value[0]:
            print(f'You enter numbers that are outside the acceptable values, '
                  f'the application converts entered entered_value ({entered_value}) '
                  f'to the the nearest acceptable number ({value[1]})')

    def __conv2bin(self) -> None:
        """
        Convert a number at the numpy.float32 datatype to number at the binary representation.
        :return:
        """
        # Преобразовать число float32 в его двоичное представление
        binary_representation = struct.pack('!f', self.__s_value)
        # Преобразовать байты в строку из нулей и единиц (бинарное представление)
        self.__b_value = ''.join(f'{byte:08b}' for byte in binary_representation)
        for _ in range(32 - len(self.__b_value)):
            self.__b_value = '0' + self.__b_value

    def __conv2single(self):
        # Преобразовать двоичную строку обратно в байты
        binary_bytes = bytes(int(self.__b_value[i:i + 8], 2) for i in range(0, len(self.__b_value), 8))
        # Преобразовать байты в число float32
        self.__s_value = single(struct.unpack('!f', binary_bytes)[0])

    def get_bin(self):
        return self.__convert_binary_to_print_view(self.__b_value)

    def get_single(self):
        return self.__s_value

    def chbit(self, nbit, value: bool):
        binary_representation = struct.pack('!f', self.__s_value)
        bit_array = BitArray(bytes=binary_representation)
        bit_array[nbit] = bool(value)
        modified_binary = bit_array.tobytes()
        self.__s_value = single(struct.unpack('!f', modified_binary)[0])
        self.__conv2bin()

    def ch_sign(self):
        pass

    def get_error_conversation(self):
        pass

    def add_min(self, loop=1):
        value = int(self.__b_value[1:32], base=2)
        sign = int(self.__b_value[0])
        # positive
        if sign == 0:
            if value <= 0x7F7FFFFF - loop:
                value += loop
        # negative
        else:
            # become 0
            if value == loop:
                sign = 0
            value -= loop
        value = bin(value)[2:32]
        for _ in range(31 - len(value)):
            value = '0' + value
        self.__b_value = bin(sign)[2] + value
        self.__conv2single()

    def sub_min(self, loop=1):
        value = int(self.__b_value[1:32], base=2)
        sign = int(self.__b_value[0])
        # positive
        if sign == 0:
            if value - loop < 0:
                sign = 1
                value = loop - value
            else:
                value -= loop
        # negative
        else:
            if value <= 0x7F7FFFFF - loop:
                value += loop
        value = bin(value)[2:32]
        for _ in range(31 - len(value)):
            value = '0' + value
        self.__b_value = bin(sign)[2] + value
        self.__conv2single()

    def __convert_to_normal_view(self, value) -> str:
        """
        Convert method from view(print view) with the delimiter of the prefix of a binary number (0b),sign(one number),
        exponent(8 numbers),significand precision to normal view
        Example:
            '0b0_00100101_00001000010011000110110'->'00010010100001000010011000110110'
        :param value: binary number of print view (0b0_00100101_00001000010011000110110)
        :return: normal view entered_value (00010010100001000010011000110110)
        """
        if len(value) == 36:
            value = value[:1:-1]
            value = value[0:23] + value[24:len(value) - 2] + value[len(value) - 1:len(value)]
            value = value[:1:-1]
        return value

    def __convert_binary_to_print_view(self, value) -> str:
        """
        Convert method from normal view to view(print view) with the delimiter of the prefix of a binary number
        (0b),sign(one number), exponent(8 numbers),significand precision
        Example:
            '00010010100001000010011000110110' -> '0b0_00100101_00001000010011000110110'
        :param value: binary number of normal view
        :return: print view entered_value ('0b0_00100101_00001000010011000110110')
        """
        if len(value) == 32:
            value = '0b' + value[0] + '_' + value[1:10] + '_' + value[10:32]
        return value


class ConversationStorage:
    """
    Stores an original and a converted value to analyze the conversion process.
    This class saves an original value and its converted version. It then
    automatically calculates error metrics like absolute error, relative
    error, and a flag to show if precision was lost.
    """

    def __init__(self, *, orig: str | single | int | double = None, converted: single = None):
        """
        Initializes the storage object.
        :param orig: The original value before conversion.
        :type orig: str | single | int | double | None
        :param converted: The value after conversion.
        :type converted: single | None
        """
        self.__ORIGINAL = 'original'
        self.__CONVERTED = 'converted'
        self.__ABSOLUTE_ERROR = 'absolute_error'
        self.__RELATIVE_ERROR = 'relative_error'
        self.__PRECISION_LOST = 'precision_lost'
        self.__value = {
            self.__ORIGINAL: None,
            self.__CONVERTED: None,
            self.__ABSOLUTE_ERROR: None,
            self.__RELATIVE_ERROR: None,
            self.__PRECISION_LOST: None
        }
        if orig is not None:
            self.set_original(orig)
        if converted is not None:
            self.set_converted(converted)

    def set_original(self, orig: str | single | int | double) -> None:
        """Sets the original value and recalculates errors.
        If the converted value is already set, this method will trigger
        a full recalculation of all error metrics.

        :param orig: The original value to store.
        :type orig: str | single | int | double
        :raises TypeError: If the provided value has an unsupported type.
        """
        if orig is not None and (
                isinstance(orig, str) or isinstance(orig, single) or isinstance(orig, int) or isinstance(orig, double)):
            self.__value[self.__ORIGINAL] = orig
            if self.__value[self.__CONVERTED] is not None:
                self.__calc_conversation_error()
        else:
            raise TypeError(f'"orig" parameter cannot be {type(orig)}')

    def get_original(self) -> str | single | int | double:
        """Returns the stored original value.
        :return: The current original value.
        :rtype: str | single | int | double
        """
        return self.__value[self.__ORIGINAL]

    def set_converted(self, converted: single | str):
        """Sets the converted value and recalculates errors.
        If the original value is already set, this method will trigger
        a full recalculation of all error metrics.

        :param converted: The converted value to store.
        :type converted: single or string
        :raises TypeError: If the provided value is not a `single` or 'str' type.
        """
        if isinstance(converted, (single, str)):
            self.__value[self.__CONVERTED] = converted
            if self.__value[self.__ORIGINAL] is not None:
                self.__calc_conversation_error()
        else:
            raise TypeError(f'"converted" parameter cannot be {type(converted)}')

    def get_converted(self) -> single:
        """Returns the stored converted value.

        :return: The current converted value.
        :rtype: single
        """
        return self.__value[self.__CONVERTED]

    def get_absolute_error(self) -> double:
        """"Returns the calculated absolute error.
        :return: The value of the absolute error.
        :rtype: double
        """
        return self.__value[self.__ABSOLUTE_ERROR]

    def get_relative_error(self) -> double:
        """Returns the calculated relative error.

        :return: The value of the relative error.
        :rtype: double
        """
        return self.__value[self.__RELATIVE_ERROR]

    def get_precision_lost(self) -> bool:
        """Returns a flag that shows if precision was lost.

        The flag is True if the original and converted values are not equal.

        :return: True if precision was lost, otherwise False.
        :rtype: bool
        """
        return self.__value[self.__PRECISION_LOST]

    def __calc_conversation_error(self) -> dict[str, any]:
        """Internal method to calculate all error metrics.
        This method uses the current original and converted values to
        calculate the errors and updates the internal state of the object.
        The calculation logic is different for numeric and non-numeric data.

        :return: The dictionary with updated property values.
        :rtype: dict[str, any]
        """
        if self.__value[self.__ORIGINAL] is not None and self.__value[self.__CONVERTED] is not None:
            if not (isinstance(self.__value[self.__ORIGINAL], str) or isinstance(self.__value[self.__CONVERTED], str)):
                orig = double(self.__value[self.__ORIGINAL])
                converted = double(self.__value[self.__CONVERTED])
                absolute_error = np.abs(double(orig - converted))
                if orig != 0:
                    relative_error = double(absolute_error / orig)
                else:
                    relative_error = 0
            else:
                orig = self.__value[self.__ORIGINAL]
                converted = self.__value[self.__CONVERTED]
                absolute_error = double(0)
                relative_error = double(0)

            self.__value[self.__ABSOLUTE_ERROR] = absolute_error
            self.__value[self.__RELATIVE_ERROR] = relative_error
            self.__value[self.__PRECISION_LOST] = orig != converted
        return self.__value

    def get_properties(self) -> dict[str, any]:
        """Returns a copy of the dictionary with all current data.

        Creates and returns a shallow copy of the internal dictionary. This
        dictionary contains the original value, the converted value, and all

        error metrics.
        :return: A copy of the properties dictionary.
        :rtype: {
            'original': str | int | single | double,
            'converted': single | str,
            'absolute_error': double,
            'relative_error': double,
            'precision_lost': bool
        }
        """
        return self.__value.copy()


class IEEE754Converter:
    # single
    __single_lim = numpy.finfo(single)
    MIN_SINGLE = single(__single_lim.min)
    MAX_SINGLE = single(__single_lim.max)
    MAX_NEGATIVE_SINGLE = single(-1.40129846432481707092373E-45)
    MIN_POSITIVE_SINGLE = single(1.401298464324817070923730E-45)

    # binary
    MIN_BINARY = '0b1_11111110_11111111111111111111111'
    MAX_BINARY = '0b0_11111110_11111111111111111111111'
    MAX_NEGATIVE_BINARY = '0b1_00000000_00000000000000000000001'
    MIN_POSITIVE_BINARY = '0b0_00000000_00000000000000000000001'
    ZERO_BINARY = '0b0_00000000_00000000000000000000000'
    NEGATIVE_ZERO_BINARY = '1b0_00000000_00000000000000000000000'

    # integer 32 bit
    __int_lim = numpy.iinfo(int32)
    MAX_INTEGER = __int_lim.max
    MIN_INTEGER = __int_lim.min

    # double
    __double_lim = numpy.finfo(double)
    MAX_DOUBLE = __double_lim.max
    MIN_DOUBLE = __double_lim.min

    def __init__(self, *, value: str | int | single | double = None):
        """
        Initializing of begin values
        :param value: the entered integer, single or float64, integer, string data type
        """
        self._single = ConversationStorage()
        self._binary = ConversationStorage()
        self._double = ConversationStorage()
        self._integer = ConversationStorage()
        if value is not None:
            self.set_value(value)
        else:
            raise TypeError(f'Please use the supported data types instead {type(value)}')



    @staticmethod
    def _check_binary(entered_value: str) -> tuple[bool, str]:
        """Validates a string for a normal float32 binary representation.

        This function checks if the input string adheres to the specific binary format
        '0b<S>_<EEEEEEEE>_<MMMMMMMMMMMMMMMMMMMMMMM>', where
            S is the sign bit,
            E is the 8-bit exponent,
            M is the 23-bit mantissa.
        It performs two levels of validation:
        1.  **Format Check:** Ensures the string matches the required pattern.
        2.  **Value Check:** Rejects valid IEEE 754 special values such as
                - Infinity (inf)
                - Not a Number (NaN)
                - Negative Zero (-0.0).

        :param
            entered_value (str): The string to be validated.

        :return
            tuple[bool, str]: A tuple where the first element is a boolean
            indicating success, and the second is a string.
            - (True, entered_value): If the string is valid and represents a
              normal, non-special number.
            - (False, '0b0_00000000_00000000000000000000001'): If the input is
              not a string, the format is incorrect, or it represents a
              special entered_value (inf, NaN).
        """
        return_result = (False, '0b0_00000000_00000000000000000000001')
        if not isinstance(entered_value, str):
            return return_result
        result = re.findall(r'^0b{1}[01]{1}_{1}[01]{8}_{1}[01]{23}$', entered_value)
        if result:
            # Checking the entered entered_value for inf
            if entered_value[4:12] == '11111111' and entered_value[13:31] == '0' * 23:
                return return_result
            # Checking the entered entered_value for Nan
            elif entered_value[4:12] == '11111111' and entered_value[13:31] != '0' * 23:
                return return_result
            # Checking the entered entered_value for -0.0
            elif entered_value == NEGATIVE_ZERO_BINARY:
                return_result = (True, '0b0_00000000_00000000000000000000000')
                return return_result
            else:
                return_result = (True, entered_value)
                return return_result
        else:
            return return_result

    @staticmethod
    def _check_single(entered_value) -> tuple[bool, single]:
        """
            Checks an input value and determines if it is a valid single (float32) number.

            This function handles special IEEE 754 values, such as NaN, infinity,
            negative zero (-0.0), and subnormal numbers, as well as incorrect data types.

            :param entered_value: The input value, which can be of any numeric type (e.g., string, int, float).
            :return: A tuple (is_valid, corrected_value).
                     - is_valid (bool): `True` if the `value` is a valid number within the
                                        acceptable range. Otherwise, `False`.
                     - corrected_value (single): The original `value` if it is valid.
                                                    Otherwise, a corrected value:
                                                    - `0.0` for NaN, -0.0, subnormal numbers, or
                                                      incorrect data types.
                                                    - `np.finfo(np.single).max` for +Infinity.
                                                    - `np.finfo(np.single).min` for -Infinity.
            """

        return_val = (True, single(0))
        single_info = np.finfo(np.single)

        try:
            # Trying to convert to single data type
            entered_value = np.single(entered_value)
        except (ValueError, TypeError):
            # If convertion is failed (for example entered_value - строка "Hello")
            return False, np.single(0)

        # Checking the entered entered_value for Nan
        if np.isnan(entered_value):
            return_val = (False, single(0))
        # Checking the entered entered_value for infinity
        elif np.isinf(entered_value):
            if entered_value > 0:
                return_val = (False, single_info.max)
            elif entered_value < 0:
                return_val = (False, single_info.min)
        # Checking the entered entered_value for -0.0
        elif 1 / entered_value == -np.inf:
            return_val = (False, single(0))
        # Checking the entered entered_value for -tiny...0.0....tiny
        elif single_info.smallest_subnormal > entered_value or -single_info.smallest_subnormal < entered_value:
            return_val = (False, single(0))
        else:
            return_val = (True, entered_value)
        return return_val

    @staticmethod
    def _check_range_integer(entered_value: int) -> tuple[bool, int]:
        """Checks if an integer is within the valid numpy.int32 range.

        This method verifies if the provided integer value fits within the
        minimum and maximum bounds of a 32-bit signed integer. It also
        handles cases where the input is not of type int.

        :param
            entered_value (int): The integer to validate.

        :return
            tuple[bool, int]: A tuple containing a boolean flag and an integer.
            - (True, entered_value): If the number is within the int32 range.
            - (False, clamped_value): If the number is out of range, where
              clamped_value is the corresponding int32 minimum or maximum.
            - (False, 0): If the input `entered_value` is not an integer.
        """
        return_value = (False, 0)
        if not isinstance(entered_value, int):
            return return_value
        imax = np.iinfo(np.int32).max
        imin = np.iinfo(np.int32).min
        if entered_value < imin:
            return False, imin
        elif entered_value > imax:
            return False, imax
        return True, entered_value

    @staticmethod
    def _check_range_double(entered_value: double) -> tuple[bool, double]:
        """
            Validates if a value can be represented as a normal float32 number.

            This function performs several checks to determine if the input value is
            a "normal" number that can be safely represented as a single-precision
            float (numpy.float32). It specifically rejects special and edge-case
            values like NaN, negative zero, and subnormals, and checks for overflow.

            :param entered_value:
                The input value to validate, which must be of NumPy.double data ype.
            :return:
                tuple[bool, float]: A tuple containing a validation flag and a number.
                - (True, value): If the input is a valid, normal, and convertible number.
                - (False, 0.0): If the input cannot be converted to a float, or if
                  it is NaN, negative zero, or a subnormal number.
                - (False, clamped_value): If the input would overflow, this returns
                  the maximum or minimum representable float32 value.
        """
        return_val = (True, double(0))
        single_info = np.finfo(np.single)

        try:
            # Trying to convert to single data type
            entered_value = double(entered_value)
        except (ValueError, TypeError):
            # If convertion is failed (for example entered_value - строка "Hello")
            return False, double(0)

        # Checking the entered entered_value for Nan
        if np.isnan(entered_value):
            return_val = (False, double(0))
        # Checking the entered entered_value for infinity
        elif np.isinf(single(entered_value)):
            if entered_value > 0:
                return_val = (False, double(single_info.max))
            elif entered_value < 0:
                return_val = (False, double(single_info.min))
        # Checking the entered entered_value for -0.0
        elif 1 / entered_value == -np.inf:
            return_val = (False, double(0))
        # Checking the entered entered_value for -tiny...0.0....tiny
        elif single_info.smallest_subnormal > entered_value or -single_info.smallest_subnormal < entered_value:
            return_val = (False, double(0))
        else:
            return_val = (True, entered_value)
        return return_val

    def _check_and_print_error_message(self, value: tuple[bool, str], entered_value: str) -> None:
        """
        The function receive entered_value as tuple[bool, str]
            1) if True then don't send error message, otherwise send the error message
            2) entered_value of checked parameter
        :return:
        """
        if value[0]:
            print(f'You enter numbers that are outside the acceptable values, '
                  f'the application converts entered entered_value ({entered_value}) '
                  f'to the the nearest acceptable number ({value[1]})')

    def get_value(self, datatype: type) -> single | double | int | str | None:
        """Gets the stored value converted to a specified data type.

        This method accesses the internal value and returns it cast to the
        requested type.

        :param datatype: The target type for the value. Supported types are
                         `numpy.single`, `numpy.double`, `int`, `str` (for binary
                         string), and `bool` (for binary string).
        :return: The value in the specified type, or None for an unsupported type.
        :rtype: single | double | int | str | None
         :raises TypeError: If the provided datatype is not the supported types.
        """
        if datatype is single:
            return self.single
        elif datatype is double:
            return self.double
        elif datatype is int:
            return self.int
        elif datatype is str:
            return self.string
        elif datatype is bool:
            return self.binary
        else:
            raise TypeError(
                f'Please enter supported types as like as: single, double, int, str. Instead {type(datatype)}')

    def set_value(self, value: single | double | int | str):
        # check range of the entered value
        check_value = (False, 0)
        # single
        if isinstance(value, single):
            check_value = self._check_single(value)
            if check_value[0]:
                self.__single_value = check_value[1]
            else:
                self.__single_value = single(0)
        # double
        elif isinstance(value, double):
            check_value = self._check_range_double(value)
            if check_value[0]:
                self.__single_value = single(check_value[1])
            else:
                self.__single_value = single(0)
        # integer
        elif isinstance(value, int):
            check_value = self._check_range_integer(value)
            # @ todo TBD
        # binary, string
        elif isinstance(value, str):
            check_value = self._check_binary(value)
            # @ todo TBD

    @property
    def single(self) -> single:
        return self._single.get_converted()

    @single.setter
    def single(self, value: single) -> None:
        if isinstance(value, single):
            check_value = self._check_single(value)
            if check_value[0]:
                self._single.set_original(value)
                self._single.set_converted(single(check_value[1]))

    @property
    def double(self) -> double:
        return self._double.get_original()

    @double.setter
    def double(self, value: double) -> None:
        res = self._check_range_double(value)
        if res or (not res and res[1] != double(0)):
            res = res[1]
        # breaking job because entered value is not convertible
        else:
            raise ValueError(f'Entered value is not convertible: {value}')
            return
        # conversation
        self.__single_value = single(res)
        self._double.calc_conversation_error(orig=res, converted=self.__single_value)

    def double_conversation_error(self) -> dict:
        return double(self._double.get_properties())

    @property
    def string(self) -> str:
        return self.__single_to_binary(self.__single_value)

    @string.setter
    def string(self, value: str) -> None:
        res = self._check_binary(value)
        if res:
            self.__single_value = self.__binary_to_single(res[1])

    @property
    def integer(self) -> int:
        return int(self._integer.get_properties())

    @integer.setter
    def integer(self, value: int) -> None:
        pass

    def integer_conversation_error(self) -> double:
        return double(self._integer)

    @property
    def binary(self) -> str:
        return ''

    @binary.setter
    def binary(self, value: bin) -> None:
        pass

    def __single_to_binary(self, value: single) -> str:
        """
        Преобразует число np.float32 в его 32-битное двоичное представление.
        """
        # 1. Используем struct для получения 4-байтового бинарного представления числа.
        # 'f' означает float, '<' означает little-endian (порядок байтов).
        # Для numpy float32, обычно используются системные байты, но 'f' в struct всегда 4 байта.
        # Обычно, Python на большинстве систем хранит float32 как little-endian.
        binary_bytes = struct.pack('<f', value)

        # 2. Преобразуем байты в строку двоичных цифр.
        # Каждый байт (8 бит) будет представлен в виде двух шестнадцатеричных символов.
        # Затем преобразуем каждый hex-символ в его 4-битное двоичное представление.
        # Мы хотим получить 32 бита, поэтому форматируем каждый байт как 8-битное двоичное число.
        # И объединяем их.

        # Пример: b'\x00\x00\x80?' для 1.0 (little-endian)
        # \x00 -> 00000000
        # \x00 -> 00000000
        # \x80 -> 10000000
        # \x3f -> 00111111
        # Последовательность бит будет 00111111100000000000000000000000 (читается в обратном порядке из-за little-endian)
        # Или, если struct.pack читает как big-endian (что для 'f' зависит от системы), то это будет проще.
        # Проверим, какой порядок байтов:
        # 1.0 в big-endian: 0 01111111 00000000000000000000000 (0x3F800000)
        # 1.0 в little-endian: 0x0000803F

        # Чтобы получить правильный порядок бит, нужно сначала преобразовать в int, а затем в бинарную строку.
        # Используем unpack для получения int из байтов.
        integer_representation = struct.unpack('<I', binary_bytes)[0]  # '<I' для unsigned int little-endian

        # Преобразуем int в 32-битную бинарную строку с нулями в начале
        binary_string = bin(integer_representation)[2:].zfill(32)
        return binary_string

    def __binary_to_single(self, binary_string: str) -> single:
        """
        Преобразует 32-битную двоичную строку в число np.float32.
        """
        if len(binary_string) != 32 or not all(bit in '01' for bit in binary_string):
            raise ValueError("Двоичная строка должна быть длиной 32 символа и содержать только '0' или '1'.")

        # 1. Преобразуем бинарную строку обратно в целое число
        integer_representation = int(binary_string, 2)

        # 2. Используем struct для упаковки целого числа в 4 байта и затем распаковки как float.
        # '<I' означает unsigned int little-endian, '<f' означает float little-endian.
        float_value = struct.unpack('<f', struct.pack('<I', integer_representation))[0]
        return np.float32(float_value)

    def __modify_bit_and_convert(self, original_value: single, bit_index: int, new_bit_value: str) -> np.float32:
        """
        Модифицирует конкретный бит в бинарном представлении числа float32
        и возвращает новое число float32.

        Args:
            original_value (np.float32): Исходное число.
            bit_index (int): Индекс бита для изменения (0-31, 0 - младший бит, 31 - старший бит).
            new_bit_value (str): Новое значение бита ('0' или '1').

        Returns:
            np.float32: Новое число с модифицированным битом.
        """
        if new_bit_value not in ('0', '1'):
            raise ValueError("Новое значение бита должно быть '0' или '1'.")
        if not (0 <= bit_index <= 31):
            raise ValueError("Индекс бита должен быть в диапазоне от 0 до 31.")

        # Получаем бинарное представление
        binary_str = float32_to_binary_representation(original_value)

        # Преобразуем строку в список символов для изменения
        binary_list = list(binary_str)

        # Индекс 0 в строке - это старший бит (знак), индекс 31 - младший бит.
        # Соответственно, для изменения по индексу (0-31), нужно инвертировать:
        # bit_index = 0  -> senior bit (sign)
        # bit_index = 31 -> least significant bit (mantissa)
        # Если мы хотим менять по порядку от знакового бита до младшего бита мантиссы:
        # index 0  -> sign bit
        # index 1-8 -> exponent bits
        # index 9-31 -> mantissa bits

        # Корректируем индекс, чтобы он соответствовал позиции в строке
        # (0 - старший бит, 31 - младший бит в Python строке)
        # Т.е. если bit_index=0, меняем первый символ, если bit_index=31, меняем последний.
        binary_list[bit_index] = new_bit_value

        # Собираем новую бинарную строку
        modified_binary_str = "".join(binary_list)

        # Преобразуем обратно в float32
        modified_float = self.binary_representation_to_float32(modified_binary_str)
        return modified_float

    def sub_mins(self, counts: int = 1) -> single:
        return single(0)

    def add_mins(self, counts: int = 1) -> single:
        return single(0)

    def multiply(self, value: single | int | double | bin) -> single:
        return single(0)

    def devide(self, value: single | int | double | bin) -> single:
        return single(0)

    def get_accurancy_conversation(self, dtype: str) -> {}:
        """
        :param: dtype can be 'int','integer', 'double' in string format
        :return: Function returns this form dictionary:
            'absolute_error': |original - converted|,
            'relative_error': |original - converted| / |original|,
            'precision_lost': True or False
        """
        if isinstance(dtype, str):
            if dtype == 'int' or dtype == 'integer':
                return self._integer.value()
            elif dtype == 'double':
                return self._double.value()
            else:
                temp = ConversationStorage()
                return temp.calc_conversation_error(orig=0, converted=single(0))


class CompareSingle:

    def __init__(self, *, value: str | int | single | double, abs_tol: double = None, rel_tol: double = None):
        # need to use IEEE754Converter object
        self.__value = value

        if abs_tol is None:
            self.__abs_tol = double(IEEE754Converter.MIN_POSITIVE_SINGLE)

        if abs_tol is None:
            self.__rel_tol = double(IEEE754Converter.MIN_POSITIVE_SINGLE)

    def cmp(self, value: single | int | double | bin) -> int:
        """
        Compare inner entered_value to entrance entered_value using
        absolute and relation tollerance
        :param self:
        :param value:
        :return:
            0 - if two numbers are -equal
            1 - if inner entered_value is more then parameter entered_value
            -1 - if inner entered_value is less then parameter entered_value
        """
        return int(0)

    @property
    def abs_tol(self) -> double:
        return self.__abs_tol

    @abs_tol.setter
    def abs_tol(self, abs_tol: double) -> None:
        self.__abs_tol = abs_tol

    @property
    def rel_tol(self) -> double:
        return double(self.__rel_tol)

    @rel_tol.setter
    def rel_tol(self, rel_tol: double) -> None:
        self.__rel_tol = rel_tol


# -----------------------Main-------------------------------------
if "__main__" == __name__:
    single_value = single(1)
    print(f'single = {single_value}')
    convNum = Bin2SingleConversion(s_value=single_value)
    print(f'single = {convNum.get_single()}')
    print(f'binary = {convNum.get_bin()}')
    # entered_value = single(input('Enter float number: '))
    # entered_value = Bin2SingleConversion(s_value=entered_value)
    # bin_value = entered_value.get_bin()
    # print(f'{bin_value=}')
    # print(f'hex_value={entered_value.get_single()}')
    # print('\n+1')
    # entered_value.add_min()
    # print(f'\tentered_value+little={entered_value.get_single()}')
    # print(f'\tentered_value+little(bin)={entered_value.get_bin()}')
    # print('\n-1')
    # entered_value.sub_min(2)
    # print(f'\tentered_value-little={entered_value.get_single()}')
    # print(f'\tentered_value-little(bin)={entered_value.get_bin()}')
    # print('\n-----change bit---------')
    # nbit = int(input('Enter num bit: '))
    # vb = int((input('Enter entered_value: ')))
    # if vb > 0:
    #     vb = True
    # else:
    #     vb = False
    # entered_value.chbit(nbit, vb)
    # entered_value = entered_value.get_single()
    # print(f'{format_real_num(entered_value, 15)}')
    # bin_value = entered_value.get_bin()
    # print(f'{bin_value=}')

    # result = None
    # while True:
    #     print("______________________________MENU_____________________________")
    #     print("0:    reprint entered number in float format")
    #     print("1:    display the sum of two numbers in float format")
    #     print("2:    display the difference of two numbers in float format")
    #     print("3:    display the result of multiplying two numbers in float format")
    #     print("4:    display result of  dividing of two numbers in float format")
    #     print("5:    exit")
    #     print()
    #     menu_item = int(input("menu item: "))
    #     if menu_item == 0:
    #         result =input_num("Enter number: ")
    #     elif menu_item == 1:
    #         num1 =input_num("Enter number1: ")
    #         num2 =input_num("Enter number2: ")
    #         result = single(num1 + num2)
    #     elif menu_item == 2:
    #         minuend =input_num("Enter minuend: ")
    #         subtractor =input_num("Enter subtractor: ")
    #         result = single(minuend - subtractor)
    #     elif menu_item == 3:
    #         num1 =input_num("Enter number1: ")
    #         num2 =input_num("Enter number2: ")
    #         result = single(num1 * num2)
    #     elif menu_item == 4:
    #         divident =input_num("Enter dividend: ")
    #         divider =input_num("Enter divider: ")
    #         if divider != 0:
    #             result = single(divident/divider)
    #         else:
    #             result = 0
    #     elif menu_item == 5:
    #         print("----------------------------EXIT----------------------------------------")
    #         exit(0)
    #     else:
    #         print("Enter valid number menu item")
    #         continue
    #     # print result
    #     print("-----------------------------RESULT--------------------------------------")
    #     print("result=", format_real_num(result, 19))
    #     print("----------------------------------------------------------------------------\n")
    #     print("\t\tFOR NEXT OPERATION PRESS \"ENTER\"")
    #     input()
    #     for _ in range(30):  print("\n")
