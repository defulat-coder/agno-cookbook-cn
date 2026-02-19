目标：对 `cookbook/10_reasoning` 进行全面测试与验证，使其符合 cookbook 规范标准。

上下文文件（请先阅读）：
- `AGENTS.md` — 项目规范、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载

执行要求：
1. **读取每一个 `.py` 文件**，在做任何修改之前，先读取目标 cookbook 目录中的所有文件。
   不要仅依赖 grep 或结构检查器——需逐一打开并阅读每个文件，了解其完整内容。这样可以发现自动检查器可能遗漏的问题（例如：section 内部的 import、注释中过时的模型引用、不一致的代码模式）。

2. 为 `cookbook/10_reasoning/` 下的每个顶级子目录（`agents/`、`models/`、`teams/`、`tools/`）启动一个并行 Agent。每个 Agent 独立处理一个子目录，包括其中的所有嵌套子目录。

3. 每个 Agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/10_reasoning/<SUBDIR> --recursive` 并修复所有违规项。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录（及嵌套子目录）中的所有 `*.py` 文件，并记录运行结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 模块文档字符串，使用 `=====` 下划线
      - Section 分隔符：`# ---------------------------------------------------------------------------`
      - import 语句位于文档字符串和第一个分隔符之间
      - 使用 `if __name__ == "__main__":` 守卫
      - 不含 emoji 字符
   d. 同时检查该目录中的非 Python 文件（`README.md` 等），更新其中过时的 `OpenAIChat` 引用。
   e. 仅做最小限度、保持行为不变的编辑以符合风格规范。
   f. 将新的 PASS/FAIL 条目更新到 `cookbook/10_reasoning/<SUBDIR>/TEST_LOG.md`。对于嵌套子目录，在每个目录中创建对应的 TEST_LOG.md。

4. 所有 Agent 完成后，汇总并合并结果。

特殊情况：
- 推理示例可能产生较长的思维链输出——请使用较宽裕的超时时间（120 秒）。
- `models/` 子目录中的示例可能需要特定模型提供商的 API 密钥——若不可用则跳过。
- `tools/` 示例将推理与工具使用结合——可能需要额外的 API 密钥（例如网络搜索）。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/10_reasoning/<SUBDIR> --recursive`（每个子目录分别运行）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现的问题（不一致、失败、风险）及文件引用。
2. 已运行的测试/验证命令及结果。
3. 任何遗留问题或需要人工跟进的事项。
4. 结果表格，格式如下：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `agents/chain_of_thought` | `cot_agent.py` | PASS | 推理链产生了正确结果 |
| `models/deepseek` | `deepseek_reasoning.py` | SKIP | DeepSeek API 密钥不可用 |
