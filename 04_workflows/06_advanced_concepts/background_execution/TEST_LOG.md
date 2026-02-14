# cookbook/04_workflows/06_advanced_concepts/background_execution 的 TEST_LOG

生成时间：2026-02-08 16:39:09

### background_poll.py

**状态：** FAIL

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：normal，超时：35s）。

**结果：** 35秒后超时。DEBUG *** Agent Run End: 279bd889-9bd2-42b5-9b88-1d665ea235cd ****

---

### websocket_client.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：8s）。

**结果：** 启动验证完成。[ERROR] Failed to connect: Multiple exceptions: [Errno 61] Connect call failed

---

### websocket_server.py

**状态：** PASS

**描述：** 使用 `.venvs/demo/bin/python` 执行（模式：startup，超时：8s）。

**结果：** 仅启动验证；进程在 8.14秒后终止。INFO: Finished server process [29101]

---
