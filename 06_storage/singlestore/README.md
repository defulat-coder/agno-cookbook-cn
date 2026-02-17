# SingleStore Integration（SingleStore 集成）

演示 SingleStore 数据库与 Agno agents 和 teams 集成的示例。

## Setup（设置）

```shell
uv pip install pymysql sqlalchemy
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.singlestore.singlestore import SingleStoreDb

# 使用环境变量
USERNAME = getenv("SINGLESTORE_USERNAME")
PASSWORD = getenv("SINGLESTORE_PASSWORD") 
HOST = getenv("SINGLESTORE_HOST")
PORT = getenv("SINGLESTORE_PORT")
DATABASE = getenv("SINGLESTORE_DATABASE")

db_url = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?charset=utf8mb4"

# 或使用直接连接字符串
db_url = "mysql+pymysql://username:password@host:3306/database?charset=utf8mb4"

db = SingleStoreDb(db_url=db_url)

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Examples（示例）

- [`singlestore_for_agent.py`](singlestore_for_agent.py) - 使用 SingleStore storage 的 Agent
- [`singlestore_for_team.py`](singlestore_for_team.py) - 使用 SingleStore storage 的 Team
