"""
学习知识：Propose 模式（深入探讨）
===========================================
Agent 提议知识，用户确认后再保存。

PROPOSE 模式添加人工质量控制：
1. Agent 识别有价值的洞察
2. Agent 向用户提议
3. 用户确认后再保存

当质量比速度更重要时使用。

对比：01_agentic_mode.py 了解自动保存。
另见：01_basics/4_learned_knowledge.py 了解基础知识。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses
from agno.vectordb.pgvector import PgVector, SearchType

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="propose_learnings",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions=(
        "When you discover a valuable insight, propose saving it. "
        "Wait for user confirmation before using save_learning."
    ),
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.PROPOSE,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "propose@example.com"
    session_id = "propose_session"

    # 用户分享经验
    print("\n" + "=" * 60)
    print("MESSAGE 1: 用户分享经验")
    print("=" * 60 + "\n")

    agent.print_response(
        "I just spent 2 hours debugging why my Docker container couldn't "
        "connect to localhost. Turns out you need to use host.docker.internal "
        "on Mac to access the host machine from inside a container.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    # Agent 应该提议保存这个

    # 用户确认
    print("\n" + "=" * 60)
    print("MESSAGE 2: 用户确认")
    print("=" * 60 + "\n")

    agent.print_response(
        "Yes, please save that. It would be helpful.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="docker localhost")

    # 拒绝示例
    print("\n" + "=" * 60)
    print("MESSAGE 3: 用户分享，然后拒绝")
    print("=" * 60 + "\n")

    agent.print_response(
        "I fixed my bug by restarting my computer.",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )

    agent.print_response(
        "No, don't save that. It's not generally useful.",
        user_id=user_id,
        session_id="session_2",
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="restart")
