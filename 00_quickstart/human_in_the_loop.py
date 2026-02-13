"""
人机协作 - 执行操作前确认
================================================
本示例展示如何在执行某些工具前要求用户确认。
对于不可逆或敏感的操作来说至关重要。

我们将在自学习 Agent 的基础上进行扩展，在保存学习心得前请求用户确认。

核心概念：
- @tool(requires_confirmation=True)：标记需要审批的工具
- run_response.active_requirements：检查待确认的请求
- requirement.confirm() / requirement.reject()：批准或拒绝
- agent.continue_run()：在用户做出决定后继续执行

实际应用场景：
- 执行敏感操作前进行确认
- API 调用前进行审核
- 验证数据转换
- 审批关键系统中的自动化操作

可尝试的示例提示：
- "What's a good P/E ratio for tech stocks? Save that insight."
- "Analyze NVDA and save any insights"
- "What learnings do we have saved?"
"""

import json
from datetime import datetime, timezone

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.text_reader import TextReader
from agno.models.google import Gemini
from agno.tools import tool
from agno.tools.yfinance import YFinanceTools
from agno.utils import pprint
from agno.vectordb.chroma import ChromaDb
from agno.vectordb.search import SearchType
from rich.console import Console
from rich.prompt import Prompt

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 学习心得知识库
# ---------------------------------------------------------------------------
learnings_kb = Knowledge(
    name="Agent Learnings HITL",
    vector_db=ChromaDb(
        name="learnings",
        collection="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
    max_results=5,
    contents_db=agent_db,
)


# ---------------------------------------------------------------------------
# 自定义工具：保存学习心得（需要确认）
# ---------------------------------------------------------------------------
@tool(requires_confirmation=True)
def save_learning(title: str, learning: str) -> str:
    """
    将可复用的洞察保存到知识库以供日后参考。
    此操作在执行前需要用户确认。

    Args:
        title: 简短的描述性标题（例如 "Tech stock P/E benchmarks"）
        learning: 要保存的洞察——需具体且可操作

    Returns:
        确认消息
    """
    if not title or not title.strip():
        return "Cannot save: title is required"
    if not learning or not learning.strip():
        return "Cannot save: learning content is required"

    payload = {
        "title": title.strip(),
        "learning": learning.strip(),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }

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

3. 保存有价值的洞察
   - 如果发现可复用的内容，使用 save_learning 保存
   - 保存前会请求用户确认
   - 好的学习心得应当具体、可操作、可推广

## 什么是好的学习心得

- 具体："科技股市盈率通常在 20-35 倍之间"，而非"市盈率各不相同"
- 可操作：能应用于未来的问题
- 可复用：不仅限于这次对话

不要保存：原始数据、一次性事实或显而易见的信息。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
human_in_the_loop_agent = Agent(
    name="Agent with Human in the Loop",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[
        YFinanceTools(),
        save_learning,
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
    console = Console()

    # 提一个可能触发保存操作的问题
    run_response = human_in_the_loop_agent.run(
        "What's a healthy P/E ratio for tech stocks? Save that insight."
    )

    # 打印初始响应内容（实际的回答）
    if run_response.content:
        pprint.pprint_run_response(run_response)

    # 处理需要确认的请求
    if run_response.active_requirements:
        for requirement in run_response.active_requirements:
            if requirement.needs_confirmation:
                console.print(
                    f"\n[bold yellow]Confirmation Required[/bold yellow]\n"
                    f"Tool: [bold blue]{requirement.tool_execution.tool_name}[/bold blue]\n"
                    f"Args: {requirement.tool_execution.tool_args}"
                )

                choice = (
                    Prompt.ask(
                        "Do you want to continue?",
                        choices=["y", "n"],
                        default="y",
                    )
                    .strip()
                    .lower()
                )

                if choice == "n":
                    requirement.reject()
                    console.print("[red]Rejected[/red]")
                else:
                    requirement.confirm()
                    console.print("[green]Approved[/green]")

        # 使用用户的决定继续运行
        run_response = human_in_the_loop_agent.continue_run(
            run_id=run_response.run_id,
            requirements=run_response.requirements,
        )

        # 打印工具执行后的最终响应
        pprint.pprint_run_response(run_response)

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
人机协作模式：

1. 敏感操作确认
   @tool(requires_confirmation=True)
   def delete_file(path: str) -> str:
       ...

2. 外部调用确认
   @tool(requires_confirmation=True)
   def send_email(to: str, subject: str, body: str) -> str:
       ...

3. 金融交易确认
   @tool(requires_confirmation=True)
   def place_order(ticker: str, quantity: int, side: str) -> str:
       ...

实现模式：
1. 使用 @tool(requires_confirmation=True) 标记工具
2. 使用 agent.run() 运行 Agent
3. 遍历 run_response.active_requirements
4. 检查 requirement.needs_confirmation
5. 调用 requirement.confirm() 或 requirement.reject()
6. 调用 agent.continue_run() 并传入 requirements

这让你可以完全控制哪些操作会被执行。
"""
