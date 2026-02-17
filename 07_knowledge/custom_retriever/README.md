# Custom Retrievers（自定义检索器）

自定义检索器提供对 Agent 如何从知识源查找和处理信息的完全控制。

## 设置

```bash
uv pip install agno qdrant-client openai
```

本地启动 Qdrant：
```bash
docker run -p 6333:6333 qdrant/qdrant
```

设置您的 API 密钥：
```bash
export OPENAI_API_KEY=your_api_key
```

## 基础集成

自定义检索器与 Agent 集成以替换默认的知识搜索：

```python
from agno.agent import Agent

def custom_knowledge_retriever(query: str, num_documents: int = 5) -> str:
    # 您的自定义检索逻辑
    results = your_search_logic(query, num_documents)
    return format_results(results)

agent = Agent(
    knowledge_retriever=custom_knowledge_retriever,
    search_knowledge=True
)

agent.print_response(query, markdown=True)
```

## 支持的自定义检索器

- **[Async Retriever](./async_retriever.py)** - 异步检索与并发处理
- **[Basic Retriever](./retriever.py)** - 自定义检索逻辑和处理
- **[Retriever with Dependencies](./retriever_with_dependencies.py)** - 在自定义检索器中访问运行时依赖项
