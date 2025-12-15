import json
from base64 import encode


def read_and_print_json(file_path):
    """
    读取指定JSON文件并以格式化字符串打印内容
    :param file_path:JSON文件名
    :return:
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    text = json.dumps(data,ensure_ascii=False, indent=2)
    print(text)

if __name__ == "__main__":
    file_path = "example_file/example.json"
    result = read_and_print_json(file_path)
    print(file_path)
