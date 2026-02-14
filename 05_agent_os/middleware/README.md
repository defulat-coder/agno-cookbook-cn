# Middleware Cookbook

AgentOS 中 `middleware` 的示例。

## 文件
- `agent_os_with_custom_middleware.py` — 此示例演示如何向 AgentOS 应用程序添加自定义中间件。
- `agent_os_with_jwt_middleware.py` — 此示例演示如何在 AgentOS 中使用 JWT 中间件。
- `agent_os_with_jwt_middleware_cookies.py` — 此示例演示如何使用带有 Cookie 而不是 Authorization 标头的 JWT 中间件。
- `custom_fastapi_app_with_jwt_middleware.py` — 此示例演示如何在自定义 FastAPI 应用程序中使用 JWT 中间件。
- `extract_content_middleware.py` — 演示如何从响应中提取内容并将其发送到通知服务的 AgentOS 示例。
- `guardrails_demo.py` — 演示如何在 Agno Agent 中使用护栏的示例。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
