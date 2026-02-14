# Agui Cookbook

AgentOS 中 `interfaces/agui` 的示例。

## 文件
- `agent_with_silent_tools.py` — 静默外部工具 - 在前端中抑制冗长消息。
- `agent_with_tools.py` — 带有工具的 Agent。
- `basic.py` — 基础示例。
- `multiple_instances.py` — 多实例。
- `reasoning_agent.py` — 推理 Agent。
- `research_team.py` — 研究团队。
- `structured_output.py` — 结构化输出。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
