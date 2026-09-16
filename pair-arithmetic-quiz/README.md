# 小学四则运算题目生成器

本项目使用 Python 标准库实现，不需要安装第三方依赖。它支持随机生成题目与答案、严格分数运算、交换律去重，以及对答案文件进行批改。

## 1. 环境

- Python 3.10 或更高版本
- Windows、macOS、Linux 均可运行

检查 Python：

```powershell
python --version
```

## 2. 生成题目

在项目根目录运行：

```powershell
python main.py -n 10 -r 10
```

- `-n 10`：生成 10 道题；不写时默认为 10。
- `-r 10`：自然数、分数值和分母均小于 10；此参数必须提供。
- 输出文件是当前目录中的 `Exercises.txt` 和 `Answers.txt`。

示例：

```text
1. 1/6 + 1/8 =
```

```text
1. 7/24
```

## 3. 批改答案

```powershell
python main.py -e Exercises.txt -a Answers.txt
```

程序在当前目录生成 `Grade.txt`：

```text
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```

## 4. 运行自动测试

```powershell
python -m unittest discover -s tests -v
```

测试覆盖分数格式、优先级、括号、交换律去重、减法和除法的子表达式约束、范围参数、10000 题生成、文件写入与答案批改。

## 5. 实现思路

项目把每道题表示成一棵表达式树：叶子是自然数或分数，非叶子节点是 `+`、`−`、`×`、`÷`。生成节点时立即计算左右子树的值，因此能在减法处调整两边顺序，保证左值不小于右值；除法只在 `0 < 左值 < 右值` 时建立，保证商为真分数。

所有数值都使用 `fractions.Fraction`，没有浮点误差。去重时递归计算“规范键”：`+` 和 `×` 的左右子键先排序，其他运算保持顺序。这样 `23 + 45` 与 `45 + 23` 的键相同，而不应重复的不同树结构仍然不同。

主要文件：

- `arithmetic_quiz/expression.py`：表达式树、求值、格式化、规范键。
- `arithmetic_quiz/generator.py`：随机生成、范围控制、去重。
- `arithmetic_quiz/parser.py`：读取题目并按优先级解析。
- `arithmetic_quiz/service.py`：生成与批改文件。
- `arithmetic_quiz/cli.py`：命令行参数和错误提示。
- `tests/test_arithmetic_quiz.py`：自动测试。

## 6. 性能分析

运行：

```powershell
python scripts/profile_generation.py
```

会得到 `generation.prof` 和 `profile_report.txt`。若需要博客中的性能分析图，可安装 SnakeViz：

```powershell
python -m pip install snakeviz
snakeviz generation.prof
```

在浏览器中截取调用图，并在博客中说明耗时最多的函数以及优化前后的变化。不要伪造数据，应在自己的电脑上重新运行并记录。

## 7. 打包成 exe（可选）

```powershell
python -m pip install pyinstaller
pyinstaller --onefile --name Myapp main.py
```

生成后可这样运行：

```powershell
.\dist\Myapp.exe -n 10 -r 10
```

## 8. Git 提交建议

不要最后一次性提交全部代码。可以按真实开发过程提交：

```text
feat: 建立表达式树和分数格式化
feat: 实现随机生成及交换律去重
feat: 增加命令行文件输出
feat: 实现答案批改功能
test: 补充分数、生成器和批改测试
docs: 添加运行说明与设计文档
```
