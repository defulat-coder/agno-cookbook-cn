# Schemas Cookbook

AgentOS 中 `schemas` 的示例。

## 文件
- `agent_schemas.py` — Agent 输入和输出 Schema。
- `team_schemas.py` — 团队输入和输出 Schema。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
