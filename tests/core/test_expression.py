from decimal import Decimal
import pytest

from calc.core.expression import eval_expr
from calc.core.errors import CalcSyntaxError, CalcMathError


def test_basic_addition():
    assert eval_expr("2 + 3") == Decimal("5")


def test_basic_subtraction():
    assert eval_expr("10 - 4") == Decimal("6")


def test_basic_multiplication():
    assert eval_expr("3 * 4") == Decimal("12")


def test_basic_division():
    assert eval_expr("15 / 3") == Decimal("5")


def test_operator_precedence():
    # multiplication before addition
    assert eval_expr("2 + 3 * 4") == Decimal("14")
    # division before subtraction
    assert eval_expr("20 - 10 / 2") == Decimal("15")


def test_parentheses():
    assert eval_expr("(2 + 3) * 4") == Decimal("20")
    assert eval_expr("2 * (5 - 1)") == Decimal("8")


def test_nested_parentheses():
    assert eval_expr("((3 + 4) * 2)") == Decimal("14")
    assert eval_expr("(((1 + 2) * 3) / 9)") == Decimal("1")


def test_unary_minus():
    assert eval_expr("-5") == Decimal("-5")
    assert eval_expr("-(3 + 2)") == Decimal("-5")
    assert eval_expr("10 + -5") == Decimal("5")


def test_decimal_numbers():
    assert eval_expr("1.5 + 2.5") == Decimal("4.0")
    assert eval_expr("10.5 / 2") == Decimal("5.25")


def test_division_by_zero():
    with pytest.raises(CalcMathError):
        eval_expr("10 / 0")


def test_empty_expression():
    with pytest.raises(CalcSyntaxError):
        eval_expr("")


def test_mismatched_parentheses():
    with pytest.raises(CalcSyntaxError):
        eval_expr("(2 + 3")
    with pytest.raises(CalcSyntaxError):
        eval_expr("2 + 3)")


def test_invalid_syntax():
    with pytest.raises(CalcSyntaxError):
        eval_expr("2 + + 3")
    with pytest.raises(CalcSyntaxError):
        eval_expr("* 5")
