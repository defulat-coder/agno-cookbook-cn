# guardrails

输入/输出安全检查和策略执行示例。

## 文件列表
- `custom_guardrail.py` - 演示自定义护栏。
- `openai_moderation.py` - 演示 OpenAI 内容审核。
- `output_guardrail.py` - 演示输出护栏。
- `pii_detection.py` - 演示个人身份信息检测。
- `prompt_injection.py` - 演示提示词注入防护。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例代码。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
