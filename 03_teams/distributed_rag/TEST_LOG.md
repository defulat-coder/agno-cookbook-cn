# 测试日志：distributed_rag

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/distributed_rag 中检查了 3 个文件。违规：0

---

### 01_distributed_rag_pgvector.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/distributed_rag/01_distributed_rag_pgvector.py`。

**结果：** 执行成功。耗时：29.14s。尾部：                           ┃ | ┃ Feel free to ask if you have any more questions or need further              ┃ | ┃ clarification on any step!                                                   ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### 02_distributed_rag_lancedb.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/distributed_rag/02_distributed_rag_lancedb.py`。

**结果：** 退出代码 1。尾部：rom agno.vectordb.lancedb.lance_db import LanceDb, SearchType |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/vectordb/lancedb/lance_db.py", line 11, in <module> |     raise ImportError("`lancedb` not installed. Please install using `pip install lancedb`") | ImportError: `lancedb` not installed. Please install using `pip install lancedb`

---

### 03_distributed_rag_with_reranking.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/distributed_rag/03_distributed_rag_with_reranking.py`。

**结果：** 退出代码 1。尾部：ing.py", line 13, in <module> |     from agno.knowledge.reranker.cohere import CohereReranker |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/knowledge/reranker/cohere.py", line 10, in <module> |     raise ImportError("cohere not installed, please run pip install cohere") | ImportError: cohere not installed, please run pip install cohere

---
