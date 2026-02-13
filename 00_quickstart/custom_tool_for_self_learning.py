"""
自学习自定义工具 - 编写你自己的工具
=====================================================
本示例展示如何为 Agent 编写自定义工具。
工具就是一个 Python 函数——Agent 会在需要时调用它。

我们将构建一个能将洞察保存到知识库的自学习 Agent。
核心理念：任何函数都可以成为工具。

核心概念：
- 工具是带有 docstring 的 Python 函数（docstring 告诉 Agent 工具的功能）
- Agent 根据对话内容决定何时调用你的工具
- 返回字符串将结果传达给 Agent

可尝试的示例提示：
- "What's a good P/E ratio for tech stocks? Save that insight."
- "Remember that NVDA's data center revenue is the key growth driver"
- "What learnings do we have saved?"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 学习心得知识库
# ---------------------------------------------------------------------------
learnings_kb = Knowledge(
    name="Agent Learnings",
    vector_db=ChromaDb(
        name="learnings",
        collection="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        hybrid_rrf_k=60,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ---------------------------------------------------------------------------
# 自定义工具：保存学习心得
# ---------------------------------------------------------------------------
def save_learning(title: str, learning: str) -> str:
    """
    将可复用的洞察保存到知识库以供日后参考。

    Args:
        title: 简短的描述性标题（例如 "Tech stock P/E benchmarks"）
        learning: 要保存的洞察——需具体且可操作

    Returns:
        确认消息
    """
    # 验证输入
    if not title or not title.strip():
        return "Cannot save: title is required"
    if not learning or not learning.strip():
        return "Cannot save: learning content is required"

    # 构建数据载荷
    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

    # 保存到知识库
    learnings_kb.insert(
        name=payload["title"],
        text_content=json.dumps(payload, ensure_ascii=False),
        reader=TextReader(),
        skip_if_exists=True,
    )

    return f"Saved: '{title}'"


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个能持续学习和改进的金融 Agent。

你有两项特殊能力：
1. 搜索知识库中之前保存的学习心得
2. 使用 save_learning 工具保存新的洞察

## 工作流程

1. 先检查知识库
   - 回答前，搜索相关的历史学习心得
   - 将相关洞察应用到回答中

2. 收集信息
   - 使用 YFinance 工具获取市场数据
   - 结合知识库中的洞察

3. 提议学习心得
   - 回答后，思考：这里有可复用的洞察吗？
   - 如果有，按以下格式提议：

---
**提议的学习心得**

标题：[简洁的标题]
内容：[洞察——需具体且可操作]

保存吗？（是/否）
---

- 仅在用户说"是"之后才调用 save_learning
- 如果用户说"否"，确认并继续

## 什么是好的学习心得

- 具体："科技股市盈率通常在 20-35 倍之间"，而非"市盈率各不相同"
- 可操作：能应用于未来的问题
- 可复用：不仅限于这次对话

不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
self_learning_agent = Agent(
    name="Self-Learning Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(),
        save_learning,  # 我们的自定义工具——就是一个 Python 函数！
    ],
    knowledge=learnings_kb,
    search_knowledge=True,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 提一个可能产生学习心得的问题
    self_learning_agent.print_response(
        "What's a healthy P/E ratio for tech stocks?",
        stream=True,
    )

    # 如果 Agent 提议了一条学习心得，批准它
    self_learning_agent.print_response(
        "yes",
        stream=True,
    )

    # 之后，Agent 可以检索已保存的学习心得
    self_learning_agent.print_response(
        "What learnings do we have saved?",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
编写自定义工具：

1. 定义一个带有类型提示和 docstring 的函数
   def my_tool(param: str) -> str:
       '''描述这个工具的功能。

       Args:
           param: 此参数的用途

       Returns:
           工具的返回值
       '''
       # 你的逻辑
       return "Result"

2. 将其添加到 Agent 的工具列表中
   agent = Agent(
       tools=[my_tool],
       ...
   )

docstring 至关重要——它告诉 Agent：
- 工具的功能是什么
- 需要哪些参数
- 返回什么

Agent 利用这些信息决定何时以及如何调用你的工具。
"""
