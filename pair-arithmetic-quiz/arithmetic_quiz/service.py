"""生成文件和批改文件的应用服务。"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .expression import Binary, format_fraction
from .generator import ProblemGenerator
from .parser import parse_expression, parse_number


LINE_NUMBER_RE = re.compile(r"^\s*(\d+)\.\s*(.*?)\s*$")


def _remove_line_number(line: str) -> tuple[int, str]:
    match = LINE_NUMBER_RE.match(line)
    if not match:
        raise ValueError(f"行格式错误：{line}")
    return int(match.group(1)), match.group(2)


def generate_files(
    count: int,
    range_limit: int,
    output_directory: Path,
    *,
    generator: ProblemGenerator | None = None,
) -> tuple[Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)
    generator = generator or ProblemGenerator(range_limit)
    expressions = generator.generate(count)

    exercise_lines: list[str] = []
    answer_lines: list[str] = []
    for index, expression in enumerate(expressions, start=1):
        if not isinstance(expression, Binary):
            question = f"{expression.render()} ="
        else:
            question = expression.render_question()
        exercise_lines.append(f"{index}. {question}")
        answer_lines.append(f"{index}. {format_fraction(expression.evaluate())}")

    exercises_path = output_directory / "Exercises.txt"
    answers_path = output_directory / "Answers.txt"
    exercises_path.write_text("\n".join(exercise_lines) + "\n", encoding="utf-8")
    answers_path.write_text("\n".join(answer_lines) + "\n", encoding="utf-8")
    return exercises_path, answers_path


@dataclass(frozen=True, slots=True)
class GradeResult:
    correct: list[int]
    wrong: list[int]

    @staticmethod
    def _line(label: str, indexes: list[int]) -> str:
        joined = ", ".join(map(str, indexes))
        return f"{label}: {len(indexes)} ({joined})"

    def render(self) -> str:
        return f"{self._line('Correct', self.correct)}\n{self._line('Wrong', self.wrong)}\n"


def grade_files(exercises_path: Path, answers_path: Path, grade_path: Path) -> GradeResult:
    exercise_lines = [
        line for line in exercises_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()
    ]
    answer_lines = [
        line for line in answers_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()
    ]

    correct: list[int] = []
    wrong: list[int] = []
    for position, exercise_line in enumerate(exercise_lines):
        number, expression_text = _remove_line_number(exercise_line)
        try:
            expected = parse_expression(expression_text).evaluate()
            if position >= len(answer_lines):
                raise ValueError("缺少答案")
            answer_number, answer_text = _remove_line_number(answer_lines[position])
            if answer_number != number:
                raise ValueError("题号不匹配")
            actual = parse_number(answer_text.rstrip("=").strip())
            (correct if actual == expected else wrong).append(number)
        except (ValueError, ZeroDivisionError):
            wrong.append(number)

    result = GradeResult(correct, wrong)
    grade_path.write_text(result.render(), encoding="utf-8")
    return result
