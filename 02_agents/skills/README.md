# skills

定义和使用 agent skills 和辅助脚本的示例。

## 文件
- `basic_skills.py` - 演示基础 skills。
- `sample_skills/code-review/scripts/check_style.py` - 演示检查风格。
- `sample_skills/git-workflow/scripts/commit_message.py` - 演示提交消息。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行 cookbook。
- 一些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
