"""
流式 Hook
=============================

演示团队响应生成后的 post-hook 通知。
"""

import asyncio

from agno.models.openai import OpenAIChat
from agno.run import RunContext
from agno.run.team import TeamRunOutput
from agno.team import Team
from agno.tools.yfinance import YFinanceTools


# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
def send_email(email: str, content: str) -> None:
    """向用户发送电子邮件。示例用途的模拟实现。"""
    print(f"发送电子邮件到 {email}: {content}")


def send_notification(run_output: TeamRunOutput, run_context: RunContext) -> None:
    """Post-hook: 向用户发送通知。"""
    if run_context.metadata is None:
        return
    email = run_context.metadata.get("email")
    if email:
        send_email(email, run_output.content)


# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    name="Financial Report Team",
    model=OpenAIChat(id="gpt-5.2"),
    members=[],
    post_hooks=[send_notification],
    tools=[YFinanceTools()],
    instructions=[
        "你是一个有用的财务报告 agent 团队。",
        "为给定公司生成财务报告。",
        "保持简短明了。",
    ],
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
async def main() -> None:
    await team.aprint_response(
        "Generate a financial report for Apple (AAPL).",
        user_id="user_123",
        metadata={"email": "test@example.com"},
        stream=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
