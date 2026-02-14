# cookbook/04_workflows/06_advanced_concepts/structured_io 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### image_input.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 22.9s

---

### input_schema.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG ********************** TOOL METRICS **********************

---

### pydantic_input.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。ddgs.exceptions.DDGSException: No results found.

---

### structured_io_agent.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_agent.py:65: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length` i

---

### structured_io_function.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_function.py:83: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length

---

### structured_io_team.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。/Users/ab/conductor/workspaces/agno/colombo/cookbook/04_workflows/06_advanced_concepts/structured_io/structured_io_team.py:65: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length` in

---
