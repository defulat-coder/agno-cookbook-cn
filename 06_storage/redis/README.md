# Redis Integration（Redis 集成）

演示 Redis 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install redis

# 启动 Redis 容器
docker run --name my-redis -p 6379:6379 -d redis
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.redis import RedisDb

db = RedisDb(db_url="redis://localhost:6379")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Examples（示例）

- [`redis_for_agent.py`](redis_for_agent.py) - 使用 Redis storage 的 Agent
- [`redis_for_team.py`](redis_for_team.py) - 使用 Redis storage 的 Team
- [`redis_for_workflow.py`](redis_for_workflow.py) - 使用 Redis storage 的 Workflow
