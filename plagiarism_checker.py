import jieba
import math
import re
from collections import Counter


# 创建全局分词器
# 避免重复初始化，提高性能
tokenizer = jieba.Tokenizer()


def tokenize(text):
    """
    中文文本分词

    :param text: 输入文本
    :return: 去除标点后的词列表
    """

    words = tokenizer.lcut(text)

    result = []

    for word in words:
        word = word.strip()

        # 去除标点符号
        if word and not re.match(
            r"^[^\w\u4e00-\u9fa5]+$",
            word
        ):
            result.append(word)

    return result



def calculate_tf(words):
    """
    计算词频 TF

    TF = 当前词出现次数 / 总词数
    """

    total_words = len(words)

    if total_words == 0:
        return {}

    counter = Counter(words)

    tf = {}

    for word, count in counter.items():
        tf[word] = count / total_words

    return tf



def calculate_idf(documents):
    """
    计算逆文档频率 IDF

    使用平滑公式：

    log((N+1)/(df+1))+1
    """

    document_count = len(documents)

    word_document_count = Counter()


    for document in documents:

        # 一个词在一篇文章只计算一次
        unique_words = set(document)

        for word in unique_words:
            word_document_count[word] += 1


    idf = {}

    for word, count in word_document_count.items():

        idf[word] = math.log(
            (document_count + 1)
            /
            (count + 1)
        ) + 1


    return idf



def calculate_tfidf(tf, idf):
    """
    TF-IDF计算
    """

    tfidf = {}

    for word, value in tf.items():

        tfidf[word] = (
            value *
            idf.get(word, 0)
        )

    return tfidf



def cosine_similarity(vector1, vector2):
    """
    计算余弦相似度
    """

    common_words = (
        set(vector1.keys())
        &
        set(vector2.keys())
    )


    numerator = sum(
        vector1[word] *
        vector2[word]
        for word in common_words
    )


    denominator1 = math.sqrt(
        sum(
            value ** 2
            for value in vector1.values()
        )
    )


    denominator2 = math.sqrt(
        sum(
            value ** 2
            for value in vector2.values()
        )
    )


    if denominator1 == 0 or denominator2 == 0:
        return 0


    return numerator / (
        denominator1 *
        denominator2
    )



def calculate_similarity(text1, text2):
    """
    计算论文重复率

    :param text1: 原论文
    :param text2: 抄袭论文
    :return: 相似度
    """


    words1 = tokenize(text1)

    words2 = tokenize(text2)


    documents = [
        words1,
        words2
    ]


    idf = calculate_idf(
        documents
    )


    tf1 = calculate_tf(words1)

    tf2 = calculate_tf(words2)


    tfidf1 = calculate_tfidf(
        tf1,
        idf
    )


    tfidf2 = calculate_tfidf(
        tf2,
        idf
    )


    return cosine_similarity(
        tfidf1,
        tfidf2
    )