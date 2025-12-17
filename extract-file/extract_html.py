from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    """
    从指定HTML文件中提取所有文本内容
    :param file_path:HTML文件路径
    :return:提取的文本内容
    """
    with open(file_path, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n")
    return text

if __name__ == "__main__":
    file_path = "example_file/example.html"
    result = extract_text_from_html(file_path)
    print(result)