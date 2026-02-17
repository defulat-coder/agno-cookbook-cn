# JSON File Storage Integration（JSON 文件存储集成）

演示基于 JSON 文件的存储与 Agno agents、teams 和 workflows 集成的示例。

## Configuration（配置）

```python
from agno.db.json import JsonDb

db = JsonDb(db_path="tmp/json_db")
```

## Examples（示例）

- [`json_for_agent.py`](json_for_agent.py) - 使用 JSON 文件存储的 Agent
- [`json_for_team.py`](json_for_team.py) - 使用 JSON 文件存储的 Team
- [`json_for_workflows.py`](json_for_workflows.py) - 使用 JSON 文件存储的 Workflow
