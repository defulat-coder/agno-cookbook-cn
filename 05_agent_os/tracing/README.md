# Tracing Cookbook

AgentOS 中 `tracing` 的示例。

## 文件
- `01_basic_agent_tracing.py` — 使用 AgentOS 进行追踪。
- `02_basic_team_tracing.py` — 02 基本团队追踪。
- `03_agent_with_knowledge_tracing.py` — 03 带有知识库的 Agent 追踪。
- `04_agent_with_reasoning_tools_tracing.py` — 04 带有推理工具的 Agent 追踪。
- `05_basic_workflow_tracing.py` — 使用 AgentOS 进行追踪。
- `06_tracing_with_multi_db_scenario.py` — 使用 AgentOS 进行追踪。
- `07_tracing_with_multi_db_and_tracing_flag.py` — 使用 AgentOS 进行追踪。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
