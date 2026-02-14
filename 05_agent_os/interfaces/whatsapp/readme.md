# Whatsapp Cookbook

AgentOS 中 `interfaces/whatsapp` 的示例。

## 文件
- `agent_with_media.py` — 带有媒体的 Agent。
- `agent_with_user_memory.py` — 带有用户记忆的 Agent。
- `basic.py` — 基础示例。
- `image_generation_model.py` — 图像生成模型。
- `image_generation_tools.py` — 图像生成工具。
- `multiple_instances.py` — 多实例。
- `reasoning_agent.py` — 推理 Agent。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
