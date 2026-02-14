# Remote Cookbook

AgentOS 中 `remote` 的示例。

## 文件
- `01_remote_agent.py` — 演示 AgentOSRunner 用于远程执行的示例。
- `02_remote_team.py` — 演示 AgentOSRunner 用于远程执行的示例。
- `03_remote_agno_a2a_agent.py` — 演示如何连接到远程 Agno A2A Agent 的示例。
- `04_remote_adk_agent.py` — 演示如何连接到远程 Google ADK Agent 的示例。
- `05_agent_os_gateway.py` — 演示如何使用 AgentOS 实例作为远程 Agent、团队和工作流的网关的示例。
- `adk_server.py` — 用于 Cookbook 示例的 Google ADK A2A 服务器。
- `agno_a2a_server.py` — 用于 Cookbook 示例的 Agno A2A 服务器。
- `server.py` — 用于 Cookbook 客户端示例的 AgentOS 服务器。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
