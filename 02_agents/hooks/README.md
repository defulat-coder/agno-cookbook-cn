# hooks

关于 pre-hooks、post-hooks 和流式生命周期 hooks 的示例。

## 文件列表
- `post_hook_output.py` - 演示 post hook 输出处理。
- `pre_hook_input.py` - 演示 pre hook 输入验证。
- `session_state_hooks.py` - 演示 session state hooks。
- `stream_hook.py` - 演示流式 hook。

## 前置要求
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
