# context_compression

上下文压缩示例，演示工具调用上下文的压缩和监控。

## 文件列表
- `advanced_compression.py` - 演示高级压缩。
- `compression_events.py` - 演示压缩事件。
- `tool_call_compression.py` - 演示工具调用压缩。

## 前置要求
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行示例。
- 部分示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
