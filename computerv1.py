#!/usr/bin/env python
# coding: utf-8

import sys
import re


def merge_data(left_data, right_data):
    """
    @param: equation data returned by get_dict_data_eq()
    return: merged data of equation to get: ax2 + bx + c = 0
    error if: degre > 2 or a == 0
    """
    final_data = left_data.copy()
    for power, coef in right_data.items():
        if final_data.get(power):
            final_data[power] -= coef
        else:
            final_data[power] = coef
    return final_data
    

def get_dict_data_eq(eq_data):
    """
    @param: data of equation returned by get_sign_coef_power()
    check if equation is polynomial form
    return: data dictionary {'power':'coef', [...]}  or Error
    """
    data = {};
    for sign, coef, power in eq_data:
        if sign == "-" and coef[0] == "-":
            coef = float(coef[1:])
        elif sign == "-":
            coef = -float(coef)
        else:
            coef = float(coef)
        try:
            power = int(power)
        except Exception:
            print "Error: float power"
            sys.exit()
        if power < 0:
            print "Error: negative power"
            sys.exit()
        data[power] = coef
    return data


def get_operator_coef_power(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2
    return: list of tuple with (operator, coef, power)  
    """
    pattern_1 = "(?: ([+-]) )?(?:([+-]?\d+(?:\.\d+)?) \* [xX]\^([+-]?\d+(?:\.\d+)?))"
    result = re.findall(pattern_1, eq)
    return result


def check_eq(eq):
    """
    @param: equation. e.g.: 8.3 * X^2 - -6 * x^-1.2 = 3 * X^-1
    check syntax of equation
    return: tuple with left_side and right_side of the equation or Error
    """
    try:
        pattern_0 = "^((?:[+-]?\d+(?:\.\d+)? \* [xX]\^[+-]?\d+(?:\.\d+)?)(?:(?: (?:[+-] ))[+-]?\d+(?:\.\d+)? \* [xX]\^[+-]?\d+(?:\.\d+)?)*) = ((?:[+-]?\d+(?:\.\d+)? \* [xX]\^[+-]?\d+(?:\.\d+)?)(?:(?: (?:[+-] ))[+-]?\d+(?:\.\d+)? \* [xX]\^[+-]?\d+(?:\.\d+)?)*)$"
        result = re.match(pattern_0, eq)
        left_eq =  result.group(1)
        right_eq = result.group(2)
        return (left_eq, right_eq)
    except Exception:
        print "Invalid format"
        sys.exit()


def main():
    try:
        left_eq, right_eq =  check_eq(sys.argv[1])
        result_left = get_operator_coef_power(left_eq)
        result_right = get_operator_coef_power(right_eq)
        left_data = get_dict_data_eq(result_left)
        right_data = get_dict_data_eq(result_right)
        final_data = merge_data(left_data, right_data)
        print final_data
        reduced_form = ""
        for index, (power, coef) in enumerate(final_data.items()):
            if coef.is_integer():
                coef = int(coef)
            if index == 0:
                reduced_form += str(coef) + " * " + "X^" + str(power)
            elif coef < 0:
                reduced_form += " - " + str(coef)[1:] + " * " + "X^" + str(power)
            else:
                reduced_form += " + " + str(coef) + " * " + "X^" + str(power)
        reduced_form += " = 0"
        print reduced_form
    except Exception:
        print "Error"

if __name__ == "__main__":
    main()
