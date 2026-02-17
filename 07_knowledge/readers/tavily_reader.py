import os

from agno.knowledge.reader.tavily_reader import TavilyReader

api_key = os.getenv("TAVILY_API_KEY")

# 示例 1：使用 markdown 格式的基本提取
print("=" * 80)
print("示例 1：基本提取（markdown，基本深度）")
print("=" * 80)

reader_basic = TavilyReader(
    api_key=api_key,
    extract_format="markdown",
    extract_depth="basic",  # 每5个URL消耗1个积分
    chunk=True,
)

try:
    documents = reader_basic.read("https://github.com/agno-agi/agno")

    if documents:
        print(f"提取了 {len(documents)} 个文档")
        for doc in documents:
            print(f"\n文档: {doc.name}")
            print(f"内容长度: {len(doc.content)} 字符")
            print(f"内容预览: {doc.content[:200]}...")
            print("-" * 80)
    else:
        print("未返回任何文档")
except Exception as e:
    print(f"发生错误: {str(e)}")


# 示例 2：使用文本格式的高级提取
print("\n" + "=" * 80)
print("示例 2：高级提取（text，高级深度）")
print("=" * 80)

reader_advanced = TavilyReader(
    api_key=api_key,
    extract_format="text",
    extract_depth="advanced",  # 每5个URL消耗2个积分，更全面
    chunk=False,  # 获取完整内容而不分块
)

try:
    documents = reader_advanced.read(
        "https://docs.tavily.com/documentation/api-reference/endpoint/extract"
    )

    if documents:
        print(f"提取了 {len(documents)} 个文档")
        for doc in documents:
            print(f"\n文档: {doc.name}")
            print(f"内容长度: {len(doc.content)} 字符")
            print(f"内容预览: {doc.content[:200]}...")
            print("-" * 80)
    else:
        print("未返回任何文档")
except Exception as e:
    print(f"发生错误: {str(e)}")


# 示例 3：使用自定义参数
print("\n" + "=" * 80)
print("示例 3：自定义参数")
print("=" * 80)

reader_custom = TavilyReader(
    api_key=api_key,
    extract_format="markdown",
    extract_depth="basic",
    chunk=True,
    chunk_size=3000,  # 自定义分块大小
    params={
        # 可以在此处传递额外的 Tavily API 参数
    },
)

try:
    documents = reader_custom.read("https://www.anthropic.com")

    if documents:
        print(f"使用自定义分块大小提取了 {len(documents)} 个文档")
        for doc in documents:
            print(f"\n文档: {doc.name}")
            print(f"内容长度: {len(doc.content)} 字符")
            print("-" * 80)
    else:
        print("未返回任何文档")
except Exception as e:
    print(f"发生错误: {str(e)}")
