"""
指标
=============================

指标统计。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools()],
    markdown=True,
    session_id="test-session-metrics",
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 直接从非流式调用中获取运行响应
    run_response = agent.run("What is the stock price of NVDA")
    print("Tool execution completed successfully!")

    # 打印每条消息的指标
    if run_response and run_response.messages:
        for message in run_response.messages:
            if message.role == "assistant":
                if message.content:
                    print(
                        f"Message: {message.content[:100]}..."
                    )  # 截断以便阅读
                elif message.tool_calls:
                    print(f"Tool calls: {len(message.tool_calls)} tool call(s)")
                print("---" * 5, "Message Metrics", "---" * 5)
                if message.metrics:
                    pprint(message.metrics)
                else:
                    print("No metrics available for this message")
                print("---" * 20)

    # 打印运行指标
    print("---" * 5, "Run Metrics", "---" * 5)
    if run_response and run_response.metrics:
        pprint(run_response.metrics)
    else:
        print("No run metrics available")

    # 打印会话指标
    print("---" * 5, "Session Metrics", "---" * 5)
    try:
        session_metrics = agent.get_session_metrics()
        if session_metrics:
            pprint(session_metrics)
        else:
            print("No session metrics available")
    except Exception as e:
        print(f"Error getting session metrics: {e}")
