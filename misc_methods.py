ver = 2022-1-8-1

import math


class MiscMethods:

    @staticmethod
    def hex_to_signed_int(val):
        uintval = int(val, 16)
        bits = 4 * (len(val) - 2)
        if uintval >= math.pow(2, bits-1):
            uintval = int(0 - (math.pow(2, bits) - uintval))
        return uintval

    @staticmethod
    def only_positive_numbers(char):
        return char.lstrip('-').isdigit()

    @staticmethod
    def only_numbers(char):
        return char.isdigit()
