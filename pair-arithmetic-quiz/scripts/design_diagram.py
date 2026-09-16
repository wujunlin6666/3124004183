"""生成博客使用的项目模块关系图。"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


def box(axis, x, y, width, height, title, detail, color):
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=color, edgecolor="#34495E", linewidth=1.5,
    )
    axis.add_patch(patch)
    axis.text(x + width / 2, y + height * 0.64, title, ha="center", va="center", fontsize=12, weight="bold")
    axis.text(x + width / 2, y + height * 0.30, detail, ha="center", va="center", fontsize=9)


def arrow(axis, start, end):
    axis.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, color="#566573", linewidth=1.4))


def main() -> None:
    figure, axis = plt.subplots(figsize=(12, 6.5))
    axis.set_xlim(0, 12)
    axis.set_ylim(0, 7)
    axis.axis("off")

    box(axis, 0.5, 2.7, 2.0, 1.1, "main.py / cli.py", "argument parsing", "#D6EAF8")
    box(axis, 3.3, 2.7, 2.0, 1.1, "service.py", "generate / grade files", "#D5F5E3")
    box(axis, 6.1, 4.5, 2.1, 1.1, "generator.py", "random tree + dedup", "#FCF3CF")
    box(axis, 6.1, 0.9, 2.1, 1.1, "parser.py", "recursive descent", "#FADBD8")
    box(axis, 9.1, 2.7, 2.3, 1.1, "expression.py", "tree / Fraction / key", "#E8DAEF")
    box(axis, 3.3, 5.3, 2.0, 1.0, "Exercises.txt", "questions", "#F2F3F4")
    box(axis, 3.3, 0.1, 2.0, 1.0, "Answers / Grade", "answers and result", "#F2F3F4")

    arrow(axis, (2.5, 3.25), (3.3, 3.25))
    arrow(axis, (5.3, 3.5), (6.1, 4.75))
    arrow(axis, (5.3, 3.0), (6.1, 1.75))
    arrow(axis, (8.2, 5.0), (9.1, 3.65))
    arrow(axis, (8.2, 1.45), (9.1, 2.95))
    arrow(axis, (4.3, 3.8), (4.3, 5.3))
    arrow(axis, (4.3, 2.7), (4.3, 1.1))

    axis.set_title("Arithmetic Quiz Generator — Module Architecture", fontsize=18, pad=18)
    output_directory = Path("blog_assets")
    output_directory.mkdir(exist_ok=True)
    output_path = output_directory / "design_architecture.png"
    figure.savefig(output_path, dpi=180, bbox_inches="tight", facecolor="white")
    print(f"设计图已生成：{output_path.resolve()}")


if __name__ == "__main__":
    main()
