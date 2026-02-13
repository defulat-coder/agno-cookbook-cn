# 测试日志：guardrails

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/guardrails 中检查了 3 个文件。违规：0

---

### openai_moderation.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/guardrails/openai_moderation.py`。

**结果：** 执行成功。耗时：17.34s。尾部：━━━━━━━━━━━━━━━━━━━━━━━━━━┓ | ┃                                                                              ┃ | ┃ OpenAI moderation violation detected.                                        ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### pii_detection.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/guardrails/pii_detection.py`。

**结果：** 执行成功。耗时：14.63s。尾部：t or form, I recommend you ┃ | ┃ **remove/redact it if possible** and use the company's official secure       ┃ | ┃ verification process (phone or in-app verification) instead.                 ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### prompt_injection.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/guardrails/prompt_injection.py`。

**结果：** 执行成功。耗时：1.64s。尾部：                                                                      ┃ | ┃ Potential jailbreaking or prompt injection detected.                         ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛[WARNING] This should have been blocked!

---
