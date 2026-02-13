# 测试日志：run_control

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/run_control 中检查了 4 个文件。违规：0

---

### cancel_run.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/run_control/cancel_run.py`。

**结果：** 执行成功。耗时：88.48s。尾部：d-ae21-e53ca1b3caad | Was Cancelled: False | Content Preview: In the misty realm of Emberland, where the mountains shimmered with the heat of ancient magma and lush valleys cradled verdant forests, there lived a dragon named Pyraxus. Pyraxus was not like the oth... |  | WARNING: Team run completed before cancellation |  | Team cancellation example completed!

---

### model_inheritance.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/run_control/model_inheritance.py`。

**结果：** 执行成功。耗时：46.53s。尾部：periences, foster trust,   ┃ | ┃ and contribute positively to society, ensuring innovations are both          ┃ | ┃ ground-breaking and responsible.                                             ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### remote_team.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/run_control/remote_team.py`。

**结果：** 退出代码 1。尾部：     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/client/os.py", line 201, in _arequest |     raise RemoteServerUnavailableError( | agno.exceptions.RemoteServerUnavailableError: Failed to connect to remote server at http://localhost:7778

---

### retries.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/run_control/retries.py`。

**结果：** 执行成功。耗时：16.11s。尾部：                           ┃ | ┃ These advancements highlight the progress in AI across domains like          ┃ | ┃ cybersecurity, healthcare, and research.                                     ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---
