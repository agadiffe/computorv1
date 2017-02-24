#!/usr/bin/env python
# coding: utf-8

import sys
import re
from collections import OrderedDict
from fractions import Fraction

def main():
    if len(sys.argv) > 1:
        try:
            left_eq, right_eq = check_eq(sys.argv[1])
            result_left = get_operator_coef_degree(left_eq)
            result_right = get_operator_coef_degree(right_eq)
            left_data = get_dict_data_eq(result_left)
            right_data = get_dict_data_eq(result_right)
            final_data = merge_data(left_data, right_data)
            print_eq_reduced_form(final_data)
            eq_degree = check_equation_degree(final_data)
            print bcolors.WHITE + "Polynomial degree: " + str(eq_degree) + bcolors.ENDC
            if eq_degree > 2:
                print bcolors.GREEN + "The polynomial degree is stricly greater than 2, I can't solve." + bcolors.ENDC
            else:
                solve_equation(final_data, eq_degree)
        except Exception, e:
            print str(e)
            print "Error"
    else:
        print bcolors.WHITE + "usage: ./computorv1 '8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0'"
        print "       degree can be in any order and present several time"
        print "       Every terms are in the form of : a * X^p" + bcolors.ENDC

def check_eq(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2 = 3 * X^-1
    check syntax of equation
    return: tuple with left_side and right_side of the equation
    """
    try:
        pattern_0 = "^\s*((?:[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)(?:(?:\s*(?:[+-]\s*))[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)*)\s*=\s*((?:[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)(?:(?:\s*(?:[+-]\s*))[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)*)\s*$"
        result = re.match(pattern_0, eq)
        left_eq =  result.group(1)
        right_eq = result.group(2)
        return (left_eq, right_eq)
    except Exception:
        print bcolors.YELLOW + "/!\ Error: Invalid format /!\\" + bcolors.ENDC
        sys.exit()

def get_operator_coef_degree(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2
    return: list of tuple with [(operator, coef, degree), ...]
    """
    pattern_1 = "(?:\s*([+-])\s*)?(?:([+-]?\d+(?:\.\d+)?)\s*\*\s*[xX]\s*\^\s*([+-]?\d+(?:\.\d+)?))"
    result = re.findall(pattern_1, eq)
    return result

def get_dict_data_eq(eq_data):
    """
    @param: data of equation returned by get_operator_coef_degree()
    check if equation is polynomial form
    return: data dictionary {degree:coef, ...}
    error: if degree < 0 or float degree
    """
    data = {};
    for sign, coef, degree in eq_data:
        if sign == "-" and coef[0] == "-":
            coef = float(coef[1:])
        elif sign == "-":
            coef = -float(coef)
        else:
            coef = float(coef)
        try:
            degree = int(degree)
        except Exception:
            print bcolors.YELLOW + "/!\ Error: degree can't be a float /!\\" + bcolors.ENDC
            sys.exit()
        if degree < 0:
            print bcolors.YELLOW + "/!\ Error: degree can't be negative /!\\" + bcolors.ENDC
            sys.exit()
        if data.get(degree):
            data[degree] += coef
        else:
            data[degree] = coef
    return data

def merge_data(left_data, right_data):
    """
    @param: equation data returned by get_dict_data_eq()
    return: dictionary merged data (sorted by degree) of equation
            to get coef and degree of reduced form aX^2 + bX + c = 0
    """
    final_data = left_data.copy()
    for degree, coef in right_data.items():
        if final_data.get(degree):
            final_data[degree] -= coef
        else:
            final_data[degree] = -coef
    sorted_final_data = OrderedDict(sorted(final_data.items(), key=lambda t: t[0]))
    return sorted_final_data
    
def print_eq_reduced_form(final_data):
    reduced_form = ""
    for degree, coef in final_data.items():
        if coef != 0:
            if coef.is_integer():
                coef = int(coef)
            if degree == 0:
                reduced_form += str(coef)
            elif coef < 0:
                if reduced_form == "":
                    reduced_form += str(coef) + "*" + "X"
                else:
                    reduced_form += bcolors.MAGENTA + " - " + bcolors.ENDC  + str(coef)[1:] + "*" + "X"
            else:
                if reduced_form == "":
                    reduced_form += str(coef) + "*" + "X"
                else:
                    reduced_form += bcolors.MAGENTA + " + " + bcolors.ENDC + str(coef) + "*" + "X"
            if degree > 1:
                reduced_form += "^" + str(degree)
    if reduced_form == "":
        reduced_form += "0"
    reduced_form += bcolors.CYAN + " = " + bcolors.ENDC + "0"
    print bcolors.BLUE + "Reduced form: " + bcolors.ENDC + reduced_form

def check_equation_degree(eq_data):
    """
    @param: equation data returned by merge_data()
    return: max degree of polynomial equation
    """
    max_degree = 0
    for degree, coef in eq_data.items():
        if degree > max_degree and coef != 0:
            max_degree = degree
    return max_degree

def solve_equation(final_data_eq, eq_degree):
    """
    get coef of equation and send them to first or second degree solver function
    first degree: aX + b = 0
    second degree: aX^2 + bX + c = 0
    """
    a = final_data_eq.get(2, 0.0)
    b = final_data_eq.get(1, 0.0)
    c = final_data_eq.get(0, 0.0)
    if eq_degree == 2:
        solve_equation_second_degree(a, b, c)
    else:
        solve_equation_first_degree(b, c)

def solve_equation_second_degree(a, b, c):
    """
    aX^2 + bX + c = 0
    Δ = b^2 − 4ac
    Δ > 0: x1 = (−b − √Δ)/(2a) and x2 = (−b + √Δ )/(2a) 
    Δ = 0: x0 = −b/(2a)
    Δ < 0: x1 = (−b − i√(-Δ))/(2a) and x2 = (−b + i√(-Δ))/(2a)
    """
    delta = b * b - 4 * a * c
    if delta > 0:
        sqrt_delta = square_root(delta)
        x1 = (-b - sqrt_delta) / (2 * a)
        x2 = (-b + sqrt_delta) / (2 * a)
        x1 = get_integer(x1)
        x2 = get_integer(x2)
        delta = get_integer(delta)
        print bcolors.YELLOW + "Delta = " + str(delta) + bcolors.ENDC
        print "Discriminant is strictly positive, the two solutions are:"
        print bcolors.GREEN + str(x1) + bcolors.ENDC
        print bcolors.GREEN + str(x2) + bcolors.ENDC
    elif delta == 0:
        x0 = -b / (2 * a)
        x0 = get_integer(x0)
        print bcolors.YELLOW + "Delta = 0" + bcolors.ENDC
        print "Discriminant is equal to 0, the solution is:"
        print bcolors.GREEN + str(x0) + bcolors.ENDC
    else:
        sqrt_delta = square_root(-delta)
        a = get_integer(a)
        b = get_integer(b)
        delta = get_integer(delta)
        if sqrt_delta.is_integer():
            sqrt_delta = int(sqrt_delta)
            x1 = str(-b) + " - i(" + str(sqrt_delta) + ") / " + str(2 * a)
            x2 = str(-b) + " + i(" + str(sqrt_delta) + ") / " + str(2 * a)
        else:
            x1 = str(-b) + " - i√(" + str(-delta) + ") / " + str(2 * a)
            x2 = str(-b) + " + i√(" + str(-delta) + ") / " + str(2 * a)
        print bcolors.YELLOW + "Delta = " + str(delta) + bcolors.ENDC
        print "Discriminant is strictly negative, the two solutions are:"
        print bcolors.GREEN + str(x1) + bcolors.ENDC
        print bcolors.GREEN + str(x2) + bcolors.ENDC

def solve_equation_first_degree(a, b):
    """
    aX + b = 0
    a != 0: x = -b/a
    a == 0 and b == 0: undefined (all Real)
    a == 0 and b != 0: impossible
    """
    if a == 0:
        print "The solution is:"
        if b == 0:
            print bcolors.GREEN + "Undefined: All Real numbers are solutions" + bcolors.ENDC
        else:
            print bcolors.GREEN + "Impossible: There is no solution" + bcolors.ENDC
    else:
        x = -b / a
        x = get_integer(x)
        print "The solution is:"
        print bcolors.GREEN + str(x) + bcolors.ENDC

def get_integer(nb):
    if nb.is_integer():
        return int(nb)
    elif len(str(abs(nb))) > 7:
        return nb
    else:
        return Fraction(nb).limit_denominator(10000)

def square_root(nb):
    if nb == 0.0:
        return 0.0
    else:
        M = 1.0
        XN = nb  
        while XN >= 2.0:
            XN = 0.25 * XN
            M = 2.0 * M
        while XN < 0.5:
            XN = 4.0 * XN
            M = 0.5 * M
        A = XN
        B = 1.0 - XN
        while 1 == 1: 
            A = A * (1.0 + 0.5 * B)
            B = 0.25 * (3.0 + B) * B * B
            if B < 1.0E-15:
                return A * M

class bcolors:
    WHITE = '\033[97m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'

if __name__ == "__main__":
    main()
