# Background Tasks Cookbook

AgentOS 中 `background_tasks` 的示例。

## 文件
- `background_evals_example.py` — 示例：在 AgentOS 中使用 AgentAsJudgeEval 的每个 Hook 后台控制。
- `background_hooks_decorator.py` — 示例：在 AgentOS 中使用后台 Post-Hook。
- `background_hooks_example.py` — 示例：在 AgentOS 中使用后台 Post-Hook。
- `background_hooks_team.py` — 示例：在 AgentOS 中与团队一起使用后台 Hook。
- `background_hooks_workflow.py` — 示例：在 AgentOS 中与工作流一起使用后台 Hook。
- `background_output_evaluation.py` — 示例：使用 Agent-as-Judge 进行后台输出评估。
- `evals_demo.py` — 创建 Session 并使用 SessionApp 的 AgentOS 来公开它的简单示例。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
