"""
成员历史记录
=============================

演示成员级历史记录，每个成员跟踪自己的先前上下文。
"""

from uuid import uuid4

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
german_agent = Agent(
    name="German Agent",
    role="你回答德语问题。",
    model=OpenAIChat(id="gpt-5.2"),
    add_history_to_context=True,  # 成员将可以访问自己的历史记录。
)

spanish_agent = Agent(
    name="Spanish Agent",
    role="你回答西班牙语问题。",
    model=OpenAIChat(id="gpt-5.2"),
    add_history_to_context=True,  # 成员将可以访问自己的历史记录。
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
multi_lingual_q_and_a_team = Team(
    name="Multi Lingual Q and A Team",
    model=OpenAIChat("gpt-5.2"),
    members=[german_agent, spanish_agent],
    instructions=[
        "你是一个多语言问答团队，可以回答英语和西班牙语的问题。你必须根据问题的语言将任务委托给合适的成员。",
        "如果问题是德语，委托给德语 agent。如果问题是西班牙语，委托给西班牙语 agent。",
    ],
    db=SqliteDb(
        db_file="tmp/multi_lingual_q_and_a_team.db"
    ),  # 添加数据库以存储对话历史记录。这是历史记录正常工作的必要条件。
    determine_input_for_members=False,  # 将输入直接发送给成员 agent。
    respond_directly=True,  # 将成员响应直接返回给用户。
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    session_id = f"conversation_{uuid4()}"

    # 用德语提问
    multi_lingual_q_and_a_team.print_response(
        "Hallo, wie heißt du? Mein Name ist John.",
        stream=True,
        session_id=session_id,
    )

    # 用德语跟进
    multi_lingual_q_and_a_team.print_response(
        "Erzähl mir eine Geschichte mit zwei Sätzen und verwende dabei meinen richtigen Namen.",
        stream=True,
        session_id=session_id,
    )

    # 用西班牙语提问
    multi_lingual_q_and_a_team.print_response(
        "Hola, ¿cómo se llama? Mi nombre es Juan.",
        stream=True,
        session_id=session_id,
    )

    # 用西班牙语跟进
    multi_lingual_q_and_a_team.print_response(
        "Cuenta una historia de dos oraciones y utiliza mi nombre real.",
        stream=True,
        session_id=session_id,
    )
