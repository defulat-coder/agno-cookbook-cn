"""
团队历史记录
=============================

演示在 session 中与成员 agent 共享团队历史记录。
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
    model=OpenAIChat(id="o3-mini"),
)

spanish_agent = Agent(
    name="Spanish Agent",
    role="你回答西班牙语问题。",
    model=OpenAIChat(id="o3-mini"),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
multi_lingual_q_and_a_team = Team(
    name="Multi Lingual Q and A Team",
    model=OpenAIChat("o3-mini"),
    members=[german_agent, spanish_agent],
    instructions=[
        "你是一个多语言问答团队，可以回答英语和西班牙语的问题。你必须根据问题的语言将任务委托给合适的成员。",
        "如果问题是德语，委托给德语 agent。如果问题是西班牙语，委托给西班牙语 agent。",
        "始终将来自相应语言的响应翻译成英语，并显示原始响应和翻译后的响应。",
    ],
    db=SqliteDb(
        db_file="tmp/multi_lingual_q_and_a_team.db"
    ),  # 添加数据库以存储对话历史记录。这是历史记录正常工作的必要条件。
    pass_user_input_to_members=True,  # 将输入直接发送给成员（替代 determine_input_for_members=False）。
    respond_directly=True,
    add_team_history_to_members=True,  # 将用户和团队之间的所有交互发送给成员 agent。
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    session_id = f"conversation_{uuid4()}"

    # 首先向团队提供信息
    # 用德语提问
    multi_lingual_q_and_a_team.print_response(
        "Hallo, wie heißt du? Meine Name ist John.",
        stream=True,
        session_id=session_id,
    )

    # 然后观察他们回忆起信息（下面的问题是：
    # "用我的名字给我讲一个 2 句话的故事"）
    # 用西班牙语跟进
    multi_lingual_q_and_a_team.print_response(
        "Cuéntame una historia de 2 oraciones usando mi nombre real.",
        stream=True,
        session_id=session_id,
    )
