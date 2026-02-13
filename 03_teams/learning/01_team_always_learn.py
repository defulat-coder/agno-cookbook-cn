"""
团队学习：Always 模式
==========================
在 Team 上设置 learning=True 以启用自动学习。

团队自动捕获：
- 用户配置文件：姓名、角色、偏好
- 用户记忆：观察、上下文、模式

提取在每次响应后并行运行。
这是向团队添加学习的最简单方法。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.team import Team

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-4o"),
    role="Research topics and provide detailed information.",
)

writer = Agent(
    name="Writer",
    model=OpenAIChat(id="gpt-4o"),
    role="Write clear, concise content based on research.",
)

team = Team(
    name="Research Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[researcher, writer],
    db=db,
    learning=True,
    markdown=True,
    show_members_responses=True,
)

if __name__ == "__main__":
    user_id = "alice@example.com"

    # Session 1: Share information naturally
    print("\n" + "=" * 60)
    print("SESSION 1: Team learns about the user automatically")
    print("=" * 60 + "\n")

    team.print_response(
        "Hi! I'm Alice, a machine learning engineer. "
        "I prefer technical explanations with code examples. "
        "Can you explain how attention mechanisms work?",
        user_id=user_id,
        session_id="session_1",
        stream=True,
    )

    lm = team.learning_machine
    print("\n--- Learned Profile ---")
    lm.user_profile_store.print(user_id=user_id)
    print("\n--- Learned Memories ---")
    lm.user_memory_store.print(user_id=user_id)

    # Session 2: New session - team remembers
    print("\n" + "=" * 60)
    print("SESSION 2: Team remembers across sessions")
    print("=" * 60 + "\n")

    team.print_response(
        "What do you know about me? And can you explain transformers?",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
