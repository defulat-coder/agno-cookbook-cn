目标：全面测试和验证 `cookbook/04_workflows`，使其符合我们的 cookbook 标准。

上下文文件（首先阅读这些文件）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python: `.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（会话状态和历史记录示例需要）

执行要求：
1. **在进行任何更改之前，读取目标 cookbook 目录中的每个 `.py` 文件**。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以了解其完整内容。这可以确保您发现自动检查器可能遗漏的问题（例如，sections 内的导入、注释中的过时模型引用、不一致的模式）。

2. 为 `cookbook/04_workflows/` 下的每个顶级子目录生成一个并行 Agent。每个 Agent 独立处理一个子目录，包括其中的任何嵌套子目录。

3. 每个 Agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/04_workflows/<SUBDIR>` 并修复任何违规。对于 `06_advanced_concepts/`，分别在每个嵌套子目录上运行检查器。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录（和嵌套子目录）中的所有 `*.py` 文件并捕获结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 模块文档字符串带有 `=====` 下划线
      - 部分横幅：`# ---------------------------------------------------------------------------`
      - 文档字符串和第一个横幅之间的导入
      - `if __name__ == "__main__":` 防护
      - 无表情符号字符
   d. 还要检查目录中的非 Python 文件（`README.md` 等）中是否有过时的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要符合样式的地方进行最少的、保持行为的编辑。
   f. 使用每个文件的新 PASS/FAIL 条目更新 `cookbook/04_workflows/<SUBDIR>/TEST_LOG.md`。对于 `06_advanced_concepts/`，在每个嵌套子目录中创建一个 TEST_LOG.md。

4. 所有 Agent 完成后，收集并合并结果。

特殊情况：
- `06_advanced_concepts/background_execution/` 包含 WebSocket 服务器/客户端对 — 验证服务器启动，然后终止。不要等待 WebSocket 连接。
- `06_advanced_concepts/long_running/` 示例需要运行中的 WebSocket 服务器 — 仅验证启动，然后终止。
- `06_advanced_concepts/workflow_agent/` 使用 WorkflowAgent，可能需要更长的执行时间 — 使用较长的超时时间（120秒）。
- `07_cel_expressions/` 文件使用 CEL（通用表达式语言） — 这些需要 `celpy` 包。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/04_workflows/<SUBDIR>`（对于每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check, mypy）

最终响应格式：
1. 发现（不一致、失败、风险）及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的缺口或手动后续工作。
4. 以此格式显示的结果表：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `01_basic_workflows/01_sequence_of_steps` | `sequence_of_steps.py` | PASS | 顺序工作流完成了两个步骤 |
| `07_cel_expressions/condition` | `cel_basic.py` | FAIL | 缺少 celpy 依赖 |
