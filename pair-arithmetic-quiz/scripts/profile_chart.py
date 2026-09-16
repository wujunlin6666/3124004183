"""把 cProfile 数据绘制成适合博客使用的性能柱状图。"""

from __future__ import annotations

import os
import pstats
from pathlib import Path

import matplotlib.pyplot as plt


PROJECT_FILES = {"service.py", "generator.py", "expression.py", "parser.py"}


def main() -> None:
    profile_path = Path("generation.prof")
    if not profile_path.exists():
        raise SystemExit("请先运行：python scripts/profile_generation.py")

    stats = pstats.Stats(str(profile_path))
    rows: list[tuple[str, float]] = []
    for (filename, _line, function_name), values in stats.stats.items():
        short_name = os.path.basename(filename)
        if short_name in PROJECT_FILES:
            cumulative_time = values[3]
            rows.append((f"{short_name}:{function_name}", cumulative_time))

    rows = sorted(rows, key=lambda item: item[1], reverse=True)[:8]
    labels = [item[0] for item in reversed(rows)]
    times = [item[1] for item in reversed(rows)]

    figure, axis = plt.subplots(figsize=(10, 5.5))
    bars = axis.barh(labels, times, color="#4C78A8")
    axis.set_title("Generation of 10,000 Questions — Cumulative Time")
    axis.set_xlabel("Cumulative time (seconds)")
    axis.grid(axis="x", linestyle="--", alpha=0.3)
    for bar, value in zip(bars, times):
        axis.text(value + 0.005, bar.get_y() + bar.get_height() / 2, f"{value:.3f}s", va="center")

    figure.tight_layout()
    output_directory = Path("blog_assets")
    output_directory.mkdir(exist_ok=True)
    output_path = output_directory / "performance_profile.png"
    figure.savefig(output_path, dpi=180, bbox_inches="tight")
    print(f"性能图已生成：{output_path.resolve()}")


if __name__ == "__main__":
    main()
