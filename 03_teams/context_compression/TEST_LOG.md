# 测试日志：context_compression

> 更新时间：2026-02-08 15:49:52

## 模式检查

**状态：** PASS

**结果：** 在 /Users/ab/conductor/workspaces/agno/colombo/cookbook/03_teams/context_compression 中检查了 2 个文件。违规：0

---

### tool_call_compression.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/context_compression/tool_call_compression.py`。

**结果：** 退出代码 1。尾部：y", line 1, in <module> |     from agno.models.aws.bedrock import AwsBedrock |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/models/aws/bedrock.py", line 22, in <module> |     raise ImportError("`boto3` not installed. Please install using `pip install boto3`") | ImportError: `boto3` not installed. Please install using `pip install boto3`

---

### tool_call_compression_with_manager.py

**状态：** FAIL

**描述：** 执行 `.venvs/demo/bin/python cookbook/03_teams/context_compression/tool_call_compression_with_manager.py`。

**结果：** 退出代码 1。尾部：y", line 1, in <module> |     from agno.models.aws.bedrock import AwsBedrock |   File "/Users/ab/conductor/workspaces/agno/colombo/libs/agno/agno/models/aws/bedrock.py", line 22, in <module> |     raise ImportError("`boto3` not installed. Please install using `pip install boto3`") | ImportError: `boto3` not installed. Please install using `pip install boto3`

---
