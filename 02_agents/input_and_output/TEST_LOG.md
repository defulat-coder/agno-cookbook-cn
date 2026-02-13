# 测试日志

生成时间: 2026-02-10 UTC

模式检查: 在 cookbook/02_agents/input_and_output 中检查了 5 个文件。违规数: 0

### input_formats.py

**状态:** 通过

**描述:** 使用 `.venvs/demo/bin/python` 作为可运行示例执行。

**结果:** 成功完成。

---

### input_schema.py

**状态:** 失败

**描述:** 使用 `.venvs/demo/bin/python` 作为可运行示例执行。

**结果:** 因 Anthropic API 认证错误失败（401 未授权）。环境问题 -- ANTHROPIC_API_KEY 无效。

---

### output_schema.py

**状态:** 通过

**描述:** 使用 `.venvs/demo/bin/python` 作为可运行示例执行。

**结果:** 成功完成。

---

### parser_model.py

**状态:** 通过

**描述:** 使用 `.venvs/demo/bin/python` 作为可运行示例执行。

**结果:** 成功完成。

---

### response_as_variable.py

**状态:** 通过

**描述:** 使用 `.venvs/demo/bin/python` 作为可运行示例执行。

**结果:** 成功完成。

---
