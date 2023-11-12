import struct

from bitstring import BitArray
from numpy import single


def format_real_num(num, precision):
    return '{:.{}g}'.format(num, precision)


def input_num(text: str):
    return single(input(text))


class bin2single_conversion:
    def __init__(self, s_value=None, b_value=None):
        if s_value:
            self.__s_value = single(s_value)
            self.__conv2bin()
        elif b_value:
            self.__b_value = str(b_value)
            self.__conv2single()
        else:
            self.__b_value = '0'
            self.__s_value = single(0)

    def __conv2bin(self):
        # Преобразовать число float32 в его двоичное представление
        binary_representation = struct.pack('!f', self.__s_value)
        # Преобразовать байты в строку из нулей и единиц (бинарное представление)
        self.__b_value = ''.join(f'{byte:08b}' for byte in binary_representation)

    def __conv2single(self):
        # Преобразовать двоичную строку обратно в байты
        binary_bytes = bytes(int(self.__b_value[i:i + 8], 2) for i in range(0, len(self.__b_value), 8))
        # Преобразовать байты в число float32
        self.__s_value = single(struct.unpack('!f', binary_bytes)[0])

    def get_bin(self):
        return self.__b_value

    def get_single(self):
        return self.__s_value

    def chbit(self, nbit, value: bool):
        binary_representation = struct.pack('!f', self.__s_value)
        bit_array = BitArray(bytes=binary_representation)
        bit_array[nbit] = bool(value)
        modified_binary = bit_array.tobytes()
        self.__s_value = single(struct.unpack('!f', modified_binary)[0])
        self.__conv2bin()

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
            if value == 0:
                sign = 1
                value = loop
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


if "__main__" == __name__:
    single_value = single(input('Enter float number: '))
    value = bin2single_conversion(s_value=single_value)
    bin_value = value.get_bin()
    print(f'{bin_value=}')
    print('\n+1')
    value.add_min()
    print(f'\tvalue+little={value.get_single()}')
    print(f'\tvalue+little(bin)={value.get_bin()}')
    print('\n-1')
    value.sub_min(2)
    print(f'\tvalue-little={value.get_single()}')
    print(f'\tvalue-little(bin)={value.get_bin()}')
    print('\n-----change bit---------')
    nbit = int(input('Enter num bit: '))
    vb = int((input('Enter value: ')))
    if vb > 0:
        vb = True
    else:
        vb = False
    value.chbit(nbit, vb)
    single_value = value.get_single()
    print(f'{format_real_num(single_value, 15)}')
    bin_value = value.get_bin()
    print(f'{bin_value=}')

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
