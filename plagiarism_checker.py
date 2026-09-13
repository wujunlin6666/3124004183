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

def calculate_idf(documents):
    """
    计算逆文档频率 IDF

    :param documents: 多篇文档的分词结果
    :return: IDF字典
    """

    total_documents = len(documents)

    idf = {}

    all_words = set(
        word
        for document in documents
        for word in document
    )

    for word in all_words:
        count = sum(
            1
            for document in documents
            if word in document
        )

        idf[word] = math.log(
            (total_documents + 1) / (count + 1)
        ) + 1

    return idf

def calculate_tfidf(words, idf):
    """
    计算TF-IDF向量
    """

    tf = calculate_tf(words)

    return {
        word: tf[word] * idf[word]
        for word in tf
    }

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

    documents = [
        words1,
        words2
    ]

    idf = calculate_idf(documents)

    vector1 = calculate_tfidf(
        words1,
        idf
    )

    vector2 = calculate_tfidf(
        words2,
        idf
    )

    return cosine_similarity(vector1, vector2)