# state（状态）

state 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- agentic_session_state.py - 演示 Agentic 会话状态。
- change_state_on_run.py - 演示运行时改变状态。
- nested_shared_state.py - 演示嵌套共享状态。
- overwrite_stored_session_state.py - 演示覆盖存储的会话状态。
- state_sharing.py - 演示状态共享。
