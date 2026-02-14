# Tracing DBs Cookbook

AgentOS 中 `tracing/dbs` 的示例。

## 文件
- `basic_agent_with_postgresdb.py` — 使用面向生产的关系型后端进行追踪。
- `basic_agent_with_sqlite.py` — 使用轻量级本地开发后端进行追踪。
- `basic_agent_with_mongodb.py` — 使用文档数据库后端进行追踪。

## 支持的后端
- 追踪模式在不同的数据库后端之间是相同的：Agent 设置保持不变，只有数据库适配器的导入/配置不同。
- 为 Postgres、SQLite 和 MongoDB 保留了代表性示例。
- 原始集合中支持的其他后端：Async MySQL、Async Postgres、Async SQLite、DynamoDB、Firestore、GCS JSON DB、JSON DB、MySQL、Redis、SingleStore 和 SurrealDB。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、MongoDB 或 SQLite）。
