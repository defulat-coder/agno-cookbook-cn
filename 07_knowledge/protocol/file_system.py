"""
FileSystemKnowledge 示例
========================
演示如何使用 FileSystemKnowledge 让 Agent 搜索本地文件。

FileSystemKnowledge 类实现了 KnowledgeProtocol 并为 Agent 提供
三个工具：
- grep_file: 在文件内容中搜索模式
- list_files: 列出匹配 glob 模式的文件
- get_file: 读取特定文件的完整内容

运行：`python cookbook/07_knowledge/protocol/file_system.py`
"""

from agno.agent import Agent
from agno.knowledge.filesystem import FileSystemKnowledge
from agno.models.openai import OpenAIChat

# 创建指向 agno 库源代码的文件系统知识库
fs_knowledge = FileSystemKnowledge(
    base_dir="libs/agno/agno",
    include_patterns=["*.py"],
    exclude_patterns=[".git", "__pycache__", ".venv"],
)

if __name__ == "__main__":
    # ==========================================
    # 具有全部三个文件系统工具的单个 Agent
    # ==========================================
    # Agent 自动获得：grep_file、list_files、get_file
    # 以及解释如何使用它们的上下文

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        knowledge=fs_knowledge,
        search_knowledge=True,
        instructions=(
            "你是一个代码助手，帮助用户探索 agno 代码库。"
            "使用可用的工具来搜索、列出和读取文件。"
        ),
        markdown=True,
    )

    # 示例 1：Grep - 查找定义的位置
    print("\n" + "=" * 60)
    print("示例 1：使用 grep_file 查找代码模式")
    print("=" * 60 + "\n")

    agent.print_response(
        "查找 KnowledgeProtocol 类的定义位置",
        stream=True,
    )

    # 示例 2：列出目录中的文件
    print("\n" + "=" * 60)
    print("示例 2：使用 list_files 探索目录")
    print("=" * 60 + "\n")

    agent.print_response(
        "knowledge 目录中存在哪些 Python 文件？",
        stream=True,
    )

    # 示例 3：读取特定文件
    print("\n" + "=" * 60)
    print("示例 3：使用 get_file 读取文件内容")
    print("=" * 60 + "\n")

    agent.print_response(
        "读取 knowledge/protocol.py 文件并解释它定义了什么",
        stream=True,
    )

    # ==========================================
    # 示例 4：文档搜索（仅文本文件）
    # ==========================================
    # 注意：FileSystemKnowledge 仅适用于文本文件（md、txt 等）
    # 对于 PDF，请使用带有适当读取器的主 Knowledge 类
    print("\n" + "=" * 60)
    print("示例 4：搜索文档文件（咖啡指南）")
    print("=" * 60 + "\n")

    docs_knowledge = FileSystemKnowledge(
        base_dir="cookbook/07_knowledge/testing_resources",
        include_patterns=["*.md", "*.txt"],  # 仅文本文件，不包括 PDF
        exclude_patterns=[],
    )

    docs_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        knowledge=docs_knowledge,
        search_knowledge=True,
        instructions="你是一个有用的助手，从文档中回答问题。",
        markdown=True,
    )

    docs_agent.print_response(
        "你有什么关于咖啡的知识？哪个咖啡产区产生明亮和坚果味？",
        stream=True,
    )
