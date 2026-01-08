"""
Calculator app tests
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""

from calculator import Calculator

def test_app():
    my_calculator = Calculator()
    welcome_message = my_calculator.get_hello_message()
    assert "== Calculatrice v1.0 ==" in welcome_message

def test_addition():
    my_calculator = Calculator()
    assert my_calculator.addition(2, 3) == 5
    assert my_calculator.addition(0, 0) == 0
    assert my_calculator.addition(-5, 10) == 5
    assert my_calculator.addition(-5, -3) == -8

def test_subtraction():
    my_calculator = Calculator()
    assert my_calculator.subtraction(10, 3) == 7
    assert my_calculator.subtraction(0, 0) == 0
    assert my_calculator.subtraction(5, 10) == -5
    assert my_calculator.subtraction(-5, -3) == -2

def test_multiplication():
    my_calculator = Calculator()
    assert my_calculator.multiplication(2, 3) == 6
    assert my_calculator.multiplication(0, 5) == 0
    assert my_calculator.multiplication(-2, 3) == -6
    assert my_calculator.multiplication(-2, -3) == 6

def test_division():
    my_calculator = Calculator()
    assert my_calculator.division(6, 3) == 2
    assert my_calculator.division(10, 2) == 5
    assert my_calculator.division(7, 2) == 3.5
    assert my_calculator.division(-6, 3) == -2

def test_division_by_zero():
    my_calculator = Calculator()
    result = my_calculator.division(5, 0)
    assert result == "Erreur : division par zéro"
    assert my_calculator.last_result == "Error"

def test_last_result():
    my_calculator = Calculator()
    my_calculator.addition(5, 3)
    assert my_calculator.last_result == 8
    my_calculator.multiplication(2, 4)
    assert my_calculator.last_result == 8
    my_calculator.subtraction(10, 7)
    assert my_calculator.last_result == 3