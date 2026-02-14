# Servers Cookbook

AgentOS 中 `client_a2a/servers` 的示例。

## 文件
- `agno_server.py` — 用于测试 A2AClient 的 Agno AgentOS A2A 服务器。
- `google_adk_server.py` — 用于测试 A2AClient 的 Google ADK A2A 服务器。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
