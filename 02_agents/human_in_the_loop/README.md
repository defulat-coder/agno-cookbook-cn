# human_in_the_loop

人机协作的示例，包括确认流程、用户输入提示和外部工具处理。

## 文件
- `agentic_user_input.py` - 演示 Agent 式用户输入。
- `confirmation_advanced.py` - 演示高级确认。
- `confirmation_required.py` - 演示需要确认。
- `confirmation_toolkit.py` - 演示确认 Toolkit。
- `external_tool_execution.py` - 演示外部工具执行。
- `user_input_required.py` - 演示需要用户输入。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行 cookbook。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
