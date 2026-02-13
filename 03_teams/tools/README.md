# tools（工具）

tools 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- async_tools.py - 演示异步工具。
- custom_tools.py - 演示自定义工具。
- member_tool_hooks.py - 演示成员工具钩子。
- tool_hooks.py - 演示工具钩子。
