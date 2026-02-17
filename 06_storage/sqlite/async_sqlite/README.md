# Async SQLite Integration（异步 SQLite 集成）

演示异步 SQLite 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install sqlalchemy aiosqlite
```

## Configuration（配置）

```python
from agno.db.sqlite import AsyncSqliteDb

db = AsyncSqliteDb(db_file="path/to/database.db")
```

## Examples（示例）

- [`async_sqlite_for_agent.py`](async_sqlite_for_agent.py) - 使用 AsyncSqliteDb storage 的 Agent
- [`async_sqlite_for_team.py`](async_sqlite_for_team.py) - 使用 AsyncSqliteDb storage 的 Team
- [`async_sqlite_for_workflow.py`](async_sqlite_for_workflow.py) - 使用 AsyncSqliteDb storage 的 Workflow
