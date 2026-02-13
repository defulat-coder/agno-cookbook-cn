# run control（运行控制）

run_control 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- cancel_run.py - 演示取消运行。
- model_inheritance.py - 演示模型继承。
- remote_team.py - 演示远程团队。
- retries.py - 演示重试。
