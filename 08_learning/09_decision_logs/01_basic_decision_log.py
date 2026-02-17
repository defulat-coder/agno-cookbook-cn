"""
决策日志：基本用法
==========================

此示例演示如何使用 DecisionLogStore 记录
和检索 Agent 决策。

DecisionLogStore 适用于：
- 审计 Agent 行为
- 调试意外结果
- 从过去的决策中学习
- 构建反馈循环

运行：
    .venvs/demo/bin/python cookbook/08_learning/09_decision_logs/01_basic_decision_log.py
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import DecisionLogConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
# 数据库连接
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 创建带决策日志的 Agent
# AGENTIC 模式：Agent 通过 log_decision 工具显式记录决策
agent = Agent(
    id="decision-logger",
    name="Decision Logger",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    learning=LearningMachine(
        decision_log=DecisionLogConfig(
            mode=LearningMode.AGENTIC,
            enable_agent_tools=True,
            agent_can_save=True,
            agent_can_search=True,
        ),
    ),
    instructions=[
        "You are a helpful assistant that logs important decisions.",
        "When you make a significant choice (like selecting a tool, choosing a response style, or deciding to ask for clarification), use the log_decision tool to record it.",
        "Include your reasoning and any alternatives you considered.",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 测试：要求 Agent 做出决策
    print("=== 测试 1: Agent 记录决策 ===\n")
    agent.print_response(
        "I need help choosing between Python and JavaScript for a web scraping project. What would you recommend?",
        session_id="session-001",
    )

    # 查看记录的决策
    print("\n=== 已记录的决策 ===\n")
    decision_store = agent.get_learning_machine().decision_log_store
    if decision_store:
        decision_store.print(agent_id="decision-logger", limit=5)
