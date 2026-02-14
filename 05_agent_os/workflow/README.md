# Workflow Cookbook

AgentOS 中 `workflow` 的示例。

## 文件
- `basic_chat_workflow_agent.py` — 演示如何使用 WorkflowAgent 将工作流添加到 AgentOS 的示例。
- `basic_workflow.py` — 基本工作流。
- `basic_workflow_team.py` — 基本工作流团队。
- `customer_research_workflow_parallel.py` — 客户研究工作流并行。
- `workflow_with_conditional.py` — 带有条件的工作流。
- `workflow_with_custom_function.py` — 带有自定义函数执行器的工作流。
- `workflow_with_custom_function_updating_session_state.py` — 带有更新 Session State 的自定义函数的工作流。
- `workflow_with_history.py` — 带有历史记录的工作流。
- `workflow_with_input_schema.py` — 带有输入 Schema 的工作流。
- `workflow_with_loop.py` — 带有循环的工作流。
- `workflow_with_nested_steps.py` — 带有嵌套步骤的工作流。
- `workflow_with_parallel.py` — 带有并行的工作流。
- `workflow_with_parallel_and_custom_function_step_stream.py` — 带有并行和自定义函数步骤流的工作流。
- `workflow_with_router.py` — 带有路由器的工作流。
- `workflow_with_steps.py` — 带有步骤的工作流。

## 前置条件
- 使用 `direnv allow` 加载环境变量（需要 `.envrc` 文件）。
- 使用 `.venvs/demo/bin/python <path-to-file>.py` 运行示例。
- 某些示例需要本地服务（例如 Postgres、Redis、Slack 或 MCP 服务器）。
