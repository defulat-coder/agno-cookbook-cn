"""
学习机制
=============================

学习机制示例。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.learn import LearningMachine, LearningMode, UserProfileConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Learning Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(mode=LearningMode.AGENTIC),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    user_id = "learning-demo-user"

    agent.print_response(
        "我叫 Alex，我更喜欢简洁的回答。",
        user_id=user_id,
        session_id="learning_session_1",
        stream=True,
    )

    agent.print_response(
        "你还记得关于我的什么信息？",
        user_id=user_id,
        session_id="learning_session_2",
        stream=True,
    )
