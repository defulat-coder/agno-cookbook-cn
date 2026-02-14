# Mcp Demo Cookbook

AgentOS 中 `mcp_demo` 的示例。

## 文件
- `enable_mcp_example.py` — 启用 MCP 的 AgentOS 应用示例。
- `mcp_tools_advanced_example.py` — Agent 具有 MCPTools 的 AgentOS 应用示例。
- `mcp_tools_example.py` — Agent 具有 MCPTools 的 AgentOS 应用示例。
- `mcp_tools_existing_lifespan.py` — Agent 具有 MCPTools 的 AgentOS 应用示例。
- `test_client.py` — 首先使用 enable_mcp=True 运行 AgentOS。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
