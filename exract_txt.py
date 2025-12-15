# 定义一个函数，用于读取指定文本文件的内容并返回
def read_text_file(filename):
    """
    读取指定文本文件内容并返回
    :param filename: 文件名
    :return: 文件内容字符串
    """
    # 以只读模式并指定utf-8编码打开文件
    with open(filename, "r", encoding="utf-8") as f:
        # 读取文件全部内容
        text = f.read()
    # 返回读取到的文本内容
    return text

# 测试代码块，只有当本文件作为主程序运行时才会执行
if __name__ == "__main__":
    # 调用函数读取example.txt文件内容
    result = read_text_file("example.txt")
    # 打印读取到的内容
    print(result)
