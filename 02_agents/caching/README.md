# 缓存

模型响应缓存和重复查询效率优化示例。

## 文件
- `cache_model_response.py` - 演示缓存模型响应。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行 cookbook。
- 部分示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `uv run python 02_agents/<目录>/<文件>.py`
