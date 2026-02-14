# cookbook/04_workflows/04_parallel_execution 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### parallel_basic.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG Added RunOutput to Agent Session

---

### parallel_with_condition.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 退出代码 1。ImportError: `exa_py` not installed. Please install using `pip install exa_py`

---
