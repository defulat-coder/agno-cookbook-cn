"""
模式：带学习的支持 Agent
====================================
一个从交互中学习的客户支持 Agent。

此模式结合：
- 用户画像：客户历史和偏好
- Session Context：当前工单/问题跟踪
- 实体记忆：产品、过去的工单（跨组织共享）
- 学习知识：解决方案和故障排除模式（共享）

Agent 通过从成功中学习来更快地解决问题。

另见：01_basics/ 了解各个存储示例。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import (
    EntityMemoryConfig,
    LearnedKnowledgeConfig,
    LearningMachine,
    LearningMode,
    SessionContextConfig,
    UserProfileConfig,
)
from agno.models.openai import OpenAIResponses
from agno.vectordb.pgvector import PgVector, SearchType

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# 解决方案的共享知识库
knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="support_kb",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)


def create_support_agent(customer_id: str, ticket_id: str, org_id: str) -> Agent:
    """为特定工单创建支持 Agent。"""
    return Agent(
        model=OpenAIResponses(id="gpt-5.2"),
        db=db,
        instructions=(
            "You are a helpful support agent. "
            "Check if similar issues have been solved before. "
            "Save successful solutions for future reference."
        ),
        learning=LearningMachine(
            knowledge=knowledge,
            user_profile=UserProfileConfig(
                mode=LearningMode.ALWAYS,
            ),
            session_context=SessionContextConfig(
                enable_planning=True,
            ),
            entity_memory=EntityMemoryConfig(
                mode=LearningMode.ALWAYS,
                namespace=f"org:{org_id}:support",
            ),
            learned_knowledge=LearnedKnowledgeConfig(
                mode=LearningMode.AGENTIC,
            ),
        ),
        user_id=customer_id,
        session_id=ticket_id,
        markdown=True,
    )


# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    org_id = "acme"

    # Ticket 1: 第一个客户的登录问题
    print("\n" + "=" * 60)
    print("TICKET 1: 第一个登录问题")
    print("=" * 60 + "\n")

    agent = create_support_agent("customer_1@example.com", "ticket_001", org_id)
    agent.print_response(
        "I can't log into my account. It says 'invalid credentials' "
        "even though I know my password is correct. I'm using Chrome.",
        stream=True,
    )

    # Agent 建议解决方案
    print("\n" + "=" * 60)
    print("TICKET 1: 解决方案有效")
    print("=" * 60 + "\n")

    agent.print_response(
        "Clearing the cache worked! Thanks so much!",
        stream=True,
    )
    agent.learning_machine.learned_knowledge_store.print(query="login chrome cache")

    # Ticket 2: 第二个客户遇到类似问题
    print("\n" + "=" * 60)
    print("TICKET 2: 类似问题（应找到先前的解决方案）")
    print("=" * 60 + "\n")

    agent2 = create_support_agent("customer_2@example.com", "ticket_002", org_id)
    agent2.print_response(
        "Login not working in Chrome, says wrong password but I'm sure it's right.",
        stream=True,
    )

    # Agent 应该找到并应用先前的解决方案
