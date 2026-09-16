"""作业格式算术表达式的词法分析和递归下降解析。"""

from __future__ import annotations

import re
from fractions import Fraction

from .expression import Binary, Expression, Number


TOKEN_RE = re.compile(
    r"\s*(\d+[’']\d+/\d+|\d+/\d+|\d+|[+\-−×÷*/()=])"
)


def parse_number(text: str) -> Fraction:
    text = text.strip().replace("'", "’")
    mixed = re.fullmatch(r"(\d+)’(\d+)/(\d+)", text)
    if mixed:
        whole, numerator, denominator = map(int, mixed.groups())
        if denominator == 0 or numerator >= denominator:
            raise ValueError(f"无效带分数：{text}")
        return Fraction(whole * denominator + numerator, denominator)

    fraction = re.fullmatch(r"(\d+)/(\d+)", text)
    if fraction:
        numerator, denominator = map(int, fraction.groups())
        if denominator == 0:
            raise ValueError(f"分母不能为零：{text}")
        return Fraction(numerator, denominator)

    if re.fullmatch(r"\d+", text):
        return Fraction(int(text), 1)
    raise ValueError(f"不是有效数字：{text}")


def _tokenize(text: str) -> list[str]:
    tokens: list[str] = []
    position = 0
    while position < len(text):
        match = TOKEN_RE.match(text, position)
        if not match:
            if text[position:].strip() == "":
                break
            raise ValueError(f"无法识别的内容：{text[position:]}")
        tokens.append(match.group(1))
        position = match.end()
    return tokens


class _Parser:
    def __init__(self, tokens: list[str]) -> None:
        self.tokens = tokens
        self.position = 0

    def peek(self) -> str | None:
        if self.position == len(self.tokens):
            return None
        return self.tokens[self.position]

    def take(self) -> str:
        token = self.peek()
        if token is None:
            raise ValueError("表达式意外结束")
        self.position += 1
        return token

    def expression(self) -> Expression:
        node = self.term()
        while self.peek() in {"+", "-", "−"}:
            operator = self.take()
            node = Binary("−" if operator in {"-", "−"} else "+", node, self.term())
        return node

    def term(self) -> Expression:
        node = self.factor()
        while self.peek() in {"×", "*", "÷", "/"}:
            operator = self.take()
            normalized = "×" if operator in {"×", "*"} else "÷"
            node = Binary(normalized, node, self.factor())
        return node

    def factor(self) -> Expression:
        token = self.take()
        if token == "(":
            node = self.expression()
            if self.take() != ")":
                raise ValueError("缺少右括号")
            return node
        if token in {"+", "-", "−", "×", "*", "÷", "/", ")", "="}:
            raise ValueError(f"此处不应出现：{token}")
        return Number(parse_number(token))


def parse_expression(text: str) -> Expression:
    tokens = _tokenize(text)
    if tokens and tokens[-1] == "=":
        tokens.pop()
    parser = _Parser(tokens)
    node = parser.expression()
    if parser.peek() is not None:
        raise ValueError(f"多余内容：{parser.peek()}")
    return node
