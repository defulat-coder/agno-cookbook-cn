from agno.knowledge.reader.website_reader import WebsiteReader

reader = WebsiteReader(max_depth=3, max_links=10)


try:
    print("开始读取...")
    documents = reader.read("https://docs.agno.com/introduction")
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
