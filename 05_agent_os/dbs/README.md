# Dbs Cookbook

AgentOS 中 `dbs` 的示例。

## 文件
- `agentos_default_db.py` — AgentOS 演示。
- `dynamo.py` — 展示如何将 AgentOS 与 DynamoDB 数据库一起使用的示例。
- `firestore.py` — 展示如何将 AgentOS 与 Firestore 数据库一起使用的示例。
- `gcs_json.py` — 展示如何将 AgentOS 与托管在 GCS 中的 JSON 文件作为数据库的示例。
- `json_db.py` — 展示如何将 AgentOS 与 JSON 文件作为数据库的示例。
- `mongo.py` — Mongo 数据库后端。
- `mysql.py` — MySQL 数据库后端。
- `neon.py` — 展示如何将 AgentOS 与 Neon 作为数据库提供商的示例。
- `postgres.py` — Postgres 数据库后端。
- `redis_db.py` — 展示如何将 AgentOS 与 Redis 作为数据库的示例。
- `singlestore.py` — 展示如何将 AgentOS 与 SingleStore 作为数据库提供商的示例。
- `sqlite.py` — 展示如何将 AgentOS 与 SQLite 数据库一起使用的示例。
- `supabase.py` — 展示如何将 AgentOS 与 Supabase 作为数据库提供商的示例。
- `surreal.py` — 展示如何将 AgentOS 与 SurrealDB 作为数据库的示例。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
