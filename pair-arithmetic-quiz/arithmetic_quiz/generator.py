"""随机题目生成与题内约束检查。"""

from __future__ import annotations

import random
from fractions import Fraction

from .expression import Binary, Expression, Number


class GenerationError(RuntimeError):
    """无法在合理尝试次数内生成足够多的唯一题目。"""


class ProblemGenerator:
    def __init__(self, range_limit: int, rng: random.Random | None = None) -> None:
        if range_limit < 1:
            raise ValueError("-r 必须是大于等于 1 的整数")
        self.range_limit = range_limit
        self.rng = rng or random.Random()

    def _number(self) -> Number:
        """生成小于 range_limit 的自然数或分数，分母也小于范围上限。"""
        can_make_fraction = self.range_limit >= 3
        if not can_make_fraction or self.rng.random() < 0.65:
            return Number(Fraction(self.rng.randrange(self.range_limit), 1))

        denominator = self.rng.randrange(2, self.range_limit)
        whole = self.rng.randrange(self.range_limit)
        numerator = self.rng.randrange(1, denominator)
        value = Fraction(whole * denominator + numerator, denominator)
        # whole 最大为 r-1，附加分数后可能达到或超过 r，故作截断处理。
        if value >= self.range_limit:
            value = Fraction(numerator, denominator)
        return Number(value)

    def _tree(self, operator_count: int) -> Expression:
        if operator_count == 0:
            return self._number()

        left_count = self.rng.randrange(operator_count)
        right_count = operator_count - 1 - left_count
        left = self._tree(left_count)
        right = self._tree(right_count)
        left_value = left.evaluate()
        right_value = right.evaluate()

        operator = self.rng.choices(
            ["+", "−", "×", "÷"], weights=[30, 25, 25, 20], k=1
        )[0]

        if operator == "−":
            if left_value < right_value:
                left, right = right, left
            return Binary(operator, left, right)

        if operator == "÷":
            # 只有 0 < 被除数 < 除数时，商才是真分数。
            if left_value > 0 and right_value > 0 and left_value != right_value:
                if left_value > right_value:
                    left, right = right, left
                return Binary(operator, left, right)
            # 当前两个子式不适合做除法时，退化为始终合法的加法。
            operator = "+"

        return Binary(operator, left, right)

    def generate(self, count: int) -> list[Expression]:
        if count < 1:
            raise ValueError("-n 必须是大于等于 1 的整数")

        expressions: list[Expression] = []
        seen: set[tuple[object, ...]] = set()
        max_attempts = max(10_000, count * 250)

        for _ in range(max_attempts):
            # 题目要求“不超过 3 个”，这里让每题随机包含 1~3 个运算符。
            expression = self._tree(self.rng.randint(1, 3))
            key = expression.canonical_key()
            if key in seen:
                continue
            seen.add(key)
            expressions.append(expression)
            if len(expressions) == count:
                return expressions

        raise GenerationError(
            f"在 -r {self.range_limit} 下只能生成 {len(expressions)} 道不同题目；"
            "请减小 -n 或增大 -r。"
        )
