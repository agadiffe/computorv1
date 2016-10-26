#!/bin/sh

echo "##########################################"
echo "#############   ComputorV1   #############"
echo "##########################################"
echo ""

echo "------- <"
echo "| 01"
echo "------------------------------------------ >"
set -x
python computorv1.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 02"
echo "------------------------------------------ >"
set -x
python computorv1.py "5 * X^0 + 4 * X^1 = 4 * X^0"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 03"
echo "------------------------------------------ >"
set -x
python computorv1.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 04"
echo "------------------------------------------ >"
set -x
python computorv1.py "5 * X^10 = 1 * X^1 + 5 * X^10 - 5*X^2"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 05"
echo "------------------------------------------ >"
set -x
python computorv1.py "42 * X^0 = 42 * X^0"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 06"
echo "------------------------------------------ >"
set -x
python computorv1.py "3 * X^2 + 5 * X^1 + 7 * X^0 = 0 * X^0"
{ set +x; } 2>/dev/null
echo "------- <"
echo "| 07"
echo "------------------------------------------ >"
set -x
python computorv1.py "-1 * X^0 - 6 * X^1 + 1 * X^2 = 0 * X^0"
