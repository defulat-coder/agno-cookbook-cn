# 01_quickstart

创建和运行 Agent 的核心配置入门示例。

## 文件
- `agent_with_instructions.py` - 演示带指令的 Agent。
- `agent_with_tools.py` - 演示带工具的 Agent。
- `basic_agent.py` - 演示基础 Agent。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行 cookbook。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
