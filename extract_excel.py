import openpyxl

def extract_text_from_excel(file_path:str) -> str:
    """
    从Excel文件中提取所有单元格内容为文本，并以字符串返回。
    :param file_path: Excel文件路径
    :return: 文本内容字符串
    """
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append("\t".join([str(cell) if cell is not None else '' for cell in row]))
    all_text = '\n'.join(rows)
    return all_text

if __name__ == "__main__":
    file_path = "example_file/example.xlsx"
    result = extract_text_from_excel(file_path)
    print(result)