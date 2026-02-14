# Multi Agent A2A Cookbook

AgentOS 中 `interfaces/a2a/multi_agent_a2a` 的示例。

## 文件
- `airbnb_agent.py` — Airbnb Agent。
- `trip_planning_a2a_client.py` — 旅行规划 A2A 客户端。
- `weather_agent.py` — 天气 Agent。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
