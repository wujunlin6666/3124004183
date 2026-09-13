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


- calculate_tfidf(tf,idf)

根据词频和逆文档频率计算TF-IDF向量。


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

## 测试说明

### 1. 单元测试

本项目使用 pytest 进行单元测试。

运行命令：
pytest tests -v

测试结果：
10 passed in 0.43s

共设计10个测试用例，主要覆盖以下功能：
1. 分词功能测试
2. 相同文本相似度测试
3. 不同文本相似度测试
4. 相似度范围测试
5. 空文本处理测试
6. 文件读取测试
7. 文件写入测试
8. 中文文本处理测试
9. 标点过滤测试
10. 长文本处理测试

### 2. 测试覆盖率

使用 coverage 工具统计代码覆盖率。

运行命令：
coverage run -m pytest tests
coverage report

测试覆盖率结果：
file_utils.py              100%
plagiarism_checker.py      100%
tests/test_plagiarism.py   100%

TOTAL                      100%

核心模块均达到100%的测试覆盖率。

### 3. 异常处理说明

程序针对以下异常情况进行了处理：

1. 命令行参数错误
程序要求输入三个参数：原论文文件路径、抄袭论文文件路径、输出文件路径。当参数数量不正确时，程序会提示正确使用方法。

2. 输入文件不存在
当输入文件路径不存在时，程序捕获 FileNotFoundError 异常，并输出错误提示。

3. 输入文件为空
当论文文件内容为空时，程序检测文本内容，并提示：Error: empty file

### 4. 性能分析与优化

1. 性能分析工具
使用 Python 自带的 cProfile 工具进行性能分析。

测试命令：
python -m cProfile -s cumulative main.py test_files/large_orig.txt test_files/large_copy.txt test_files/performance_result.txt

性能分析结果：
25810 function calls in 0.382 seconds

2. 性能瓶颈分析
通过 cProfile 分析发现，程序主要耗时集中在文本预处理阶段。其中 tokenize() 函数占用了主要运行时间。
进一步分析发现，中文分词库 jieba 的初始化和分词过程是主要耗时来源，而 TF-IDF 计算和余弦相似度计算耗时较低。

3. 优化方案
针对性能瓶颈，对分词模块进行了优化：
（1）使用全局 jieba Tokenizer 对象；
（2）避免重复初始化分词器；
（3）减少重复计算开销。

优化后程序保持算法结果稳定，并减少了分词器重复初始化带来的额外开销。

## 使用示例

运行：

python main.py test_files/orig.txt test_files/copy.txt test_files/result.txt


输出：

0.55
