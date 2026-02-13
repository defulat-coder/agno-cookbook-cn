# Agent Teams（Agent 团队）

在 Agno 中构建多 Agent 团队的实例手册。

## 前置条件

- 使用 `direnv allow` 加载环境变量（例如 `OPENAI_API_KEY`）。
- 使用 `.venvs/demo/bin/python` 运行示例。
- 某些示例需要外部服务（例如 PostgreSQL、LanceDB、Infinity 服务器或 AgentOS 远程实例）。

## 目录说明

- `01_quickstart/` - 核心团队协调模式，包括路由/广播/任务和嵌套团队。
- `context_compression/` - 工具结果压缩和压缩管理器使用。
- `context_management/` - 上下文过滤、引入和少样本上下文。
- `dependencies/` - 上下文、工具和成员流程中的运行时依赖。
- `distributed_rag/` - 使用 PgVector/LanceDB/重排序的多成员分布式检索。
- `guardrails/` - 提示注入、内容审核和 PII 保护。
- `hooks/` - 输入前钩子、输出后钩子和流钩子。
- `human_in_the_loop/` - 确认、外部执行和需要用户输入的流程。
- `knowledge/` - 团队知识、过滤器和自定义检索器。
- `memory/` - 内存管理器、Agentic 记忆和 LearningMachine 示例。
- `metrics/` - 团队/会话/成员指标检查。
- `multimodal/` - 音频、图像和视频工作流。
- `reasoning/` - 多用途推理团队模式。
- `run_control/` - 取消、重试、模型继承和远程团队。
- `search_coordination/` - 成员间协调的 RAG/搜索模式。
- `session/` - 会话持久化、选项、摘要和历史搜索。
- `state/` - 成员和嵌套团队间共享的会话状态。
- `streaming/` - 响应流和事件监控。
- `structured_input_output/` - 结构化输入/输出模式、覆盖和流式传输。
- `tools/` - 自定义工具和工具钩子模式。
