# Filters（过滤器）

过滤器帮助您根据元数据、内容模式或自定义条件有选择地检索和处理知识，以实现目标信息检索。

## 设置

```bash
uv pip install agno lancedb pandas
```

设置您的 API 密钥：
```bash
export OPENAI_API_KEY=your_api_key
```

## 基础集成

过滤器与 Knowledge 系统集成以启用目标搜索：

```python
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb

knowledge = Knowledge(vector_db=LanceDb(table_name="docs", uri="tmp/lancedb"))
knowledge.add_content(path="data.csv", metadata={"type": "sales", "quarter": "Q1"})

results = knowledge.search(
    query="revenue trends",
    filters={"quarter": "Q1"}
)
```

## Agent 集成

Agent 可以使用过滤的知识进行目标响应：

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    knowledge=knowledge,
    search_knowledge=True
)

# Agent 在知识搜索期间自动应用过滤器
response = agent.print_response(
    "What are the Q1 sales trends?",
    knowledge_filters={"quarter": "Q1"},
    markdown=True,
)
```

## 过滤表达式

对于复杂的过滤逻辑，使用 `agno.filters` 中的 `FilterExpr` 对象：

```python
from agno.filters import EQ, IN, GT, LT, AND, OR, NOT

# 简单相等
filter = EQ("status", "published")

# 范围查询
filter = AND(GT("views", 1000), LT("views", 10000))

# 复杂逻辑
filter = OR(AND(EQ("type", "article"), GT("word_count", 500)), IN("priority", ["high", "urgent"]))

# 否定
filter = NOT(EQ("status", "archived"))

# 与 agent 一起使用
agent.run("Query", knowledge_filters=[filter])
```

**操作符：**
- `EQ(key, value)` - 相等
- `IN(key, [values])` - 值在列表中
- `GT(key, value)` - 大于
- `LT(key, value)` - 小于
- `AND(...)` - AND 逻辑
- `OR(...)` - OR 逻辑
- `NOT(...)` - NOT 逻辑

## 支持的过滤器类型

- **[Agentic Filtering](./agentic_filtering.py)** - Agent 集成过滤
- **[Async Filtering](./async_filtering.py)** - 异步过滤操作
- **[Basic Filtering](./filtering.py)** - 基于元数据的过滤
- **[Filter Expressions](./filtering_with_conditions_on_agent.py)** - 使用 FilterExpr 的复杂过滤
- **[API Filter Examples](../../agent_os/knowledge/knowledge_filters.py)** - 通过 HTTP API 使用过滤器
- **[Filtering on Load](./filtering_on_load.py)** - 在内容加载期间设置元数据
- **[Invalid Keys Handling](./filtering_with_invalid_keys.py)** - 带错误处理的过滤
