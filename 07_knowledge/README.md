# Agent Knowledge（知识库）

**Knowledge Base（知识库）：** 是 Agent 可以搜索以改进其响应的信息。本目录包含一系列示例，演示如何为 Agent 构建知识库。

> 注意：如果需要，请 fork 并克隆此仓库

## 快速开始

### 1. 设置环境

```bash
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/bin/activate
uv pip install -U agno openai pgvector "psycopg[binary]" sqlalchemy
```

### 2. 启动 PgVector 数据库

```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:16
```

### 3. 基础知识库

```python
from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="vectors",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"
    )
)

# 从 URL 添加内容
knowledge.add_content(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
)

# 创建带有知识库的 agent
agent = Agent(
    name="Knowledge Agent",
    knowledge=knowledge,
    search_knowledge=True,
)

agent.print_response("What can you tell me about Thai recipes?")
```

## 示例

添加文档、手册和数据库，以便 Agent 可以搜索并引用特定来源，而不是猜测。

### 快速开始
- **[01_from_path.py](./01_quickstart/01_from_path.py)** - 从本地文件添加内容
- **[02_from_url.py](./01_quickstart/02_from_url.py)** - 从 URL 添加内容
- **[04_from_multiple.py](./01_quickstart/04_from_multiple.py)** - 添加多个来源
- **[13_specify_reader.py](./01_quickstart/13_specify_reader.py)** - 使用特定文档 reader
- **[15_batching.py](./01_quickstart/15_batching.py)** - 批量嵌入工作流

### 其他主题
- **[chunking/](./chunking/)** - 文本分块策略
- **[embedders/](./embedders/)** - 嵌入模型提供商  
- **[filters/](./filters/)** - 内容过滤和访问控制
- **[readers/](./readers/)** - 文档格式处理器
- **[search_type/](./search_type/)** - 搜索算法选项
- **[vector_db/](./vector_db/)** - 向量数据库实现
