def read_file(file_path):
    """
    读取论文文件内容

    :param file_path: 文件路径
    :return: 文件文本内容
    """
    with open(file_path, "r", encoding="utf-8-sig") as file:
        return file.read()


def write_result(file_path, similarity):
    """
    将重复率写入答案文件

    :param file_path: 输出文件路径
    :param similarity: 相似度
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{similarity:.2f}")