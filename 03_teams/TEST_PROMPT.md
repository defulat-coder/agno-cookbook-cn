目标：全面测试和验证 `cookbook/03_teams`，确保其符合我们的手册标准。

上下文文件（先阅读这些文件）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（对于 knowledge、session、distributed_rag 示例需要）

执行要求：
1. **阅读目标手册目录中的每个 `.py` 文件**，然后再进行任何更改。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以了解其完整内容。这确保你能捕获自动化检查器可能遗漏的问题（例如，section 内的 import、注释中陈旧的模型引用、不一致的模式）。

2. 为 `cookbook/03_teams/` 下的每个子目录生成一个并行 agent。每个 agent 独立处理一个子目录。

3. 每个 agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/03_teams/<SUBDIR>` 并修复任何违规。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录中的所有 `*.py` 文件并记录结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 带有 `=====` 下划线的模块文档字符串
      - Section 标识：`# ---------------------------------------------------------------------------`
      - 在文档字符串和第一个标识之间放置 import
      - `if __name__ == "__main__":` 守护
      - 无 emoji 字符
   d. 还要检查目录中的非 Python 文件（`README.md` 等）是否有陈旧的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要符合样式时进行最小的、保持行为的编辑。
   f. 更新 `cookbook/03_teams/<SUBDIR>/TEST_LOG.md`，为每个文件添加最新的 PASS/FAIL 条目。

4. 所有 agent 完成后，收集并合并结果。

特殊情况：
- `human_in_the_loop/` 示例需要交互式输入 — 验证启动和初始工具调用，然后终止。
- 某些子目录需要 pgvector（`knowledge/`、`session/`、`distributed_rag/`、`memory/`）。
- `hooks/` 示例可能仅通过钩子回调产生输出 — 验证执行无错误完成。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/03_teams/<SUBDIR>`（对每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现（不一致、失败、风险）及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的空白或手动跟进。
4. 此格式的结果表：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `01_quickstart` | `01_basic_coordination.py` | PASS | Team 协调了来自两个成员的响应 |
| `guardrails` | `pii_detection.py` | FAIL | 缺少 presidio 依赖 |
