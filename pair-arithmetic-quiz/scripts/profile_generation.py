"""生成 10000 道题目的性能分析脚本。"""

from __future__ import annotations

import cProfile
import pstats
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from arithmetic_quiz.service import generate_files


def workload() -> None:
    with tempfile.TemporaryDirectory() as directory:
        generate_files(10_000, 10, Path(directory))


if __name__ == "__main__":
    profile_path = Path("generation.prof")
    report_path = Path("profile_report.txt")
    cProfile.run("workload()", str(profile_path))
    with report_path.open("w", encoding="utf-8") as report:
        stats = pstats.Stats(str(profile_path), stream=report)
        stats.strip_dirs().sort_stats("cumulative").print_stats(25)
    print(f"原始数据：{profile_path.resolve()}")
    print(f"文本报告：{report_path.resolve()}")
