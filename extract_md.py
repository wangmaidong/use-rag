# 定义一个函数，用于读取Markdown文件内容
def read_markdown_file(file_path):
    # 以只读模式并指定utf-8编码打开Markdown文件
    with open(file_path, "r", encoding="utf-8") as f:
        # 读取并返回文件的全部内容
        return f.read()


# 测试代码块，只有当本文件作为主程序运行时才会执行
if __name__ == "__main__":
    # 调用函数读取example.md文件内容
    content = read_markdown_file("example.md")
    # 打印读取到的内容
    print(content)
