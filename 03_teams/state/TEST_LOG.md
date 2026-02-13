# 测试日志：state

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/state 中检查了 5 个文件。违规：0

---

### agentic_session_state.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/state/agentic_session_state.py`。

**结果：** 退出代码 1。尾部：ession_state |     return get_session_state_util(cast(Any, team), session_id=session_id) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/utils/agent.py", line 760, in get_session_state_util |     raise Exception("Session not found") | Exception: Session not found

---

### change_state_on_run.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/state/change_state_on_run.py`。

**结果：** 执行成功。耗时：6.42s。尾部：, line 314, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/in_memory/in_memory_db.py", line 308, in upsert_session |     return TeamSession.from_dict(session_dict_copy) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### nested_shared_state.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/state/nested_shared_state.py`。

**结果：** 退出代码 1。尾部：ession_state |     return get_session_state_util(cast(Any, team), session_id=session_id) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/utils/agent.py", line 760, in get_session_state_util |     raise Exception("Session not found") | Exception: Session not found

---

### overwrite_stored_session_state.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/state/overwrite_stored_session_state.py`。

**结果：** 退出代码 1。尾部：ession_state |     return get_session_state_util(cast(Any, team), session_id=session_id) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/utils/agent.py", line 760, in get_session_state_util |     raise Exception("Session not found") | Exception: Session not found

---

### state_sharing.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/state/state_sharing.py`。

**结果：** 执行成功。耗时：54.48s。尾部：db/sqlite/sqlite.py", line 1039, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/sqlite/sqlite.py", line 998, in upsert_session |     return TeamSession.from_dict(session_raw) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---
