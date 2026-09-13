import jieba
import math
from collections import Counter


def tokenize(text):
    """
    中文文本预处理和分词

    :param text: 原始文本
    :return: 有效词语列表
    """

    punctuation = "，。！？；：、,.!?;:\"'（）()【】[]"

    words = jieba.lcut(text)

    return [
        word.strip()
        for word in words
        if word.strip()
        and word not in punctuation
    ]


def calculate_tf(words):

    total = len(words)

    counter = Counter(words)

    return {
        word: count / total
        for word, count in counter.items()
    }


def cosine_similarity(vector1, vector2):

    numerator = sum(
        vector1[key] * vector2.get(key, 0)
        for key in vector1
    )

    denominator1 = math.sqrt(
        sum(value ** 2 for value in vector1.values())
    )

    denominator2 = math.sqrt(
        sum(value ** 2 for value in vector2.values())
    )

    if denominator1 == 0 or denominator2 == 0:
        return 0

    return numerator / (denominator1 * denominator2)


def calculate_similarity(text1, text2):

    words1 = tokenize(text1)
    words2 = tokenize(text2)

    vector1 = calculate_tf(words1)
    vector2 = calculate_tf(words2)

    return cosine_similarity(vector1, vector2)