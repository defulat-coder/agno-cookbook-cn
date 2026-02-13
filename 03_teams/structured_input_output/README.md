# structured input output（结构化输入输出）

structured_input_output 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- input_formats.py - 演示输入格式。
- input_schema.py - 演示输入模式。
- json_schema_output.py - 演示 JSON 模式输出。
- output_model.py - 演示输出模型。
- output_schema_override.py - 演示输出模式覆盖。
- parser_model.py - 演示解析器模型。
- pydantic_input.py - 演示 Pydantic 输入。
- pydantic_output.py - 演示 Pydantic 输出。
- response_as_variable.py - 演示响应作为变量。
- structured_output_streaming.py - 演示结构化输出流式传输。
