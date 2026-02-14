# Client Cookbook

AgentOS 中 `client` 的示例。

## 文件
- `01_basic_client.py` — 基本 AgentOSClient 示例。
- `02_run_agents.py` — 使用 AgentOSClient 运行 Agent。
- `03_memory_operations.py` — 使用 AgentOSClient 的记忆操作。
- `04_session_management.py` — 使用 AgentOSClient 的 Session 管理。
- `05_knowledge_search.py` — 使用 AgentOSClient 的知识库搜索。
- `06_run_teams.py` — 使用 AgentOSClient 运行团队。
- `07_run_workflows.py` — 使用 AgentOSClient 运行工作流。
- `08_run_evals.py` — 使用 AgentOSClient 运行评估。
- `09_upload_content.py` — 使用 AgentOSClient 将内容上传到知识库。
- `server.py` — 用于 Cookbook 客户端示例的 AgentOS 服务器。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
