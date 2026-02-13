# distributed rag（分布式 RAG）

distributed_rag 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- 01_distributed_rag_pgvector.py - 演示使用 pgvector 的分布式 RAG。
- 02_distributed_rag_lancedb.py - 演示使用 lancedb 的分布式 RAG。
- 03_distributed_rag_with_reranking.py - 演示带重排序的分布式 RAG。
