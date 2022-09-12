from boolErrors import BoolTypeError, BoolLengthError
import math


class BoolFun:

    def __init__(self, data, kind):
        """Initialize the instance.

        Argument kind determines what kind is data i.e.
        1 - data is values of truth table of boolean function
        2 - data is values of truth table of character function
        3 - data is values of algebraic normal form"""

        if kind not in [1, 2, 3]:
            raise BoolTypeError("Incorrect type of data")
        self.data = data
        self.kind = kind
        self.size = int(math.log2(len(data)))

    def __str__(self):
        inscription = ""
        if self.kind == 1:
            inscription += "Postać tablicy prawdy: \n"
        elif self.kind == 2:
            inscription += "Postać tablicy prawdy funkcji znakowej: \n"
        elif self.kind == 3:
            inscription += "Algebraiczna postać normalna: \n"
        inscription += str(self.data)
        return inscription

    def __normal_bool_normal(self):
        """Transform the truth table into algebraic normal form and vice versa.

        It is possible, because this transformation looks identically both for anf and true table"""
        length = 1
        while length < len(self.data):
            for j in range(len(self.data)):
                if (j // length) % 2 == 1:
                    self.data[j] += self.data[j-length]
                    self.data[j] %= 2
            length *= 2

    """Next three functions provide transformation between each form of functions i.e: 
        boolean function, character function, algebraic normal form"""

    def to_char_form(self):
        """Manage the transformation into the truth table of character function"""
        if self.kind == 1:
            for j in range(len(self.data)):
                self.data[j] = (-1) ** self.data[j]
            self.kind = 2
        elif self.kind == 2:
            pass
        elif self.kind == 3:
            self.to_bool_form()
            self.kind = 1
            self.to_char_form()

    def to_normal_form(self):
        """Manage the transformation into algebraic normal form"""
        if self.kind == 1:
            self.__normal_bool_normal()
            self.kind = 3
        elif self.kind == 2:
            self.to_bool_form()
            self.kind = 1
            self.to_normal_form()
        elif self.kind == 3:
            pass

    def to_bool_form(self):
        """Manage the transformation into truth table of boolean function"""
        if self.kind == 1:
            pass
        elif self.kind == 2:
            for j in range(len(self.data)):
                if self.data[j] == -1:
                    self.data[j] = 1
                else:
                    self.data[j] = 0
            self.kind = 1
        elif self.kind == 3:
            self.__normal_bool_normal()
            self.kind = 1

    def __create_anf_help_table(self):
        """Return a list of two-argument lists.

        The first arguments are anf coefficients, which have value 1, saved in binary.
        The second arguments are floats, an integer part of this number
        is sum of values in argument nr one. A decimal part of this number shows
        in which positions in argument nr one was value 1. It is needed to order a notation of the equation
        in generally accepted order e.g. we write x(4) before x(3), x(2)x(1) before x(3) and x(2)x(1) not x(1)x(2)"""
        self.to_normal_form()
        help_table = []
        binary_size = len(bin(len(self.data)-1)[2:])
        for j in range(len(self.data)):
            if self.data[j] or j == 0:
                binary = bin(j)[2:]
                sum_weight_digits = 0
                while len(binary) < binary_size:
                    binary = "0" + binary
                for i in range(len(binary)):
                    if binary[i] == "1":
                        sum_weight_digits += 1 + 0.1 ** (i+1)
                if j == 0:
                    if self.data[j] == 0:
                        sum_weight_digits = 0.0
                    else:
                        sum_weight_digits = -1.0
                help_table.append([binary, sum_weight_digits])
        help_table.sort(key=lambda x: x[1], reverse=True)
        """przypomniec fcje lambda"""
        return help_table, binary_size

    def show_normal_form(self):
        """Show algebraic normal form in the form of an equation"""
        help_table, binary_size = self.__create_anf_help_table()
        equation = ""
        for i in help_table:
            for j in range(binary_size):
                if i[0][j] == "1":
                    equation += "x({0})".format(binary_size-j)
            if i[1] == 0.0 or i[1] == -1.0:
                equation += str(abs(i[1]))[0]
            equation += "+"
        while equation[len(equation)-1] == "+":
            equation = equation[:-1]
        print("Algebraiczna postać normalna to: \n", equation)

    def algebraic_degree(self):
        self.to_normal_form()
        help_table = []
        for j in range(len(self.data)):
            if self.data[j] or j == 0:
                binary = bin(j)[2:]
                sum_weight_digits = 0
                for i in range(len(binary)):
                    if binary[i] == "1":
                        sum_weight_digits += 1
                if j == 0:
                    sum_weight_digits = 0
                help_table.append([binary, sum_weight_digits])
        help_table.sort(key=lambda x: x[1], reverse=True)
        return help_table[0][1]

    def transform_wh(self):
        """Return a list with values of Walsh-Hadamard transformation for each form of available functions"""
        self.to_char_form()
        length = 1
        help_list = self.data[:]
        help_list_2 = self.data[:]
        while length < len(self.data):
            for j in range(len(self.data)):
                if (j // length) % 2 == 0:
                    help_list[j] += help_list_2[j+length]
                else:
                    help_list[j] = help_list_2[j-length] - help_list_2[j]
            length *= 2
            help_list_2 = help_list[:]
        return help_list_2

    def hamming_weight(self):
        self.to_bool_form()
        hamming_weight = 0
        for i in self.data:
            if i == 1:
                hamming_weight += 1
        return hamming_weight

    @staticmethod
    def hamming_distance(fun1, fun2):
        fun1.to_bool_form()
        fun2.to_bool_form()
        hamming_distance = 0
        if len(fun1.data) != len(fun2.data):
            raise BoolLengthError("Different lengths of the truth table")
        for i in range(len(fun1.data)):
            if fun1.data[i] != fun2.data[i]:
                hamming_distance += 1
        return hamming_distance

    def non_linearity(self):
        transform = self.transform_wh()
        for i in range(len(transform)):
            transform[i] = abs(transform[i])
        return 2 ** (self.size - 1) - int(0.5 * max(transform))

    def closest_linear(self):
        transform = self.transform_wh()
        maximum = max(transform)
        closest = 2 ** (self.size - 1) - int(0.5 * maximum)
        result_string = ""
        for i in range(len(transform)):
            if transform[i] == maximum:
                result_string += "A({0},0) = {1}  ".format(i, closest)
        print(result_string)

    def farthest_linear(self):
        transform = self.transform_wh()
        minimum = min(transform)
        closest = 2 ** (self.size - 1) - int(0.5 * minimum)
        result_string = ""
        for i in range(len(transform)):
            if transform[i] == minimum:
                result_string += "A({0},0) = {1}  ".format(i, closest)
        print(result_string)

    def closest_affine(self):
        transform = self.transform_wh()
        transform_abs = []
        for i in range(len(transform)):
            transform_abs.append(abs(transform[i]))
        maximum = max(transform_abs)
        closest = 2 ** (self.size - 1) - int(0.5 * maximum)
        result_string = ""
        for i in range(len(transform)):
            if transform_abs[i] == maximum:
                if transform[i] > 0:
                    affine_or_linear = 0
                else:
                    affine_or_linear = 1
                result_string += "A({0},{1}) = {2}  ".format(i, affine_or_linear, closest)
        print(result_string)

    def farthest_affine(self):
        transform = self.transform_wh()
        transform_abs = []
        for i in range(len(transform)):
            transform_abs.append(abs(transform[i]))
        maximum = max(transform_abs)
        closest = 2 ** (self.size - 1) - int(0.5 * maximum)
        result_string = ""
        for i in range(len(transform)):
            if transform_abs[i] == maximum:
                if transform[i] > 0:
                    affine_or_linear = 1
                else:
                    affine_or_linear = 0
                result_string += "A({0},{1}) = {2}  ".format(i, affine_or_linear, len(self.data)-closest)
        print(result_string)

    @staticmethod
    def correlation_fun(fun1, fun2):
        return (len(fun1.data) - BoolFun.hamming_distance(fun1, fun2)) / len(fun1.data)

    def balanced(self):
        transform = self.transform_wh()
        if transform[0] == 0:
            print("Jest zrównoważona")
        else:
            print("Nie jest zrównoważona")

    def correlation_immune(self):
        transform = self.transform_wh()
        table_argument_weight = []
        for i in range(len(self.data)):
            i = bin(i)[2:]
            argument_weight = 0
            for j in range(len(i)):
                if i[j] == "1":
                    argument_weight += 1
            table_argument_weight.append(argument_weight)
        for degree in range(1, self.size+1, 1):
            for j in range(len(transform)):
                if table_argument_weight[j] == degree:
                    if transform[j] != 0:
                        if degree == 1:
                            print("Odporność korelacyjna nie istnieje!")
                            return
                        else:
                            print("Odporność korelacyjna wynosi: ", degree-1)
                            return
            print("Odporność korelacyjna wynosi: ", degree)
            return
