目标：彻底测试和验证 `cookbook/05_agent_os`，使其符合我们的 cookbook 标准。

上下文文件（先读取这些）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（知识库和数据库示例需要）

执行要求：
1. **读取目标 cookbook 目录中的每个 `.py` 文件**，然后再进行任何更改。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以了解其完整内容。这确保你能捕获自动检查器可能遗漏的问题（例如，sections 内的 imports、注释中过时的模型引用、不一致的模式）。

2. 为 `cookbook/05_agent_os/` 下的每个顶级子目录生成一个并行 Agent。每个 Agent 独立处理一个子目录，包括其中的所有嵌套子目录。

3. 每个 Agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/05_agent_os/<SUBDIR> --recursive` 并修复任何违规。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录中的所有 `*.py` 文件并记录结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 带有 `=====` 下划线的模块 docstring
      - Section 横幅：`# ---------------------------------------------------------------------------`
      - 在 docstring 和第一个横幅之间导入
      - `if __name__ == "__main__":` 保护
      - 无 emoji 字符
   d. 还要检查目录中的非 Python 文件（`README.md` 等）是否有过时的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要符合样式时进行最小的、保持行为的编辑。
   f. 使用每个文件的新的 PASS/FAIL 条目更新 `cookbook/05_agent_os/<SUBDIR>/TEST_LOG.md`。

4. 所有 Agent 完成后，收集并合并结果。

特殊情况：
- `client_a2a/` 包含 server/client 对 — 验证服务器启动，然后终止。不要等待客户端连接。
- `mcp_demo/` 包含 MCP 服务器示例 — 仅验证启动。
- `background_tasks/` 示例可能生成后台任务 — 验证执行启动并在初始输出后终止。
- `rbac/` 包含对称和非对称加密示例 — 两个子目录应独立测试。
- 根级文件（`agno_agent.py`、`basic.py`、`demo.py`）应作为独立示例进行测试。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/05_agent_os/<SUBDIR> --recursive`（针对每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现的问题（不一致、失败、风险）及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的差距或手动后续工作。
4. 以此格式的结果表：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `rbac/symmetric` | `rbac_demo.py` | PASS | 对称 RBAC 正确执行 |
| `mcp_demo` | `server.py` | PASS | MCP 服务器成功启动 |
