# Firestore Integration（Firestore 集成）

演示 Google Cloud Firestore 与 Agno agents 集成的示例。

## Setup（设置）

```shell
uv pip install google-cloud-firestore
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.firestore import FirestoreDb

db = FirestoreDb(project_id="your-project-id")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Authentication（认证）

使用以下方法之一设置认证：

```shell
# 使用 gcloud CLI
gcloud auth application-default login

# 使用环境变量
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

## Examples（示例）

- [`firestore_for_agent.py`](firestore_for_agent.py) - 使用 Firestore storage 的 Agent
