import fitz
def extract_pdf_text(pdf_path:str) -> str:
    """
    提取PDF文件中的所有文本内容
    :param pdf_path: PDF文件路径
    :return:合并后的所有页文本
    """
    pdf = fitz.open(pdf_path)
    text_list = []
    for page in pdf:
        text_list.append(page.get_text("text"))
    all_text = '\n'.join(text_list)
    return all_text

if __name__ == "__main__":
    # 指定要读取的PDF文件名
    pdf_file = "example_file/example.pdf"
    # 调用函数提取PDF文本
    result_text = extract_pdf_text(pdf_file)
    # 打印提取到的文本内容
    print(result_text)