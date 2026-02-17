# Vector Databases（向量数据库）

向量数据库存储嵌入向量并为知识检索启用相似度搜索。Agno 支持多种向量数据库实现以适应不同的部署需求 - 从本地嵌入式数据库到云托管解决方案。

## 基础集成

向量数据库通过 Knowledge 系统与 Agno 集成：

```python
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

vector_db = PgVector(
    table_name="vectors", 
    db_url=db_url
)


knowledge = Knowledge(
    name="My Knowledge Base",
    vector_db=vector_db
)

agent = Agent(
    knowledge=knowledge, 
    search_knowledge=True
)
```

## 支持的向量数据库

- **[Cassandra](./cassandra_db/)** - 具有向量搜索的分布式数据库
- **[ChromaDB](./chroma_db/)** - 嵌入式向量数据库
- **[ClickHouse](./clickhouse_db/)** - 具有向量函数的列式数据库
- **[Couchbase](./couchbase_db/)** - 具有向量搜索的 NoSQL 数据库
- **[LanceDB](./lance_db/)** - 快速列式向量数据库
- **[LangChain](./langchain/)** - 使用任何 LangChain 向量存储
- **[LightRAG](./lightrag/)** - 基于图的 RAG 系统
- **[LlamaIndex](./llamaindex_db/)** - 使用 LlamaIndex 向量存储
- **[Milvus](./milvus_db/)** - 可扩展的向量数据库
- **[MongoDB](./mongo_db/)** - 具有向量搜索的文档数据库
- **[PgVector](./pgvector/)** - 具有向量相似度搜索的 PostgreSQL
- **[Pinecone](./pinecone_db/)** - 托管向量数据库
- **[Qdrant](./qdrant_db/)** - 向量搜索引擎
- **[SingleStore](./singlestore_db/)** - 具有向量能力的分布式数据库
- **[SurrealDB](./surrealdb/)** - 具有向量能力的多模型数据库
- **[Upstash](./upstash_db/)** - 无服务器向量数据库
- **[Weaviate](./weaviate_db/)** - 多模态向量数据库
