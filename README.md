# 论文查重系统

## 项目名称

基于 Python 的论文查重算法设计


## 学号

3124004183


## 项目简介

本项目实现一个基于文本相似度计算的论文查重系统。

程序通过命令行参数读取原论文文件和待检测论文文件，
计算两篇论文之间的相似度，并将结果输出到指定文件。


## 项目结构

- main.py
  - 程序入口，负责命令行参数处理

- file_utils.py
  - 文件读取和输出模块

- plagiarism_checker.py
  - 查重核心算法模块

- tests/
  - 单元测试代码

- test_files/
  - 测试数据

- PSP.xlsx
  - PSP时间记录表


## 算法设计

本项目采用 TF-IDF（Term Frequency-Inverse Document Frequency）
结合余弦相似度（Cosine Similarity）的文本相似度算法。


## 算法流程

1. 读取原论文和待检测论文文本。

2. 对文本进行预处理和分词。

3. 统计词频，并计算TF-IDF权重。

4. 将文本转换为数学向量。

5. 使用余弦相似度计算两个文本向量的相似程度。

6. 输出最终重复率。


## 模块设计


### file_utils.py

负责文件操作：

- read_file(path)

根据文件路径读取论文内容。


### plagiarism_checker.py

负责核心计算：

- tokenize(text)

文本预处理和分词。


- calculate_tfidf(words)

计算TF-IDF向量。


- cosine_similarity(vector1, vector2)

计算两个向量之间的余弦相似度。


- calculate_similarity(text1,text2)

提供最终查重接口。


### main.py

负责程序入口：

- 接收三个命令行参数：
  - 原论文路径
  - 抄袭论文路径
  - 输出文件路径

- 调用查重模块计算结果。

- 将重复率写入答案文件。


## 开发环境

Python 3.x

Windows 10

