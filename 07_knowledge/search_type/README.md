# Search Types（搜索类型）

搜索策略决定 Agent 如何使用不同的算法和方法在知识库中查找相关信息。

## 基础集成

搜索类型与向量数据库集成以控制检索行为：

```python
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector, SearchType
from agno.agent import Agent
from agno.models.openai import OpenAIChat

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="docs",
        db_url="your_db_url",
        search_type=SearchType.hybrid
    )
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True
)

agent.print_response("Ask anything - the search type determines how I find answers")
```

## 支持的搜索类型

- **[Hybrid Search](./hybrid_search.py)** - 结合向量和关键词搜索
- **[Keyword Search](./keyword_search.py)** - 传统的基于文本的搜索
- **[Vector Search](./vector_search.py)** - 语义相似度搜索
