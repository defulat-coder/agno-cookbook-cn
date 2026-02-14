# Slack Cookbook

AgentOS 中 `interfaces/slack` 的示例。

## 文件
- `agent_with_user_memory.py` — 带有用户记忆的 Agent。
- `basic.py` — 基础示例。
- `basic_workflow.py` — 基本工作流。
- `channel_summarizer.py` — 频道摘要器。
- `file_analyst.py` — 文件分析器。
- `multiple_instances.py` — 多实例。
- `reasoning_agent.py` — 推理 Agent。
- `research_assistant.py` — 研究助手。
- `support_team.py` — 支持团队。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
