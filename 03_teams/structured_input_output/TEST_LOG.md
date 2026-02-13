# 测试日志：structured_input_output

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/structured_input_output 中检查了 10 个文件。违规：0

---

### input_formats.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/input_formats.py`。

**结果：** 执行成功。耗时：42.58s。尾部：t detection, medical scans ┃ | ┃ - **NLP:** translation, summarization, chatbots                              ┃ | ┃ - **Speech/audio:** speech recognition, voice activity detection             ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### input_schema.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/input_schema.py`。

**结果：** 执行成功。耗时：125.01s。尾部：ctor/workspaces/agno/colombo/cookbook/03_teams/structured_input_output/input_schema.py:22: PydanticDeprecatedSince20: `min_items` is deprecated and will be removed, use `min_length` instead. Deprecated in Pydantic V2.0 to be removed in V3.0. See Pydantic V2 Migration Guide at https://errors.pydantic.dev/2.12/migration/ |   research_topics: List[str] = Field(

---

### json_schema_output.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/json_schema_output.py`。

**结果：** 执行成功。耗时：14.1s。尾部：                           │ | │     "company_name": "NVIDIA Corporation",                                    │ | │     "analysis": "NVIDIA Corporation (NVDA) is currently trading at $192.73,… │ | │ }                                                                            │ | ╰──────────────────────────────────────────────────────────────────────────────╯

---

### output_model.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/output_model.py`。

**结果：** 执行成功。耗时：5.12s。尾部：━━━━━━━━━━━━━━━━━━━━━━━━━━┓ | ┃                                                                              ┃ | ┃ I'll now wait for the detailed itinerary from our Itinerary Planner.         ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### output_schema_override.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/output_schema_override.py`。

**结果：** 执行成功。耗时：124.14s。尾部： DEBUG ------------- OpenAI Async Response Stream End -------------               | DEBUG Added RunOutput to Team Session                                            | DEBUG **** Team Run End: 5295ff6f-207b-443f-986a-6104a9a97041 ****               | BookSchema(title='Pride and Prejudice', author='Jane Austen', year=1813) | Schema after override: PersonSchema

---

### parser_model.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/parser_model.py`。

**结果：** 执行成功。耗时：23.36s。尾部：ong Trail Ridge Road', | │   │   'Guided ranger programs offering deeper insights into local ecology' | │   ], | │   difficulty_rating=3, | │   estimated_days=7, | │   special_permits_needed=[ | │   │   'Wilderness permits for overnight backcountry hikes (if applicable)', | │   │   'Advance reservations for popular facilities during peak seasons' | │   ] | )

---

### pydantic_input.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/pydantic_input.py`。

**结果：** 执行成功。耗时：35.23s。尾部：ibuted systems             ┃ | ┃ implementations. Enjoy exploring these posts for deeper understanding and    ┃ | ┃ practical strategies!                                                        ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### pydantic_output.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/pydantic_output.py`。

**结果：** 执行成功。耗时：8.72s。尾部：                           │ | │   "company_name": "NVIDIA Corporation",                                      │ | │   "analysis": "NVIDIA's stock price has been experiencing fluctuations rece… │ | │ }                                                                            │ | ╰──────────────────────────────────────────────────────────────────────────────╯

---

### response_as_variable.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/response_as_variable.py`。

**结果：** 执行成功。耗时：59.31s。尾部：OL METRICS  **********************               | DEBUG ------------------- OpenAI Response End --------------------               | DEBUG Added RunOutput to Team Session                                            | DEBUG **** Team Run End: 2e280926-3731-4146-8323-087827d70df8 ****               | Processed MSFT: StockAnalysis | Total responses processed: 3

---

### structured_output_streaming.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/structured_input_output/structured_output_streaming.py`。

**结果：** 执行成功。耗时：30.72s。尾部：                           │ | │   "company_name": "Apple Inc.",                                              │ | │   "analysis": "Apple Inc. is a leading technology company known globally fo… │ | │ }                                                                            │ | ╰──────────────────────────────────────────────────────────────────────────────╯

---
