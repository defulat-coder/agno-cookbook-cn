# input_and_output

输入格式、验证模式和结构化输出的示例。

## 文件列表
- `input_formats.py` - 演示输入格式。
- `input_schema.py` - 演示输入模式。
- `output_schema.py` - 演示输出模式。
- `parser_model.py` - 演示解析模型。
- `response_as_variable.py` - 演示将响应存储为变量。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
