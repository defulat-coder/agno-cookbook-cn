import json
from pathlib import Path

from agno.knowledge.reader.json_reader import JSONReader

reader = JSONReader()

json_path = Path("tmp/test.json")
test_data = {"key": "value"}
json_path.write_text(json.dumps(test_data))

try:
    print("开始读取...")
    documents = reader.read(json_path)

    if documents:
        for doc in documents:
            print(doc.name)
            print(doc.content)
            print(f"内容长度: {len(doc.content)}")
            print("-" * 80)
    else:
        print("未返回任何文档")

except Exception as e:
    print(f"错误类型: {type(e)}")
    print(f"发生错误: {str(e)}")
