# Customize Cookbook

AgentOS 中 `customize` 的示例。

## 文件
- `custom_fastapi_app.py` — 带有基本路由的自定义 FastAPI 应用的 AgentOS 应用示例。
- `custom_health_endpoint.py` — 带有自定义健康检查端点的 AgentOS 应用示例。
- `custom_lifespan.py` — Agent 具有自定义生命周期的 AgentOS 应用示例。
- `handle_custom_events.py` — 展示如何生成自定义事件的 AgentOS 示例。
- `override_routes.py` — 带有冲突路由的自定义 FastAPI 应用的 AgentOS 应用示例。
- `pass_dependencies_to_agent.py` — 展示如何将依赖项传递给 Agent 的 AgentOS 示例。
- `update_from_lifespan.py` — 从生命周期更新。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
