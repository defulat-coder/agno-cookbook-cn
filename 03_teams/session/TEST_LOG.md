# 测试日志：session

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/session 中检查了 6 个文件。违规：0

---

### chat_history.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/chat_history.py`。

**结果：** 退出代码 1。尾部：no/colombo/libs/agno/agno/team/team.py", line 2482, in get_session_messages |     return _storage.get_session_messages( |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/team/_storage.py", line 1601, in get_session_messages |     raise Exception("Session not found") | Exception: Session not found

---

### persistent_session.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/persistent_session.py`。

**结果：** 执行成功。耗时：29.48s。尾部：/postgres.py", line 1093, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/postgres/postgres.py", line 1050, in upsert_session |     return TeamSession.from_dict(session_dict) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### search_session_history.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/search_session_history.py`。

**结果：** 退出代码 1。尾部：dbapi_meth(**dbapi_args) |             ^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/.venvs/demo/lib/python3.12/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py", line 449, in import_dbapi |     __import__("aiosqlite"), __import__("sqlite3") |     ^^^^^^^^^^^^^^^^^^^^^^^ | ModuleNotFoundError: No module named 'aiosqlite'

---

### session_options.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/session_options.py`。

**结果：** 退出代码 1。尾部：^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/team/_storage.py", line 1386, in set_session_name |     set_session_name_util( |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/utils/agent.py", line 685, in set_session_name_util |     raise Exception("No session found") | Exception: No session found

---

### session_summary.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/session_summary.py`。

**结果：** 退出代码 1。尾部：session_summary(self, session_id=session_id) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/team/_storage.py", line 1729, in aget_session_summary |     raise Exception(f"Session {session_id} not found") | Exception: Session async_team_session_summary not found

---

### share_session_with_agent.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/session/share_session_with_agent.py`。

**结果：** 执行成功。耗时：10.59s。尾部：.py", line 145, in get_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/in_memory/in_memory_db.py", line 132, in get_session |     return AgentSession.from_dict(session_data_copy) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---
