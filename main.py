import sys

from file_utils import read_file, write_result
from plagiarism_checker import calculate_similarity


def main():
    """
    程序入口
    """

    if len(sys.argv) != 4:
        print(
            "Usage: python main.py "
            "<original_file> "
            "<copy_file> "
            "<answer_file>"
        )
        return

    original_path = sys.argv[1]
    copy_path = sys.argv[2]
    answer_path = sys.argv[3]

    try:
        original_text = read_file(original_path)
        copy_text = read_file(copy_path)

    except FileNotFoundError:
        print("Error: input file not found")
        return

    if not original_text.strip() or not copy_text.strip():
        print("Error: empty file")
        return

    try:
        similarity = calculate_similarity(
            original_text,
            copy_text
        )

    except Exception as e:
        print(f"Error: calculation failed - {e}")
        return

    try:
        write_result(
            answer_path,
            similarity
        )

    except Exception as e:
        print(f"Error: output failed - {e}")


if __name__ == "__main__":
    main()