import csv

def read_csv_to_text(file_path):
    """
    读取CSV文件内容，并将每行用逗号连接，所有行用换行符拼接成一个字符串返回。
    :param file_path:
    :return:
    """
    with open(file_path,"r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [', '.join(row) for row in reader]
    all_text = "\n".join(rows)

    return all_text

if __name__ == "__main__":
    file_path = "../example_file/example.csv"
    result = read_csv_to_text(file_path)
    print(result)
