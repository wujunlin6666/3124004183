import os

from plagiarism_checker import (
    tokenize,
    calculate_similarity,
    calculate_tf
)

from file_utils import (
    read_file,
    write_result
)


def test_tokenize_basic():
    text = "今天是星期天，天气晴。"

    result = tokenize(text)

    assert "今天" in result
    assert "天气" in result


def test_similarity_same_text():
    text = "机器学习是一门人工智能技术"

    score = calculate_similarity(
        text,
        text
    )

    assert score == 1.0


def test_similarity_different_text():
    text1 = "苹果手机很好用"

    text2 = "今天学习软件工程"

    score = calculate_similarity(
        text1,
        text2
    )

    assert score < 1


def test_similarity_range():
    score = calculate_similarity(
        "人工智能",
        "人工智能技术"
    )

    assert 0 <= score <= 1


def test_empty_text():

    score = calculate_similarity(
        "",
        ""
    )

    assert score == 0


def test_file_read():

    path = "test_files/test_read.txt"

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("测试文本")

    result = read_file(path)

    assert result == "测试文本"


def test_file_write():

    path = "test_files/test_output.txt"

    write_result(
        path,
        0.8567
    )

    with open(
        path,
        encoding="utf-8"
    ) as file:

        result = file.read()

    assert result == "0.86"


def test_chinese_similarity():

    score = calculate_similarity(
        "深度学习算法",
        "深度学习模型"
    )

    assert score > 0


def test_punctuation_filter():

    result = tokenize(
        "你好，世界！"
    )

    assert "，" not in result
    assert "！" not in result


def test_long_text():

    text1 = "人工智能"*100

    text2 = "人工智能"*50

    score = calculate_similarity(
        text1,
        text2
    )

    assert score > 0

def test_empty_words_tf():
    from plagiarism_checker import calculate_tf

    result = calculate_tf([])

    assert result == {}

def test_empty_original_text():
    result = calculate_similarity(
        "",
        "这是一个测试文本"
    )

    assert result >= 0