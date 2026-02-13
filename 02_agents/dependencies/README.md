# dependencies

运行时依赖注入和动态运行时输入的示例。

## 文件
- `dependencies_in_context.py` - 演示上下文中的依赖。
- `dependencies_in_tools.py` - 演示工具中的依赖。
- `dynamic_tools.py` - 演示动态工具。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行 cookbook。
- 一些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
