# search coordination（搜索协调）

search_coordination 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- 01_coordinated_agentic_rag.py - 演示协调的 Agentic RAG。
- 02_coordinated_reasoning_rag.py - 演示协调的推理 RAG。
- 03_distributed_infinity_search.py - 演示分布式 Infinity 搜索。
