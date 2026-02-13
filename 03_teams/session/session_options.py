"""
Session 选项
=============================

演示 session 命名、内存数据库使用和 session 缓存选项。
"""

from agno.agent import Agent
from agno.db.in_memory import InMemoryDb
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
postgres_db = PostgresDb(db_url=db_url)
sessions_db = PostgresDb(db_url=db_url, session_table="sessions")
in_memory_db = InMemoryDb()

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
agent = Agent(model=OpenAIChat(id="o3-mini"))
research_agent = Agent(
    model=OpenAIChat(id="o3-mini"),
    name="Research Assistant",
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
renamable_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[agent],
    db=postgres_db,
)

in_memory_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[research_agent],
    db=in_memory_db,
    add_history_to_context=True,
    num_history_runs=3,
    session_id="test_session",
)

cached_team = Team(
    model=OpenAIChat(id="o3-mini"),
    members=[research_agent],
    db=sessions_db,
    session_id="team_session_cache",
    add_history_to_context=True,
    cache_session=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    renamable_team.print_response("Tell me a new interesting fact about space")
    renamable_team.set_session_name(session_name="Interesting Space Facts")
    print(renamable_team.get_session_name())

    renamable_team.set_session_name(autogenerate=True)
    print(renamable_team.get_session_name())

    in_memory_team.print_response("Share a 2 sentence horror story", stream=True)

    print("\n" + "=" * 50)
    print("第一次运行后的聊天历史记录")
    print("=" * 50)
    try:
        chat_history = in_memory_team.get_chat_history(session_id="test_session")
        pprint([m.model_dump(include={"role", "content"}) for m in chat_history])
    except Exception as e:
        print(f"获取聊天历史记录时出错: {e}")
        print("这在使用内存数据库第一次运行时可能是预期的")

    in_memory_team.print_response("What was my first message?", stream=True)

    print("\n" + "=" * 50)
    print("第二次运行后的聊天历史记录")
    print("=" * 50)
    try:
        chat_history = in_memory_team.get_chat_history(session_id="test_session")
        pprint([m.model_dump(include={"role", "content"}) for m in chat_history])
    except Exception as e:
        print(f"获取聊天历史记录时出错: {e}")
        print("这表明内存数据库 session 处理存在问题")

    cached_team.print_response("Tell me a new interesting fact about space")
