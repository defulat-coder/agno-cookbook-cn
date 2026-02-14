# Client A2A Cookbook

AgentOS 中 `client_a2a` 的示例。

## 文件
- `01_basic_messaging.py` — 使用 A2AClient 的基本 A2A 消息传递。
- `02_streaming.py` — 使用 A2AClient 的流式 A2A 消息。
- `03_multi_turn.py` — 使用 A2AClient 的多轮对话。
- `04_error_handling.py` — 使用 A2AClient 的错误处理。
- `05_connect_to_google_adk.py` — 将 Agno A2AClient 连接到 Google ADK A2A 服务器。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
