# Database Integration（数据库集成）

本目录包含演示如何将各种数据库与 Agno agents、teams 和 workflows 集成以实现持久化 storage（存储）的示例。

## Setup（设置）

```shell
# 根据你的选择安装所需的数据库驱动
uv pip install psycopg2-binary  # PostgreSQL
uv pip install pymongo         # MongoDB
uv pip install mysql-connector-python  # MySQL
uv pip install redis           # Redis
uv pip install google-cloud-firestore  # Firestore
uv pip install boto3           # DynamoDB
uv pip install singlestoredb   # SingleStore
uv pip install google-cloud-storage  # GCS
```

导航到特定的集成目录以获取详细文档和示例。

## Basic Integration（基本集成）

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb

db = PostgresDb(db_url="postgresql+psycopg://user:password@localhost:5432/dbname")

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Supported Databases（支持的数据库）

- [`postgres`](postgres/) - PostgreSQL 关系型数据库集成
- [`sqllite`](sqllite/) - SQLite 轻量级数据库集成
- [`mongo`](mongo/) - MongoDB 文档数据库集成
- [`mysql`](mysql/) - MySQL 关系型数据库集成
- [`redis`](redis/) - Redis 内存数据结构存储集成
- [`singlestore`](singlestore/) - SingleStore 分布式 SQL 数据库集成
- [`firestore`](firestore/) - Google Cloud Firestore NoSQL 数据库集成
- [`dynamodb`](dynamodb/) - AWS DynamoDB NoSQL 数据库集成
- [`json`](json/) - JSON 文件存储集成
- [`gcs`](gcs/) - Google Cloud Storage JSON blob 集成
- [`in_memory`](in_memory/) - 内存存储（带可选持久化钩子）

## Session Management（Session 管理）

- [`00_in_memory_session_storage.py`](00_in_memory_session_storage.py) - 基本 session 处理
- [`01_persistent_session_storage.py`](01_persistent_session_storage.py) - 数据库持久化
- [`02_session_summary.py`](02_session_summary.py) - Session 摘要
- [`03_chat_history.py`](03_chat_history.py) - 聊天历史管理
