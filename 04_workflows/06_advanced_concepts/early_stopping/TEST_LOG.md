# cookbook/04_workflows/06_advanced_concepts/early_stopping 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### early_stop_basic.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。┃ • Endpoint breakdown: top routes by latency and errors ┃

---

### early_stop_condition.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。ddgs.exceptions.DDGSException: No results found.

---

### early_stop_loop.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。Completed in 14.3s

---

### early_stop_parallel.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 执行成功。┃ responsible for AI-driven errors or harms. ┃

---
