import os

from agno.knowledge.reader.firecrawl_reader import FirecrawlReader

api_key = os.getenv("FIRECRAWL_API_KEY")

reader = FirecrawlReader(
    api_key=api_key,
    mode="scrape",
    chunk=True,
    # 用于爬取
    # params={
    #     'limit': 5,
    #     'scrapeOptions': {'formats': ['markdown']}
    # }
    # 用于抓取
    params={"formats": ["markdown"]},
)

try:
    print("开始抓取...")
    documents = reader.read("https://github.com/agno-agi/agno")

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
