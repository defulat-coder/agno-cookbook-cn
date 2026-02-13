# human in the loop（人机协作）

human_in_the_loop 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- confirmation_required.py - 演示需要确认的流程。
- external_tool_execution.py - 演示外部工具执行。
- user_input_required.py - 演示需要用户输入的流程。
