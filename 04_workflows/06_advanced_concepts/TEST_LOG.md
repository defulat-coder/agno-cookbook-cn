# cookbook/04_workflows/06_advanced_concepts 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### background_execution/background_poll.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG *** Agent Run End: 279bd889-9bd2-42b5-9b88-1d665ea235cd ****

---

### background_execution/websocket_client.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：8s）。

**结果：** 启动验证完成。[ERROR] Failed to connect: Multiple exceptions: [Errno 61] Connect call failed

---

### background_execution/websocket_server.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：8s）。

**结果：** 仅启动验证；进程在 8.14秒后终止。INFO: Finished server process [29101]

---

### early_stopping/early_stop_basic.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。┃ • Endpoint breakdown: top routes by latency and errors ┃

---

### early_stopping/early_stop_condition.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。ddgs.exceptions.DDGSException: No results found.

---

### early_stopping/early_stop_loop.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 14.3s

---

### early_stopping/early_stop_parallel.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。┃ responsible for AI-driven errors or harms. ┃

---

### guardrails/prompt_injection.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。ERROR Validation failed: Potential jailbreaking or prompt injection detected.

---

### history/continuous_execution.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。Student :

---

### history/history_in_function.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。Content Manager :

---

### history/intent_routing_with_history.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。- 'I'm getting an error message'

---

### history/step_history.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。fit their needs.

---

### long_running/disruption_catchup.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：2s）。

**结果：** 仅启动验证；进程在 2.01秒后终止。Starting test in 2 seconds...

---

### long_running/events_replay.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：2s）。

**结果：** 仅启动验证；进程在 2.01秒后终止。Starting test in 2 seconds...

---

### long_running/websocket_reconnect.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：2s）。

**结果：** 仅启动验证；进程在 2.01秒后终止。Starting test in 2 seconds...

---

### previous_step_outputs/access_previous_outputs.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Getting top 15 stories from Hacker News

---

### run_control/cancel_run.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Workflow cancellation example completed

---

### run_control/deep_copy.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。First Step: Draft Outline Copy

---

### run_control/event_storage.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-5.2

---

### run_control/executor_events.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。DEBUG Marked run 544da40f-5099-4686-a1fe-b9dcd4e537c6 as RunStatus.completed

---

### run_control/metrics.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-4o

---

### run_control/remote_workflow.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Error: Failed to connect to remote server at http://localhost:7777

---

### run_control/workflow_cli.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。┃ • Add observability and safety: logs/metrics, error handling, retries, ┃

---

### run_control/workflow_serialization.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。ERROR Error saving workflow: Label 'serialization-demo' already exists for

---

### session_state/rename_session.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 退出代码 1。AttributeError: 'NoneType' object has no attribute 'session_data'

---

### session_state/state_in_condition.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 3.2s

---

### session_state/state_in_function.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-4o

---

### session_state/state_in_router.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。- Useful large-scale quantum computing likely requires **quantum error

---

### session_state/state_with_agent.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Final workflow session state: {'shopping_list': []}

---

### session_state/state_with_team.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG [ERROR] Step 'Write Tests' not found in the list

---

### structured_io/image_input.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 22.9s

---

### structured_io/input_schema.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG ********************** TOOL METRICS **********************

---

### structured_io/pydantic_input.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。ddgs.exceptions.DDGSException: No results found.

---

### structured_io/structured_io_agent.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_agent.py:65: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length` i

---

### structured_io/structured_io_function.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_function.py:83: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length

---

### structured_io/structured_io_team.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_team.py:65: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length` in

---

### tools/workflow_tools.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。involvement from IBM, targeting error challenges in quantum computing.

---

### workflow_agent/basic_workflow_agent.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：120s）。

**结果：** 120秒后超时。DEBUG ********************** TOOL METRICS **********************

---

### workflow_agent/workflow_agent_with_condition.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：120s）。

**结果：** 执行成功。Completed in 13.5s

---
