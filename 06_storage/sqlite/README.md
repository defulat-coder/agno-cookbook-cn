# SQLite Integration（SQLite 集成）

演示 SQLite 数据库与 Agno agents、teams 和 workflows 集成的示例。

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file="path/to/database.db")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Async usage（异步使用）

Agno 还支持通过 `AsyncSqliteDb` 类异步使用 SQLite 数据库：

```python
from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb

db = AsyncSqliteDb(db_file="path/to/database.db")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Examples（示例）

- [`sqlite_for_agent.py`](sqlite_for_agent.py) - 使用 SQLite storage 的 Agent
- [`sqlite_for_team.py`](sqlite_for_team.py) - 使用 SQLite storage 的 Team
- [`sqlite_for_workflow.py`](sqlite_for_workflow.py) - 使用 SQLite storage 的 Workflow

