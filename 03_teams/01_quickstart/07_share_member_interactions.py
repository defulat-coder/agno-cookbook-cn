"""
共享成员交互
=============================

演示在执行期间在团队成员之间共享交互。
"""

from uuid import uuid4

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team


# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
def get_user_profile() -> dict:
    """获取用户配置文件。"""
    return {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "billing_address": "123 Main St, Anytown, USA",
        "login_type": "email",
        "mfa_enabled": True,
    }


user_profile_agent = Agent(
    name="User Profile Agent",
    role="你是一个用户配置文件 agent，可以检索关于用户和用户账户的信息。",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[get_user_profile],
)

technical_support_agent = Agent(
    name="Technical Support Agent",
    role="你是一个技术支持 agent，可以回答关于技术支持的问题。",
    model=OpenAIChat(id="gpt-5.2"),
)

billing_agent = Agent(
    name="Billing Agent",
    role="你是一个账单 agent，可以回答关于账单的问题。",
    model=OpenAIChat(id="gpt-5.2"),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
support_team = Team(
    name="Technical Support Team",
    model=OpenAIChat("o3-mini"),
    members=[user_profile_agent, technical_support_agent, billing_agent],
    instructions=[
        "你是一个 Facebook 账户的技术支持团队，可以回答关于 Facebook 技术支持和账单的问题。",
        "如果问题是关于用户配置文件或账户的，首先获取用户的配置文件信息。",
    ],
    db=SqliteDb(
        db_file="tmp/technical_support_team.db"
    ),  # 添加数据库以存储对话历史记录。
    share_member_interactions=True,  # 在当前运行期间发送成员交互。
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    session_id = f"conversation_{uuid4()}"

    # 询问关于技术支持的问题
    support_team.print_response(
        "What is my billing address and how do I change it?",
        stream=True,
        session_id=session_id,
    )

    support_team.print_response(
        "Do I have multi-factor enabled? How do I disable it?",
        stream=True,
        session_id=session_id,
    )
