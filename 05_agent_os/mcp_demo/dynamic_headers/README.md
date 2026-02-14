# Dynamic Headers Cookbook

AgentOS 中 `mcp_demo/dynamic_headers` 的示例。

## 文件
- `client.py` — 使用动态标头的 MCPTools 的 AgentOS。
- `server.py` — 记录从客户端接收的标头的简单 MCP 服务器。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
