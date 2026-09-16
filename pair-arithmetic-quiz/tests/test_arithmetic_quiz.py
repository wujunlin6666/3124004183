from __future__ import annotations

import random
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from arithmetic_quiz.expression import Binary, Number, format_fraction
from arithmetic_quiz.generator import ProblemGenerator
from arithmetic_quiz.parser import parse_expression, parse_number
from arithmetic_quiz.service import generate_files, grade_files


def walk(expression):
    yield expression
    if isinstance(expression, Binary):
        yield from walk(expression.left)
        yield from walk(expression.right)


class FractionFormatTests(unittest.TestCase):
    def test_natural_number_format(self):
        self.assertEqual("3", format_fraction(Fraction(3, 1)))

    def test_proper_fraction_format(self):
        self.assertEqual("3/5", format_fraction(Fraction(3, 5)))

    def test_mixed_fraction_format(self):
        self.assertEqual("2’3/8", format_fraction(Fraction(19, 8)))

    def test_parse_ascii_and_curly_apostrophe(self):
        self.assertEqual(Fraction(11, 2), parse_number("5'1/2"))
        self.assertEqual(Fraction(11, 2), parse_number("5’1/2"))


class ParserTests(unittest.TestCase):
    def test_operator_precedence(self):
        self.assertEqual(Fraction(7), parse_expression("1 + 2 × 3 =").evaluate())

    def test_parentheses(self):
        self.assertEqual(Fraction(9), parse_expression("(1 + 2) × 3 =").evaluate())

    def test_fraction_expression(self):
        self.assertEqual(Fraction(7, 24), parse_expression("1/6 + 1/8 =").evaluate())


class DuplicateRuleTests(unittest.TestCase):
    def test_commutative_children_are_duplicates(self):
        first = parse_expression("23 + 45")
        second = parse_expression("45 + 23")
        self.assertEqual(first.canonical_key(), second.canonical_key())

    def test_nested_example_is_duplicate(self):
        first = parse_expression("3 + (2 + 1)")
        second = parse_expression("1 + 2 + 3")
        self.assertEqual(first.canonical_key(), second.canonical_key())

    def test_different_left_associative_tree_is_not_duplicate(self):
        first = parse_expression("1 + 2 + 3")
        second = parse_expression("3 + 2 + 1")
        self.assertNotEqual(first.canonical_key(), second.canonical_key())


class GeneratorTests(unittest.TestCase):
    def test_generated_constraints_on_every_subexpression(self):
        expressions = ProblemGenerator(10, random.Random(20260916)).generate(1000)
        for expression in expressions:
            self.assertLessEqual(expression.operator_count(), 3)
            for node in walk(expression):
                if isinstance(node, Binary) and node.operator == "−":
                    self.assertGreaterEqual(node.left.evaluate(), node.right.evaluate())
                if isinstance(node, Binary) and node.operator == "÷":
                    self.assertGreater(node.evaluate(), 0)
                    self.assertLess(node.evaluate(), 1)

    def test_operands_and_denominators_are_in_range(self):
        expressions = ProblemGenerator(10, random.Random(7)).generate(500)
        for expression in expressions:
            for node in walk(expression):
                if isinstance(node, Number):
                    self.assertGreaterEqual(node.value, 0)
                    self.assertLess(node.value, 10)
                    self.assertLess(node.value.denominator, 10)

    def test_generation_is_unique_under_required_rule(self):
        expressions = ProblemGenerator(10, random.Random(8)).generate(1000)
        keys = [expression.canonical_key() for expression in expressions]
        self.assertEqual(len(keys), len(set(keys)))

    def test_range_one_is_supported(self):
        expressions = ProblemGenerator(1, random.Random(9)).generate(10)
        self.assertEqual(10, len(expressions))

    def test_ten_thousand_questions_are_supported(self):
        expressions = ProblemGenerator(10, random.Random(10)).generate(10_000)
        self.assertEqual(10_000, len(expressions))


class FileServiceTests(unittest.TestCase):
    def test_generate_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generator = ProblemGenerator(10, random.Random(11))
            exercises, answers = generate_files(20, 10, root, generator=generator)
            self.assertEqual(20, len(exercises.read_text(encoding="utf-8").splitlines()))
            self.assertEqual(20, len(answers.read_text(encoding="utf-8").splitlines()))

    def test_grade_correct_and_wrong_answers(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exercises = root / "Exercises.txt"
            answers = root / "Answers.txt"
            grade = root / "Grade.txt"
            exercises.write_text(
                "1. 1/6 + 1/8 =\n2. 3 × 4 =\n3. 9 − 2 =\n",
                encoding="utf-8",
            )
            answers.write_text("1. 7/24\n2. 11\n3. 7\n", encoding="utf-8")
            result = grade_files(exercises, answers, grade)
            self.assertEqual([1, 3], result.correct)
            self.assertEqual([2], result.wrong)
            self.assertEqual(
                "Correct: 2 (1, 3)\nWrong: 1 (2)\n",
                grade.read_text(encoding="utf-8"),
            )

    def test_missing_answer_is_wrong(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            exercises = root / "Exercises.txt"
            answers = root / "Answers.txt"
            exercises.write_text("1. 1 + 1 =\n2. 2 + 2 =\n", encoding="utf-8")
            answers.write_text("1. 2\n", encoding="utf-8")
            result = grade_files(exercises, answers, root / "Grade.txt")
            self.assertEqual([1], result.correct)
            self.assertEqual([2], result.wrong)


if __name__ == "__main__":
    unittest.main()
