"""命令行参数处理。"""

from __future__ import annotations

import argparse
from pathlib import Path

from .generator import GenerationError
from .service import generate_files, grade_files


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Myapp",
        description="生成小学四则运算题目，或批改已有答案。",
    )
    parser.add_argument("-n", type=int, default=None, help="生成题目数量（默认 10）")
    parser.add_argument("-r", type=int, help="操作数和分母的上限（不包含该值）")
    parser.add_argument("-e", type=Path, metavar="EXERCISES", help="待批改的题目文件")
    parser.add_argument("-a", type=Path, metavar="ANSWERS", help="待批改的答案文件")
    return parser


def _fail(parser: argparse.ArgumentParser, message: str) -> int:
    parser.print_help()
    print(f"\n错误：{message}")
    return 2


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    grading_mode = args.e is not None or args.a is not None
    if grading_mode:
        if args.e is None or args.a is None:
            return _fail(parser, "批改模式必须同时提供 -e 和 -a。")
        if args.r is not None or args.n is not None:
            return _fail(parser, "批改模式不能同时使用 -n 或 -r。")
        try:
            result = grade_files(args.e, args.a, Path.cwd() / "Grade.txt")
        except (OSError, ValueError) as exc:
            return _fail(parser, f"批改失败：{exc}")
        print(result.render(), end="")
        print(f"批改结果已写入：{Path.cwd() / 'Grade.txt'}")
        return 0

    if args.r is None:
        return _fail(parser, "生成模式必须提供 -r 参数。")
    count = 10 if args.n is None else args.n
    if args.r < 1:
        return _fail(parser, "-r 必须大于等于 1。")
    if count < 1:
        return _fail(parser, "-n 必须大于等于 1。")

    try:
        exercises_path, answers_path = generate_files(count, args.r, Path.cwd())
    except (GenerationError, OSError, ValueError) as exc:
        return _fail(parser, f"生成失败：{exc}")
    print(f"已生成 {count} 道题目：{exercises_path}")
    print(f"答案文件：{answers_path}")
    return 0
