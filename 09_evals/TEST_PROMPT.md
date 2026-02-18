目标：对 `cookbook/09_evals` 进行全面测试和验证，使其符合我们的 cookbook 规范标准。

上下文文件（请先阅读）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

运行环境：
- Python：`.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载

执行要求：
1. **读取每一个 `.py` 文件**，在修改之前读取目标 cookbook 目录中的所有文件。
   不要仅依赖 grep 或结构检查脚本——逐一打开并阅读每个文件以理解其完整内容。这可确保你捕捉到自动化检查器可能遗漏的问题（例如，section 内部的导入、注释中过期的模型引用、不一致的代码模式）。

2. 为 `cookbook/09_evals/` 下的每个顶层子目录（`accuracy/`、`agent_as_judge/`、`performance/`、`reliability/`）各派生一个并行 Agent（代理）。每个 Agent 独立处理一个子目录，包括其中的嵌套子目录。

3. 每个 Agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/09_evals/<SUBDIR> --recursive` 并修复所有违规项。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录（及嵌套子目录）中所有 `*.py` 文件并记录运行结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md` 规范：
      - 带 `=====` 下划线的模块文档字符串
      - Section 分隔线：`# ---------------------------------------------------------------------------`
      - 导入语句位于文档字符串与第一条分隔线之间
      - 使用 `if __name__ == "__main__":` 入口守卫
      - 无 emoji 字符
   d. 同时检查目录中的非 Python 文件（`README.md` 等），找出过期的 `OpenAIChat` 引用并更新。
   e. 仅进行最小化、保持行为不变的编辑以满足风格合规要求。
   f. 用新的 PASS/FAIL 条目更新 `cookbook/09_evals/<SUBDIR>/TEST_LOG.md`。对于嵌套子目录，在每个子目录中创建对应的 TEST_LOG.md。

4. 所有 Agent 完成后，汇总并合并结果。

特殊情况：
- Eval（评估）脚本可能需要较长时间运行，因为它们会执行多次 LLM 调用进行评分——请使用较宽松的超时时间（120 秒）。
- `performance/`（性能）评估可能测量延迟或吞吐量——结果因运行环境而异。
- `agent_as_judge/` 示例使用一个 Agent 评估另一个 Agent——预期会有两轮 LLM 调用。

验证命令（完成前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/09_evals/<SUBDIR> --recursive`（对每个子目录执行）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现的问题（不一致、失败、风险）及对应文件引用。
2. 已运行的测试/验证命令及结果。
3. 剩余缺口或需要手动跟进的事项。
4. 结果汇总表，格式如下：

| 子目录 | 文件 | 状态 | 备注 |
|-------------|------|--------|-------|
| `accuracy/factual` | `factual_accuracy.py` | PASS | 准确性 Eval（评估）已完成，包含评分 |
| `performance/latency` | `latency_benchmark.py` | PASS | 延迟在预期范围内 |
