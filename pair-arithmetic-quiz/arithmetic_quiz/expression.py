"""表达式树及其精确求值、显示和去重规则。"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TypeAlias


def format_fraction(value: Fraction) -> str:
    """按作业格式输出自然数、真分数或带分数。"""
    if value.denominator == 1:
        return str(value.numerator)

    whole, remainder = divmod(value.numerator, value.denominator)
    if whole == 0:
        return f"{remainder}/{value.denominator}"
    return f"{whole}’{remainder}/{value.denominator}"


@dataclass(frozen=True, slots=True)
class Number:
    value: Fraction

    def evaluate(self) -> Fraction:
        return self.value

    def render(self) -> str:
        return format_fraction(self.value)

    def canonical_key(self) -> tuple[object, ...]:
        return ("number", self.value.numerator, self.value.denominator)

    def operator_count(self) -> int:
        return 0


Expression: TypeAlias = "Number | Binary"


@dataclass(frozen=True, slots=True)
class Binary:
    operator: str
    left: Expression
    right: Expression

    def evaluate(self) -> Fraction:
        left_value = self.left.evaluate()
        right_value = self.right.evaluate()
        if self.operator == "+":
            return left_value + right_value
        if self.operator == "−":
            return left_value - right_value
        if self.operator == "×":
            return left_value * right_value
        if self.operator == "÷":
            if right_value == 0:
                raise ZeroDivisionError("表达式中出现除以零")
            return left_value / right_value
        raise ValueError(f"未知运算符：{self.operator}")

    def render(self) -> str:
        # 子表达式全部加括号，可无歧义地保留随机生成的树结构。
        return f"({self.left.render()} {self.operator} {self.right.render()})"

    def render_question(self) -> str:
        rendered = self.render()
        return f"{rendered[1:-1]} ="

    def canonical_key(self) -> tuple[object, ...]:
        left_key = self.left.canonical_key()
        right_key = self.right.canonical_key()
        if self.operator in {"+", "×"}:
            left_key, right_key = sorted((left_key, right_key), key=repr)
        return (self.operator, left_key, right_key)

    def operator_count(self) -> int:
        return 1 + self.left.operator_count() + self.right.operator_count()
