# Advanced Demo Cookbook

AgentOS 中 `advanced_demo` 的示例。

## 文件
- `_agents.py` — Agent。
- `_teams.py` — 团队。
- `demo.py` — AgentOS 演示。
- `file_output.py` — 文件输出。
- `mcp_demo.py` — 此示例展示如何在 Agno OS 中使用 MCP 集成运行 Agent。
- `multiple_knowledge_bases.py` — 多个知识库。
- `reasoning_demo.py` — 运行 `uv pip install openai exa_py ddgs yfinance pypdf sqlalchemy 'fastapi[standard]' youtube-transcript-api python-docx agno` 安装依赖项。
- `reasoning_model.py` — 展示 AgentOS 中推理 Agent 的示例。
- `teams_demo.py` — 团队演示。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
