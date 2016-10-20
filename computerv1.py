#!/usr/bin/env python
# coding: utf-8

import sys
import re
from collections import OrderedDict

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

def solve_equation_first_degree(a, b):
    """
    aX + b = 0
    a != 0: x = -b/a
    a == 0 and b == 0: undefined (all Real)
    a == 0 and b != 0: impossible
    """
    if a == 0:
        if b == 0:
            print "The solution is:"
            print "Undefined: All Real number are solution"
        else:
            print "The solution is:"
            print "Impossible: There is no solution"
    else:
        x = -b / a
        if x.is_integer():
            x = int(x)
        print "The solution is:"
        print x

def solve_equation_second_degree(a, b, c):
    """
    aX^2 + bX + c = 0
    Δ = b^2 − 4ac
    Δ > 0: x1 = (−b − √Δ)/(2a) and x2 = (−b + √Δ )/(2a) 
    Δ = 0: x0 = −b/(2a)
    Δ < 0: x1 = (−b − i√(-Δ))/(2a) and x2 = (−b + i√(-Δ))/(2a)
    """
    delta = b * b - 4 * a * c
    sqrt_delta = square_root(delta)
    if delta.is_integer():
        delta = int(delta)
    if delta > 0:
        x1 = (-b - sqrt_delta) / (2 * a)
        x2 = (-b + sqrt_delta) / (2 * a)
        if x1.is_integer():
            x1 = int(x1)
        if x2.is_integer():
            x2 = int(x2)
        print x1
        print x2
    elif delta == 0:
        x0 = -b / (2 * a)
        if x0.is_integer():
            x0 = int(x0)
        print x0
    else:
        if a.is_integer():
            a = int(a)
        if b.is_integer():
            b = int(b)
        if sqrt_delta.is_integer():
            sqrt_delta = int(-sqrt_delta)
            x1 = str(-b) + " - i" + sqrt_delta + " / " + str(2 * a)
            x2 = str(-b) + " + i" + sqrt_delta + " / " + str(2 * a)
        else:
            x1 = str(-b) + " - i√(" + str(delta) + ") / " + str(2 * a)
            x2 = str(-b) + " + i√(" + str(delta) + ") / " + str(2 * a)
        print x1
        print x2

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

def check_equation_degree(eq_data):
    """
    @param: equation data returned by merge_data()
    return: tutple with (max degree of polynomial equation, true or false)
    error: if degree 2 and a == 0 (aX^2 + bX + c = 0) return true in tuple
    """
    max_degree = 0
    coef_max_degree = 0
    for degree, coef in eq_data.items():
        if degree > max_degree and coef != 0:
            max_degree = degree
            coef_max_degree = coef
    if max_degree == 2 and coef_max_degree == 0:
        return max_degree, True
    else:
        return max_degree, False

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
            final_data[degree] = coef
    sorted_final_data = OrderedDict(sorted(final_data.items(), key=lambda t: t[0]))
    return sorted_final_data
    
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
            print "Error: degree can't be a float"
            sys.exit()
        if degree < 0:
            print "Error: degree can't be negative"
            sys.exit()
        data[degree] = coef
    return data

def get_operator_coef_degree(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2
    return: list of tuple with [(operator, coef, degree), ...]
    """
    pattern_1 = "(?:\s*([+-])\s*)?(?:([+-]?\d+(?:\.\d+)?)\s*\*\s*[xX]\s*\^\s*([+-]?\d+(?:\.\d+)?))"
    result = re.findall(pattern_1, eq)
    return result

def check_eq(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2 = 3 * X^-1
    check syntax of equation
    return: tuple with left_side and right_side of the equation
    """
    try:
        pattern_0 = "^((?:[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)(?:(?:\s*(?:[+-]\s*))[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)*)\s*=\s*((?:[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)(?:(?:\s*(?:[+-]\s*))[+-]?\d+(?:\.\d+)?\s*\*\s*[xX]\s*\^\s*[+-]?\d+(?:\.\d+)?)*)$"
        result = re.match(pattern_0, eq)
        left_eq =  result.group(1)
        right_eq = result.group(2)
        return (left_eq, right_eq)
    except Exception:
        print "Invalid format"
        sys.exit()

def main():
    if len(sys.argv) > 1:
        try:
            left_eq, right_eq =  check_eq(sys.argv[1])
            result_left = get_operator_coef_degree(left_eq)
            result_right = get_operator_coef_degree(right_eq)
            left_data = get_dict_data_eq(result_left)
            right_data = get_dict_data_eq(result_right)
            final_data = merge_data(left_data, right_data)
            reduced_form = ""
            for index, (degree, coef) in enumerate(final_data.items()):
                if coef.is_integer():
                    coef = int(coef)
                if index == 0:
                    reduced_form += str(coef) + " * " + "X^" + str(degree)
                elif coef < 0:
                    reduced_form += " - " + str(coef)[1:] + " * " + "X^" + str(degree)
                else:
                    reduced_form += " + " + str(coef) + " * " + "X^" + str(degree)
            reduced_form += " = 0"
            print "Reduced form: " + reduced_form
            eq_degree, error_second_degree = check_equation_degree(final_data)
            print "Polynomial degree: " + str(eq_degree)
            if eq_degree > 2:
                print "The polynomial degree is stricly greater than 2, I can't solve."
            elif error_second_degree:
                print "Error: coefficient of degree 2 can't be equal to 0"
            else:
                solve_equation(final_data, eq_degree)
        except Exception, e:
            print str(e)
            print "Error"
    else:
        print "No argument"

if __name__ == "__main__":
    main()
