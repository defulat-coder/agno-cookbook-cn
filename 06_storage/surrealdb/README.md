# SurrealDB Integration（SurrealDB 集成）

演示 SurrealDB 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install surrealdb
```

## Configuration（配置）

```python
credentials = { "username": "root", "password": "root" }
db = SurrealDb(
  None,                   # 现有连接
  "ws://localhost:8000",  # url
  credentials,            # 凭证
  "agno_ns",              # 命名空间
  "example_db",           # 数据库
)
```

## Examples（示例）

- [`surrealdb_for_agent.py`](surrealdb_for_agent.py) - 使用 SurrealDB storage 的 Agent
- [`surrealdb_for_team.py`](surrealdb_for_team.py) - 使用 SurrealDB storage 的 Team
- [`surrealdb_for_workflow.py`](surrealdb_for_workflow.py) - 使用 SurrealDB storage 的 Workflow
