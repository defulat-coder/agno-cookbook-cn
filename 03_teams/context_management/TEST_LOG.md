# 测试日志：context_management

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/context_management 中检查了 3 个文件。违规：0

---

### few_shot_learning.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/context_management/few_shot_learning.py`。

**结果：** 执行成功。耗时：36.24s。尾部：                           ┃ | ┃ Could you please reply with your account details so we can proceed? Thank    ┃ | ┃ you for your patience.                                                       ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### filter_tool_calls_from_history.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/context_management/filter_tool_calls_from_history.py`。

**结果：** 执行成功。耗时：108.62s。尾部：db/sqlite/sqlite.py", line 1039, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/sqlite/sqlite.py", line 998, in upsert_session |     return TeamSession.from_dict(session_raw) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### introduction.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/context_management/introduction.py`。

**结果：** 执行成功。耗时：47.79s。尾部：db/sqlite/sqlite.py", line 1039, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/sqlite/sqlite.py", line 998, in upsert_session |     return TeamSession.from_dict(session_raw) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---
