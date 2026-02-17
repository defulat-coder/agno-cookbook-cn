"""
学习机器：学习知识（Learned Knowledge）
====================================
学习知识存储可跨用户迁移的洞察。
一个人教给 Agent 的知识，另一个人也能受益。

在 AGENTIC 模式下，Agent 接收工具：
- search_learnings: 查找相关的过去知识
- save_learning: 存储新洞察

Agent 决定何时保存和应用知识。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import LearnedKnowledgeConfig, LearningMachine, LearningMode
from agno.models.openai import OpenAIResponses
from agno.vectordb.chroma import ChromaDb, SearchType

# ---------------------------------------------------------------------------
# 创建 Knowledge 和 Agent
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/agents.db")

knowledge = Knowledge(
    name="Agent Learnings",
    vector_db=ChromaDb(
        name="learnings",
        path="tmp/chromadb",
        persistent_client=True,
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Session 1: 用户 1 教 Agent
    print("\n--- Session 1: 用户 1 保存学习 ---\n")
    agent.print_response(
        "We're trying to reduce our cloud egress costs. Remember this.",
        user_id="engineer_1@example.com",
        session_id="session_1",
        stream=True,
    )
    lm = agent.learning_machine
    lm.learned_knowledge_store.print(query="cloud")

    # Session 2: 用户 2 从学习中受益
    print("\n--- Session 2: 用户 2 问相关问题 ---\n")
    agent.print_response(
        "I'm picking a cloud provider for a data pipeline. Give me 2 key considerations.",
        user_id="engineer_2@example.com",
        session_id="session_2",
        stream=True,
    )
