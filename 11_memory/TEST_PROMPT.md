目标：全面测试和验证 `cookbook/11_memory`，确保符合 cookbook 规范。

上下文文件（请先阅读）：
- `AGENTS.md` — 项目约定、虚拟环境、测试流程
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规范

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（记忆持久化所需）

执行要求：
1. **逐一阅读目标 cookbook 目录中的每个 `.py` 文件**，再进行任何修改。
   不要仅依赖 grep 或结构检查器——打开并阅读每个文件以了解其完整内容。这样可以发现自动检查器可能遗漏的问题（如 section 内部的 import、注释中过时的模型引用、不一致的模式等）。

2. 测试根目录文件和各子目录。可按需为 `memory_manager/` 和 `optimize_memories/` 启动并行 agent。

3. 每个 agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/11_memory/<SUBDIR>` 并修复所有违规项。
   b. 使用 `.venvs/demo/bin/python` 运行所有 `*.py` 文件并记录结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 模块文档字符串带 `=====` 下划线
      - 区域分隔注释：`# ---------------------------------------------------------------------------`
      - import 语句位于文档字符串和第一个分隔注释之间
      - `if __name__ == "__main__":` 入口保护
      - 不含 emoji 字符
   d. 同时检查目录中的非 Python 文件（`README.md` 等）是否存在过时的 `OpenAIChat` 引用并更新。
   e. 仅在需要风格合规时做最小化、不改变行为的修改。
   f. 更新 `cookbook/11_memory/TEST_LOG.md`（根目录）、`cookbook/11_memory/memory_manager/TEST_LOG.md` 和 `cookbook/11_memory/optimize_memories/TEST_LOG.md`，为每个文件记录最新的 PASS/FAIL 条目。

4. 所有 agent 完成后，汇总并合并结果。

特殊情况：
- 所有记忆示例都需要运行中的 PostgreSQL 实例——确保 `./cookbook/scripts/run_pgvector.sh` 已启动。
- `05_multi_user_multi_session_chat.py` 和 `06_multi_user_multi_session_chat_concurrent.py` 模拟多用户 Session——可能耗时较长。
- `memory_manager/` 中的文件直接使用 MemoryManager API（不通过 Agent）——其模式与根目录文件不同。
- `memory_manager/surrealdb/` 中的文件正在迁移到 `cookbook/92_integrations/surrealdb/`——如仍存在则跳过。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/11_memory`
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/11_memory/memory_manager`
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/11_memory/optimize_memories`
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 校验所有代码（ruff check, mypy）

最终输出格式：
1. 发现的问题（不一致、失败、风险），附文件引用。
2. 已执行的测试/验证命令及结果。
3. 剩余差距或需手动跟进的事项。
4. 结果汇总表，格式如下：

| 子目录 | 文件 | 状态 | 备注 |
|--------|------|------|------|
| 根目录 | `01_agent_with_memory.py` | PASS | 记忆在多次 Run 中持久保存 |
| `memory_manager` | `01_standalone_memory.py` | PASS | CRUD 操作完成 |
