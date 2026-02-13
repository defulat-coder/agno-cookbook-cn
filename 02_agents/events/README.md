# events

读取和响应 agent 运行事件的示例。

## 文件列表
- `basic_agent_events.py` - 演示基本 agent 事件。
- `reasoning_agent_events.py` - 演示推理 agent 事件。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例代码。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
