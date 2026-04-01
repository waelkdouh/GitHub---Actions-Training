# content of tests/test_math.py
from src.calculator import add, subtract, multiply, divide
import pytest

def test_add():
    assert add(10, 5) == 15

def test_subtract():
    assert subtract(10, 5) == 5

def test_multiply():
    assert multiply(10, 5) == 50

def test_divide():
    assert divide(10, 5) == 2

def test_divide_by_zero():
    # This tells pytest to expect an error
    with pytest.raises(ValueError):
        divide(10, 0)
