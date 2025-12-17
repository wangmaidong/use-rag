from lxml import etree
def extract_xml_text(file_path):
    """
    读取XML文件并提取所有文本内容
    :param file_path:XML文件路径
    :return:提取的所有文本内容
    """
    with open(file_path, "r", encoding="utf-8") as f :
        xml = f.read()
    root = etree.fromstring(xml.encode('utf-8'))
    text = " ".join(root.itertext())
    return text

if __name__ == "__main__":
    file_path = "../example_file/example.xml"
    result = extract_xml_text(file_path)
    print(result)
