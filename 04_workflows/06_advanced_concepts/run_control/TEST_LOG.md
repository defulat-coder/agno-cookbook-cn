# cookbook/04_workflows/06_advanced_concepts/run_control 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### cancel_run.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Workflow cancellation example completed

---

### deep_copy.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。First Step: Draft Outline Copy

---

### event_storage.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-5.2

---

### executor_events.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。DEBUG Marked run 544da40f-5099-4686-a1fe-b9dcd4e537c6 as RunStatus.completed

---

### metrics.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-4o

---

### remote_workflow.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Error: Failed to connect to remote server at http://localhost:7777

---

### workflow_cli.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。┃ • Add observability and safety: logs/metrics, error handling, retries, ┃

---

### workflow_serialization.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。ERROR Error saving workflow: Label 'serialization-demo' already exists for

---
