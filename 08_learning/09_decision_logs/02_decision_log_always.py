"""
决策日志：ALWAYS 模式（自动记录）
===============================================

此示例演示自动决策记录，其中
工具调用自动记录为决策。

在 ALWAYS 模式下，DecisionLogStore 从以下内容提取决策：
- 工具调用（使用了哪个工具）
- Agent 做出的其他重要选择

运行：
    .venvs/demo/bin/python cookbook/08_learning/09_decision_logs/02_decision_log_always.py
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import DecisionLogConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
# 数据库连接
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 创建带自动决策记录的 Agent
# ALWAYS 模式：工具调用自动记录为决策
agent = Agent(
    id="auto-decision-logger",
    name="Auto Decision Logger",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    learning=LearningMachine(
        decision_log=DecisionLogConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
    tools=[DuckDuckGoTools()],
    instructions=[
        "You are a helpful research assistant.",
        "Use web search to find current information when needed.",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 测试：Agent 使用工具（将自动记录）
    print("=== 测试: Agent 使用网络搜索 ===\n")
    agent.print_response(
        "What are the latest developments in AI agents?",
        session_id="session-002",
    )

    # 查看自动记录的决策
    print("\n=== 自动记录的决策 ===\n")
    decision_store = agent.get_learning_machine().decision_log_store
    if decision_store:
        decision_store.print(agent_id="auto-decision-logger", limit=10)
