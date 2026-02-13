# run_control

重试、取消、序列化、限制和执行控制的示例。

## 文件
- `agent_serialization.py` - 演示 agent 序列化。
- `cancel_run.py` - 演示取消运行。
- `concurrent_execution.py` - 演示并发执行。
- `debug.py` - 演示调试。
- `metrics.py` - 演示指标统计。
- `retries.py` - 演示重试。
- `tool_call_limit.py` - 演示工具调用限制。
- `tool_choice.py` - 演示工具选择。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
