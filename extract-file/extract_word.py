from docx import Document

def extract_text_from_word(file_path:str) -> str:
    """
    从Word文档中提取所有段落的文本，并以字符串返回。
    :param file_path: Word文档的路径
    :return: 文本内容字符串
    """
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

if __name__ == "__main__":
    file_path = "../example_file/example.docx"
    result = extract_text_from_word(file_path)
    print(result)