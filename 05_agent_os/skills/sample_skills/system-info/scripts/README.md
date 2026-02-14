# Scripts Cookbook

AgentOS 中 `skills/sample_skills/system-info/scripts` 的示例。

## 文件
- `get_system_info.py` — 获取基本系统信息。
- `list_directory.py` — 列出目录中的文件。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
