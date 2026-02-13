"""
Stream Hook 示例
=============================

演示在 Agent 生成响应后向用户发送通知的示例。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run import RunContext
from agno.run.agent import RunOutput
from agno.tools.yfinance import YFinanceTools


def send_notification(run_output: RunOutput, run_context: RunContext) -> None:
    """
    Post-hook：向用户发送通知。
    """
    if run_context.metadata is None:
        return
    email = run_context.metadata.get("email")
    if email:
        send_email(email, run_output.content)


def send_email(email: str, content: str) -> None:
    """
    向用户发送电子邮件。模拟的，仅用于示例。
    """
    print(f"Sending email to {email}: {content}")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
async def main():
    # 带有综合输出验证的 Agent

    # ---------------------------------------------------------------------------
    # 创建 Agent
    # ---------------------------------------------------------------------------

    agent = Agent(
        name="Financial Report Agent",
        model=OpenAIChat(id="gpt-5-mini"),
        post_hooks=[send_notification],
        tools=[YFinanceTools()],
        instructions=[
            "You are a helpful financial report agent.",
            "Generate a financial report for the given company.",
            "Keep it short and concise.",
        ],
    )

    # 运行 Agent
    await agent.aprint_response(
        "Generate a financial report for Apple (AAPL).",
        user_id="user_123",
        metadata={"email": "test@example.com"},
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
