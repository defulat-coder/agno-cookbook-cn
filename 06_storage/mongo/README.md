# MongoDB Integration（MongoDB 集成）

演示 MongoDB 与 Agno agents 和 teams 集成的示例。

## Setup（设置）

```shell
uv pip install pymongo
```

使用以下命令运行本地 MongoDB 服务器：
```bash
docker run -d \
  --name local-mongo \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo
```
或使用我们的脚本：
```bash
./scripts/run_mongodb.sh
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.mongo import MongoDb

db = MongoDb(db_url="mongodb://username:password@localhost:27017")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Examples（示例）

- [`mongodb_for_agent.py`](mongodb_for_agent.py) - 使用 MongoDB storage 的 Agent
- [`mongodb_for_team.py`](mongodb_for_team.py) - 使用 MongoDB storage 的 Team
