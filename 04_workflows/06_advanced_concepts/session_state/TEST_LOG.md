# cookbook/04_workflows/06_advanced_concepts/session_state 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### rename_session.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 退出代码 1。AttributeError: 'NoneType' object has no attribute 'session_data'

---

### state_in_condition.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 3.2s

---

### state_in_function.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Creating new sync OpenAI client for model gpt-4o

---

### state_in_router.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。- Useful large-scale quantum computing likely requires **quantum error

---

### state_with_agent.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Final workflow session state: {'shopping_list': []}

---

### state_with_team.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG [ERROR] Step 'Write Tests' not found in the list

---
