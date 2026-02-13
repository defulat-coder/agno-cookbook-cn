# 测试日志：multimodal

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/multimodal 中检查了 8 个文件。违规：0

---

### audio_sentiment_analysis.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/audio_sentiment_analysis.py`。

**结果：** 执行成功。耗时：44.01s。尾部：db/sqlite/sqlite.py", line 1039, in upsert_session |     raise e |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/db/sqlite/sqlite.py", line 998, in upsert_session |     return TeamSession.from_dict(session_raw) |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ | NameError: name 'requirements' is not defined. Did you mean: 'RunRequirement'?

---

### audio_to_text.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/audio_to_text.py`。

**结果：** 执行成功。耗时：16.55s。尾部：gether?                    ┃ | ┃                                                                              ┃ | ┃ Speaker B: Yes, we do. My mom always prepares delicious meals for us.        ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### generate_image_with_team.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/generate_image_with_team.py`。

**结果：** 执行成功。耗时：26.94s。尾部： None, | │   │   'additional_metrics': None | │   }, | │   'session_state': { | │   │   'current_session_id': '0591d68c-2d11-4802-b413-b55ab7cf0eb8', | │   │   'current_run_id': '64a46b30-ed80-4d3e-a9ff-5e93d404f4b1' | │   } | } | ------------------------------------------------------------ | DEBUG **** Team Run End: 64a46b30-ed80-4d3e-a9ff-5e93d404f4b1 ****

---

### image_to_image_transformation.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/image_to_image_transformation.py`。

**结果：** 退出代码 1。尾部：", line 11, in <module> |     from agno.tools.fal import FalTools |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/tools/fal.py", line 19, in <module> |     raise ImportError("`fal_client` not installed. Please install using `pip install fal-client`") | ImportError: `fal_client` not installed. Please install using `pip install fal-client`

---

### image_to_structured_output.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/image_to_structured_output.py`。

**结果：** 执行成功。耗时：36.66s。尾部：2.8962 tokens/s                            | DEBUG ************************  METRICS  *************************               | DEBUG ---------------- OpenAI Response Stream End ----------------               | DEBUG Added RunOutput to Team Session                                            | DEBUG **** Team Run End: 7b4daca9-8437-4d9d-ac96-1c99978deb51 ****

---

### image_to_text.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/image_to_text.py`。

**结果：** 执行成功。耗时：4.36s。尾部：ge for analysis. Could you ┃ | ┃ please provide a brief description of the image, so my team can assist you   ┃ | ┃ more effectively?                                                            ┃ | ┃                                                                              ┃ | ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

---

### media_input_for_tool.py

**状态：** PASS

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/media_input_for_tool.py`。

**结果：** 执行成功。耗时：14.6s。尾部：0 - $125,000) / $125,000). |     *   However, the growth from Q2 to Q3 is approximately 16.7% (($175,000 - $150,000) / $150,000), not 20%. |  | In summary, the company shows strong revenue growth, though the stated 20% quarter-over-quarter growth rate is not consistently maintained in the provided data. |  | ==================================================

---

### video_caption_generation.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/multimodal/video_caption_generation.py`。

**结果：** 退出代码 1。尾部：from agno.tools.moviepy_video import MoviePyVideoTools |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/tools/moviepy_video.py", line 9, in <module> |     raise ImportError("`moviepy` not installed. Please install using `pip install moviepy ffmpeg`") | ImportError: `moviepy` not installed. Please install using `pip install moviepy ffmpeg`

---
