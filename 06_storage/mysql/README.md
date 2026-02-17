# MySQL Integration（MySQL 集成）

演示 MySQL 数据库与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

### Synchronous MySQL（同步 MySQL）

```shell
uv pip install mysql-connector-python sqlalchemy pymysql
```

### Asynchronous MySQL（异步 MySQL）

```shell
uv pip install sqlalchemy asyncmy
```

## Configuration（配置）

### Synchronous MySQL（同步 MySQL）

```python
from agno.agent import Agent
from agno.db.mysql import MySQLDb

db = MySQLDb(db_url="mysql+pymysql://username:password@localhost:3306/database")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

### Asynchronous MySQL（异步 MySQL）

```python
import asyncio
from agno.agent import Agent
from agno.db.mysql import AsyncMySQLDb

db = AsyncMySQLDb(db_url="mysql+asyncmy://username:password@localhost:3306/database")

agent = Agent(
    db=db,
    add_history_to_context=True,
)

asyncio.run(agent.aprint_response("Hello!"))
```

## Synchronous Examples（同步示例）

- [`mysql_for_agent.py`](mysql_for_agent.py) - 使用 MySQL storage 的 Agent
- [`mysql_for_team.py`](mysql_for_team.py) - 使用 MySQL storage 的 Team

## Asynchronous Examples（异步示例）

- [`async_mysql/async_mysql_for_agent.py`](async_mysql/async_mysql_for_agent.py) - 使用异步 MySQL storage 的 Agent
- [`async_mysql/async_mysql_for_team.py`](async_mysql/async_mysql_for_team.py) - 使用异步 MySQL storage 的 Team
- [`async_mysql/async_mysql_for_workflow.py`](async_mysql/async_mysql_for_workflow.py) - 使用异步 MySQL storage 的 Workflow

## Database URL Format（数据库 URL 格式）

### Synchronous Drivers（同步驱动）

- **PyMySQL**：`mysql+pymysql://user:password@host:port/database`
- **MySQL Connector/Python**：`mysql+mysqlconnector://user:password@host:port/database`

### Asynchronous Drivers（异步驱动）

- **asyncmy**：`mysql+asyncmy://user:password@host:port/database`

## Async vs Sync（异步 vs 同步）

选择 **AsyncMySQLDb** 当：
- 构建高并发应用程序
- 使用异步框架（FastAPI、Sanic 等）
- 需要非阻塞数据库操作

选择 **MySQLDb** 当：
- 构建传统同步应用程序
- 更简单的部署要求
- 使用仅支持同步的库
