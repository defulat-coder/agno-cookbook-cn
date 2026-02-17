# DynamoDB Integration（DynamoDB 集成）

演示 AWS DynamoDB 与 Agno agents 集成的示例。

## Setup（设置）

```shell
uv pip install boto3
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.db.dynamodb import DynamoDb

db = DynamoDb(
    region_name="us-east-1"
)

agent = Agent(
    db=db
)
```

## Authentication（认证）

使用以下方法之一配置 AWS 凭证：

```shell
# 使用 AWS CLI
aws configure

# 使用环境变量
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"
```

## Examples（示例）

- [`dynamo_for_agent.py`](dynamo_for_agent.py) - 使用 DynamoDB storage 的 Agent
- [`dynamo_for_team.py`](dynamo_for_team.py) - 使用 DynamoDB storage 的 Team
