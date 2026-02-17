# PostgreSQL Integration（PostgreSQL 集成）

演示 PostgreSQL 数据库与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install psycopg2-binary
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb

db = PostgresDb(db_url="postgresql+psycopg://username:password@localhost:5432/database")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Async usage（异步使用）

Agno 还支持通过 `AsyncPostgresDb` 类异步使用 PostgreSQL 数据库：

```python
from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb

db = AsyncPostgresDb(db_url="postgresql+psycopg://username:password@localhost:5432/database")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Examples（示例）

- [`postgres_for_agent.py`](postgres_for_agent.py) - 使用 PostgreSQL storage 的 Agent
- [`postgres_for_team.py`](postgres_for_team.py) - 使用 PostgreSQL storage 的 Team
- [`postgres_for_workflow.py`](postgres_for_workflow.py) - 使用 PostgreSQL storage 的 Workflow
