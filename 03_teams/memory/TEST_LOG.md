# 测试日志：memory

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/memory 中检查了 3 个文件。违规：0

---

### 01_team_with_memory_manager.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/memory/01_team_with_memory_manager.py`。

**结果：** 执行成功。耗时：7.16s。尾部：/postgres.py", line 1093, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/postgres/postgres.py", line 1050, in upsert_session |     return TeamSession.from_dict(session_dict) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### 02_team_with_agentic_memory.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/memory/02_team_with_agentic_memory.py`。

**结果：** 执行成功。耗时：17.59s。尾部：/postgres.py", line 1093, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/postgres/postgres.py", line 1050, in upsert_session |     return TeamSession.from_dict(session_dict) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### learning_machine.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/memory/learning_machine.py`。

**结果：** 执行成功。耗时：4.98s。尾部：db/sqlite/sqlite.py", line 1039, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/sqlite/sqlite.py", line 998, in upsert_session |     return TeamSession.from_dict(session_raw) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---
