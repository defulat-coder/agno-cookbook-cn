# culture

创建和应用共享文化知识的示例。

## 文件列表
- `01_create_cultural_knowledge.py` - 演示创建文化知识。
- `02_use_cultural_knowledge_in_agent.py` - 演示在 Agent 中使用文化知识。
- `03_automatic_cultural_management.py` - 演示自动管理文化知识。
- `04_manually_add_culture.py` - 演示手动添加文化知识。

## 前置条件
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后使用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
