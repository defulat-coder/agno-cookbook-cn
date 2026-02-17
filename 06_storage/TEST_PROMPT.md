目标：彻底测试和验证 `cookbook/06_storage`，使其符合我们的 cookbook 标准。

上下文文件（首先阅读这些文件）：
- `AGENTS.md` — 项目约定、虚拟环境、测试 workflow
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（postgres 示例需要）

执行要求：
1. **在进行任何更改之前，读取目标 cookbook 目录中的每个 `.py` 文件**。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以理解其完整内容。这确保你能捕获自动检查器可能遗漏的问题（例如，section 内的导入、注释中的过时模型引用、不一致的模式）。

2. 为 `cookbook/06_storage/` 下的每个子目录生成一个并行 agent。每个 agent 独立处理一个子目录。

3. 每个 agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/06_storage/<SUBDIR>` 并修复任何违规。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录中的所有 `*.py` 文件并捕获结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 带有 `=====` 下划线的模块文档字符串
      - Section 横幅：`# ---------------------------------------------------------------------------`
      - 文档字符串和第一个横幅之间的导入
      - `if __name__ == "__main__":` 守卫
      - 没有表情符号字符
   d. 还要检查目录中的非 Python 文件（`README.md` 等）中过时的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要符合样式规范的地方进行最小的、保留行为的编辑。
   f. 使用每个文件的最新 PASS/FAIL 条目更新 `cookbook/06_storage/<SUBDIR>/TEST_LOG.md`。

4. 还要测试根级别文件（`01_persistent_session_storage.py`、`02_session_summary.py`、`03_chat_history.py`）并更新 `cookbook/06_storage/TEST_LOG.md`。

5. 所有 agents 完成后，收集并合并结果。

特殊情况：
- `postgres/` 和 `postgres_async/` 需要运行的 PostgreSQL 实例（`./cookbook/scripts/run_pgvector.sh`）。
- `mysql/` 和 `mysql_async/` 需要运行的 MySQL 实例 — 如果 MySQL 不可用则跳过。
- `mongo/` 和 `mongo_async/` 需要运行的 MongoDB 实例 — 如果 MongoDB 不可用则跳过。
- `redis/` 需要运行的 Redis 实例 — 如果 Redis 不可用则跳过。
- `dynamodb/` 需要 AWS DynamoDB（本地或云端）— 如果不可用则跳过。
- `firestore/`、`gcs/` 需要 Google Cloud 凭证 — 如果不可用则跳过。
- `surrealdb/` 需要运行的 SurrealDB 实例 — 如果不可用则跳过。
- `sqlite/`、`json_db/`、`in_memory/` 没有外部依赖 — 这些应该始终通过。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/06_storage/<SUBDIR>`（对于每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现（不一致、失败、风险）及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的差距或手动后续工作。
4. 以此格式的结果表：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `postgres` | `session_storage.py` | PASS | Session 已持久化并检索 |
| `dynamodb` | `dynamodb_storage.py` | SKIP | DynamoDB 本地不可用 |
