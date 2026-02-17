from pathlib import Path

from agno.knowledge.reader.csv_reader import CSVReader

reader = CSVReader()

csv_path = Path("tmp/test.csv")


try:
    print("开始读取...")
    documents = reader.read(csv_path)

    if documents:
        for doc in documents:
            print(doc.name)
            # print(doc.content)
            print(f"内容长度: {len(doc.content)}")
            print("-" * 80)
    else:
        print("未返回任何文档")

except Exception as e:
    print(f"错误类型: {type(e)}")
    print(f"发生错误: {str(e)}")
