# 测试日志：streaming

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/streaming 中检查了 2 个文件。违规：0

---

### team_events.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/streaming/team_events.py`。

**结果：** 执行成功。耗时：1.15s。尾部：x-api-key'}, 'request_id': 'req_011CXvqoznZfhPkABjd3fmCJ'}              | ERROR    Error in Team run: Error code: 401 - {'type': 'error', 'error':         |          {'type': 'authentication_error', 'message': 'invalid x-api-key'},       |          'request_id': 'req_011CXvqoznZfhPkABjd3fmCJ'}                           | DEBUG Added RunOutput to Team Session

---

### team_streaming.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/streaming/team_streaming.py`。

**结果：** 执行成功。耗时：41.62s。尾部：tely $185.41. Please note  │ | │ that stock prices can fluctuate frequently throughout the trading day, so    │ | │ you may want to check again for the most up-to-date information if you're    │ | │ making time-sensitive decisions.                                             │ | ╰──────────────────────────────────────────────────────────────────────────────╯

---
