# knowledge（知识库）

knowledge 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- 01_team_with_knowledge.py - 演示带知识库的团队。
- 02_team_with_knowledge_filters.py - 演示带知识过滤器的团队。
- 03_team_with_agentic_knowledge_filters.py - 演示带 Agentic 知识过滤器的团队。
- 04_team_with_custom_retriever.py - 演示带自定义检索器的团队。
