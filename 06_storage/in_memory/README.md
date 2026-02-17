# In-Memory Storage（内存存储）

本目录包含演示如何将 `InMemoryDb` 与 Agno agents、workflows 和 teams 一起使用的示例。

## Overview（概述）

`InMemoryDb` 提供了一个灵活、轻量级的存储解决方案，将所有 session 数据保存在内存中，并可选择将其连接到任何自定义持久化存储解决方案。

请注意，不建议将其用于生产环境。

### Highlights（亮点）

- **无需设置或额外依赖**：无需安装或数据库设置。
- **灵活的存储**：使用内置字典或提供您自己的字典以实现自定义持久化。

### Important Notes（重要说明）

- **数据持久化**：Session 数据在程序重启后**不会持久化**，除非您提供带有自己持久化机制的外部字典。
- **内存使用**：所有 session 数据都存储在 RAM 中。对于具有许多长 sessions 的应用程序，请监控内存使用情况。

## Usage（使用）

### Basic Setup（基本设置）

```python
from agno.db.in_memory import InMemoryDb

db = InMemoryDb()
```

### Bring Your Own Dictionary (Flexible Storage Integration)（自带字典（灵活的存储集成））

InMemoryDb 的真正威力来自于提供您自己的字典以实现自定义存储机制，以防当前优先支持的存储方案过于固化：

```python
from agno.db.in_memory import InMemoryDb
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import json
import boto3

# 示例：将 sessions 保存到 S3 并从 S3 加载
def save_sessions_to_s3(sessions_dict, bucket_name, key_name):
    """将 sessions 字典保存到 S3"""
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=bucket_name,
        Key=key_name,
        Body=json.dumps(sessions_dict, default=str)
    )

def load_sessions_from_s3(bucket_name, key_name):
    """从 S3 加载 sessions 字典"""
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key_name)
        return json.loads(response['Body'].read())
    except:
        return {}  # 如果文件不存在则返回空字典

# 步骤 1：使用外部字典创建 agent
my_sessions = {}
db = InMemoryDb(storage_dict=my_sessions)

agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    add_history_to_context=True,
)

# 运行一些对话
agent.print_response("What is the capital of France?")
agent.print_response("What is its population?")

print(f"Sessions in memory: {len(my_sessions)}")

# 步骤 2：将 sessions 保存到 S3
save_sessions_to_s3(my_sessions, "my-bucket", "agent-sessions.json")
print("Sessions saved to S3!")

# 步骤 3：稍后，从 S3 加载 sessions 并与新 agent 一起使用
loaded_sessions = load_sessions_from_s3("my-bucket", "agent-sessions.json")
new_db = InMemoryDb(storage_dict=loaded_sessions)

new_agent = Agent(
    model=OpenAIChat(id="gpt-5.2"),
    db=new_db,
    session_id=agent.session_id,  # 使用相同的 session ID
    add_history_to_context=True,
)

# 这个 agent 现在可以访问之前的对话
new_agent.print_response("What was my first question?")
```

### Common Operations（常见操作）

```python
# 创建存储
db = InMemoryDb()

# 获取所有 sessions
all_sessions = db.get_all_sessions()

# 按用户过滤 sessions
user_sessions = db.get_all_sessions(user_id="user123")

# 获取最近的 sessions
recent = db.get_recent_sessions(limit=5)

# 删除一个 session
db.delete_session("session_id")

# 清除所有 sessions
db.drop()
```
