目标：全面测试和验证 `cookbook/08_learning`，使其符合我们的 cookbook 标准。

上下文文件（首先阅读这些）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流程
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（学习存储示例需要）

执行要求：
1. **在进行任何更改之前阅读目标 cookbook 目录中的每个 `.py` 文件**。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以了解其完整内容。这确保您捕获到自动检查器可能遗漏的问题（例如，部分内的导入、注释中过时的模型引用、不一致的模式）。

2. 为 `cookbook/08_learning/` 下的每个子目录生成一个并行 agent。每个 agent 独立处理一个子目录。

3. 每个 agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/08_learning/<SUBDIR>` 并修复任何违规。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录中的所有 `*.py` 文件并捕获结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 带有 `=====` 下划线的模块文档字符串
      - 部分横幅：`# ---------------------------------------------------------------------------`
      - 文档字符串和第一个横幅之间的导入
      - `if __name__ == "__main__":` 门控
      - 无表情符号字符
   d. 同时检查目录中的非 Python 文件（`README.md` 等）是否有过时的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要符合样式的地方进行最小的、行为保持的编辑。
   f. 使用每个文件的新 PASS/FAIL 条目更新 `cookbook/08_learning/<SUBDIR>/TEST_LOG.md`。

4. 所有 agent 完成后，收集并合并结果。

特殊情况：
- 大多数学习示例需要数据库来存储学习的知识 — 确保 pgvector 正在运行。
- `08_custom_stores/` 可能使用替代存储后端 — 如果依赖不可用则跳过。
- `06_quick_tests/` 包含应该快速运行的轻量级验证脚本。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/08_learning/<SUBDIR>`（对每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现（不一致、失败、风险）以及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的差距或手动后续行动。
4. 此格式的结果表：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `00_quickstart` | `quickstart.py` | PASS | 学习存储已初始化并查询 |
| `02_user_profile` | `user_profile.py` | PASS | 用户偏好已存储和检索 |
