# Async Postgres Integration（异步 Postgres 集成）

演示异步 PostgreSQL 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install sqlalchemy psycopg
```

## Configuration（配置）

```python
from agno.db.postgres import AsyncPostgresDb

db = AsyncPostgresDb(db_url="postgresql+psycopg_async://username:password@localhost:5432/database")
```

## Examples（示例）

- [`async_postgres_for_agent.py`](async_postgres_for_agent.py) - 使用 AsyncPostgresDb storage 的 Agent
- [`async_postgres_for_team.py`](async_postgres_for_team.py) - 使用 AsyncPostgresDb storage 的 Team
- [`async_postgres_for_workflow.py`](async_postgres_for_workflow.py) - 使用 AsyncPostgresDb storage 的 Workflow
