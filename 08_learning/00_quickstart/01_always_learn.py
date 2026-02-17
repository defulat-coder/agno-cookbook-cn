"""
学习机器（Learning Machines）
=================
设置 learning=True 将 Agent 转变为学习机器。

Agent 自动捕获：
- 用户画像：姓名、角色、偏好
- 用户记忆：观察、上下文、模式

无需显式工具调用。提取并行运行。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agents.db")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    user_id = "alice1@example.com"

    # Session 1: 自然分享信息
    print("\n--- Session 1: 自动提取发生 ---\n")
    agent.print_response(
        "Hi! I'm Alice. I work at Anthropic as a research scientist. "
        "I prefer concise responses without too much explanation.",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )
    lm = agent.learning_machine
    lm.user_profile_store.print(user_id=user_id)
    lm.user_memory_store.print(user_id=user_id)

    # Session 2: 新 Session - Agent 记住了
    print("\n--- Session 2: Agent 跨 Session 记忆 ---\n")
    agent.print_response(
        "What do you know about me?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
