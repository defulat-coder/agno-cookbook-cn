# guardrails（防护栏）

guardrails 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- openai_moderation.py - 演示 OpenAI 内容审核。
- pii_detection.py - 演示 PII（个人身份信息）检测。
- prompt_injection.py - 演示提示注入防护。
