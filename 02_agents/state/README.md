# state

关于读取、更新和管理 session state 模式的示例。

## 文件列表
- `agentic_session_state.py` - 演示 Agentic Session State。
- `dynamic_session_state.py` - 演示动态 Session State。
- `session_state_advanced.py` - 演示 Session State 高级用法。
- `session_state_basic.py` - 演示 Session State 基础用法。
- `session_state_events.py` - 演示 Session State 事件。
- `session_state_manual_update.py` - 演示手动更新 Session State。
- `session_state_multiple_users.py` - 演示多用户 Session State。

## 前置要求
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
