# session

Session 持久化、摘要、选项和历史访问的示例。

## 文件
- `chat_history.py` - 演示聊天历史。
- `last_n_session_messages.py` - 演示最近 N 条 session 消息。
- `persistent_session.py` - 演示持久化 session。
- `session_options.py` - 演示 session 选项。
- `session_summary.py` - 演示 session 摘要。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行 cookbook。
- 部分示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<目录>/<文件>.py`
