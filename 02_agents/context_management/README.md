# context_management

上下文管理示例，涵盖指令、动态上下文和少样本行为塑造。

## 文件列表
- `few_shot_learning.py` - 演示少样本学习。
- `filter_tool_calls_from_history.py` - 演示从历史记录中过滤工具调用。
- `instructions.py` - 演示指令。
- `instructions_with_state.py` - 演示带状态的指令。

## 前置要求
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行示例。
- 部分示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
