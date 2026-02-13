# rag

传统和 agentic 检索增强生成的示例。

## 文件
- `agentic_rag.py` - 演示 agentic rag。
- `agentic_rag_with_reasoning.py` - 演示带推理的 agentic rag。
- `agentic_rag_with_reranking.py` - 演示带重排序的 agentic rag。
- `rag_custom_embeddings.py` - 演示自定义嵌入的 rag。
- `traditional_rag.py` - 演示传统 rag。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
