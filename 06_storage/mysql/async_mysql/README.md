# Async MySQL Integration（异步 MySQL 集成）

演示异步 MySQL 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install sqlalchemy asyncmy
```

## Configuration（配置）

```python
from agno.db.mysql import AsyncMySQLDb

db = AsyncMySQLDb(db_url="mysql+asyncmy://username:password@localhost:3306/database")
```

## Examples（示例）

- [`async_mysql_for_agent.py`](async_mysql_for_agent.py) - 使用 AsyncMySQLDb storage 的 Agent
- [`async_mysql_for_team.py`](async_mysql_for_team.py) - 使用 AsyncMySQLDb storage 的 Team
- [`async_mysql_for_workflow.py`](async_mysql_for_workflow.py) - 使用 AsyncMySQLDb storage 的 Workflow
