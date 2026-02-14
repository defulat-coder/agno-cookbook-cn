# Symmetric Cookbook

AgentOS 中 `rbac/symmetric` 的示例。

## 文件
- `advanced_scopes.py` — 使用 AgentOS 的高级 RBAC 示例 - 带有受众验证的简化作用域。
- `agent_permissions.py` — 使用 AgentOS 的每个 Agent 权限示例。
- `basic.py` — 使用 AgentOS 的基本 RBAC 示例。
- `custom_scope_mappings.py` — 自定义作用域映射示例。
- `with_cookie.py` — 使用 AgentOS 的基本 RBAC 示例。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
