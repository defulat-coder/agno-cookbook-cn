# context compression（上下文压缩）

context_compression 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- tool_call_compression.py - 演示工具调用压缩。
- tool_call_compression_with_manager.py - 演示带管理器的工具调用压缩。
