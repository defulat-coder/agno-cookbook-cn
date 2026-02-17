"""
用户画像：自定义 Schema
===========================
使用 dataclass 定义你自己的画像结构。

当你想要特定字段（如角色、部门）而不是默认的自由格式画像时，使用自定义 schema。

对比：01_always_extraction.py 使用默认 schema。
另见：01_basics/1a_user_profile_always.py 了解基础知识。
"""

from dataclasses import dataclass, field
from typing import Optional

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.learn.schemas import UserProfile
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 自定义画像 Schema
# ---------------------------------------------------------------------------


@dataclass
class DeveloperProfile(UserProfile):
    """开发者画像 schema。每个字段都有 LLM 使用的描述。"""

    company: Optional[str] = field(
        default=None, metadata={"description": "Company or organization"}
    )
    role: Optional[str] = field(
        default=None, metadata={"description": "Job title (e.g., Senior Engineer)"}
    )
    primary_language: Optional[str] = field(
        default=None, metadata={"description": "Main programming language"}
    )
    languages: Optional[list[str]] = field(
        default=None, metadata={"description": "All programming languages they know"}
    )
    frameworks: Optional[list[str]] = field(
        default=None, metadata={"description": "Frameworks and libraries they use"}
    )
    experience_years: Optional[int] = field(
        default=None, metadata={"description": "Years of programming experience"}
    )


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.ALWAYS,
            schema=DeveloperProfile,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "alex@example.com"

    # 分享映射到 schema 字段的信息
    print("\n" + "=" * 60)
    print("CONVERSATION 1: 介绍")
    print("=" * 60 + "\n")

    agent.print_response(
        "Hi! I'm Alex Chen, a senior backend engineer at Stripe. "
        "I've been coding for about 12 years now.",
        user_id=user_id,
        session_id="conv_1",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # 添加技术栈详情
    print("\n" + "=" * 60)
    print("CONVERSATION 2: 技术栈")
    print("=" * 60 + "\n")

    agent.print_response(
        "I mainly work with Go and Python. For Python, I use FastAPI "
        "and SQLAlchemy a lot. I'm also familiar with Rust.",
        user_id=user_id,
        session_id="conv_2",
        stream=True,
    )
    agent.learning_machine.user_profile_store.print(user_id=user_id)

    # 测试个性化
    print("\n" + "=" * 60)
    print("CONVERSATION 3: 个性化响应")
    print("=" * 60 + "\n")

    agent.print_response(
        "How should I structure a new microservice?",
        user_id=user_id,
        session_id="conv_3",
        stream=True,
    )
