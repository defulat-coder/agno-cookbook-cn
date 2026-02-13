"""
带存储的 Agent - 带持久化存储的金融 Agent
====================================================
在金融 Agent（01）的基础上，本示例添加了持久化存储。
你的 Agent 现在可以跨运行记住对话内容。

询问 NVDA 的信息，关闭脚本，稍后再回来——从上次中断的地方继续。
对话历史保存到 SQLite 中，并自动恢复。

核心概念：
- Run（运行）：每次运行 Agent（通过 agent.print_response() 或 agent.run()）
- Session（会话）：一个对话线程，由 session_id 标识
- 相同的 session_id = 连续的对话，即使跨运行也是如此

可尝试的示例提示：
- "What's the current price of AAPL?"
- "Compare that to Microsoft"（它记得 AAPL）
- "Based on our discussion, which looks better?"
- "What stocks have we analyzed so far?"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent——一个数据驱动的分析师，负责获取市场数据、
计算关键指标，并提供简洁的、可供决策的洞察。

## 工作流程

1. 澄清
   - 从公司名称识别股票代码（例如 Apple → AAPL）
   - 如有歧义，请询问

2. 获取数据
   - 获取：价格、涨跌幅、市值、市盈率、每股收益、52周范围
   - 对比分析时，为每只股票获取相同字段

3. 分析
   - 在未提供时计算比率（市盈率、市销率、利润率）
   - 关键驱动因素和风险——最多 2-3 条
   - 仅陈述事实，不做投机

4. 呈现
   - 以一行摘要开头
   - 多股对比使用表格
   - 保持精炼

## 规则

- 数据来源：Yahoo Finance。始终标注时间戳。
- 数据缺失？标注"N/A"，继续。
- 不提供个性化建议——相关时添加免责声明。
- 不使用 emoji。
- 在相关时引用之前的分析。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_storage = Agent(
    name="Agent with Storage",
    model=Gemini(id="gemini-3-flash-preview"),
    instructions=instructions,
    tools=[YFinanceTools()],
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
    # 使用固定的 session_id 以在多次运行间保持对话
    # 注意：如果未设置，session_id 会自动生成
    session_id = "finance-agent-session"

    # 第 1 轮：分析一只股票
    agent_with_storage.print_response(
        "Give me a quick investment brief on NVIDIA",
        session_id=session_id,
        stream=True,
    )

    # 第 2 轮：对比——Agent 记得第 1 轮的 NVDA
    agent_with_storage.print_response(
        "Compare that to Tesla",
        session_id=session_id,
        stream=True,
    )

    # 第 3 轮：基于完整对话给出推荐
    agent_with_storage.print_response(
        "Based on our discussion, which looks like the better investment?",
        session_id=session_id,
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
试试这个流程：

1. 运行脚本——它会分析 NVDA，与 TSLA 对比，然后给出推荐
2. 注释掉上面的三个提示
3. 添加：agent.print_response("What about AMD?", session_id=session_id, stream=True)
4. 再次运行——它记得之前 NVDA vs TSLA 的完整对话

存储层将对话历史持久化到 SQLite。
随时重启脚本，从上次中断的地方继续。
"""
