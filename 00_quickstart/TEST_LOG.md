# TEST_LOG.md - 快速入门 Cookbook

`cookbook/00_quickstart/` 示例的测试结果。

**测试日期：** 2026-02-10（重新验证）
**环境：** `.venvs/demo/bin/python`，已加载 `direnv` 导出
**模型：** `gemini-3-flash-preview`（Google Gemini）
**数据库：** SQLite（`tmp/agents.db`）和 ChromaDB（`tmp/chromadb/`）

---

## 结构验证

### check_cookbook_pattern.py

**状态：** 通过

**描述：** 验证快速入门示例的 cookbook 结构和格式规范。

**结果：** `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/00_quickstart` 报告 `Checked 13 file(s) ... Violations: 0`。

---

### style_guide_compliance_scan

**状态：** 通过

**描述：** 验证模块文档字符串（含 `=====` 下划线）、段落横幅、import 位置、`if __name__ == "__main__":` 入口和无 emoji 字符。

**结果：** 全部 13 个可运行文件符合 `cookbook/STYLE_GUIDE.md`。未发现 emoji 字符。

---

## 运行时验证

### agent_with_tools.py

**状态：** 通过

**描述：** 带 YFinanceTools 的金融 Agent 获取 NVIDIA 的实时市场数据。

**结果：** 退出码 `0`；生成了包含价格（$190.04）、市值（$4.63T）、市盈率、52周范围、关键驱动因素和风险的投资简报。

---

### agent_with_structured_output.py

**状态：** 通过

**描述：** 返回 NVIDIA 的类型化 `StockAnalysis` Pydantic 模型。

**结果：** 退出码 `0`；结构化输出正确解析，包含所有字段（ticker、company_name、current_price、market_cap、pe_ratio、52周范围、key_drivers、key_risks、recommendation）。

---

### agent_with_typed_input_output.py

**状态：** 通过

**描述：** 使用 `AnalysisRequest` 输入和 `StockAnalysis` 输出 schema 的完整类型安全。测试了字典和 Pydantic 模型两种输入方式。

**结果：** 退出码 `0`；字典输入（NVDA 深度分析）和 Pydantic 模型输入（AAPL 快速分析）均返回了正确类型的 `StockAnalysis` 响应。

---

### agent_with_storage.py

**状态：** 通过

**描述：** 带 SQLite 存储的金融 Agent 在三轮对话中保持持久化。

**结果：** 退出码 `0`；完成了三轮对话（NVDA 简报、TSLA 对比、投资建议）。Agent 正确引用了之前的轮次。

---

### agent_with_memory.py

**状态：** 通过

**描述：** 带 MemoryManager 的 Agent 提取并回忆用户偏好。

**结果：** 退出码 `0`；Agent 存储了两条记忆（"对 AI 和半导体股票感兴趣"、"中等风险承受能力"）并利用它们个性化股票推荐。

---

### agent_with_state_management.py

**状态：** 通过

**描述：** Agent 通过自定义状态修改工具管理股票自选列表。

**结果：** 退出码 `0`；将 NVDA、AAPL、GOOGL 添加到自选列表，获取了自选股票的价格，并确认会话状态为 `['NVDA', 'AAPL', 'GOOGL']`。

---

### agent_search_over_knowledge.py

**状态：** 通过

**描述：** 将 Agno 介绍文档加载到 ChromaDB 知识库中，使用混合搜索回答问题。

**结果：** 退出码 `0`；从 `https://docs.agno.com/introduction.md` 加载知识，搜索并综合了关于 Agno 功能和组件的回答。

---

### custom_tool_for_self_learning.py

**状态：** 通过

**描述：** 带自定义 `save_learning` 工具的 Agent 将洞察保存到 ChromaDB 知识库并可检索。

**结果：** 退出码 `0`；Agent 提议并保存了关于科技股市盈率基准的学习心得，然后从知识库中检索了它。

---

### agent_with_guardrails.py

**状态：** 通过

**描述：** 测试 PII 检测、提示注入防护和自定义垃圾信息护栏。

**结果：** 退出码 `0`；四个测试用例执行：正常请求通过、PII（社保号）被阻止、提示注入被阻止、垃圾信息（过多感叹号）被阻止。

---

### human_in_the_loop.py

**状态：** 通过

**描述：** 使用 `@tool(requires_confirmation=True)` 的确认工具执行。

**结果：** 退出码 `0`；Agent 提议保存学习心得，通过 stdin 输入 `y` 批准确认，工具执行并保存了学习心得。

---

### multi_agent_team.py

**状态：** 通过

**描述：** 多头/空头分析师团队，领导综合 NVIDIA 和 AMD 的对比分析。

**结果：** 退出码 `0`；两位分析师提供了独立观点，领导综合成平衡的建议并附对比表格。

---

### sequential_workflow.py

**状态：** 通过

**描述：** 三步工作流：数据采集、分析、报告撰写（针对 NVIDIA）。

**结果：** 退出码 `0`，耗时约 30.8 秒；三个步骤全部完成，最终报告包含建议（买入）、关键指标表格和理由。

---

### run.py

**状态：** 通过

**描述：** 长时间运行的 AgentOS 服务器的启动验证。

**结果：** 服务器在 `http://localhost:7777` 成功启动，注册了全部 10 个 Agent、1 个团队和 1 个工作流。Uvicorn 启动完成。15 秒后进程正常终止。

---

## 总结

| 文件 | 状态 | 备注 |
|------|------|------|
| `agent_with_tools.py` | 通过 | 使用真实市场数据生成了 NVDA 投资简报 |
| `agent_with_structured_output.py` | 通过 | 返回了包含所有字段的类型化 `StockAnalysis` |
| `agent_with_typed_input_output.py` | 通过 | 字典和 Pydantic 模型输入均正确处理 |
| `agent_with_storage.py` | 通过 | 三轮持久化对话完成 |
| `agent_with_memory.py` | 通过 | 记忆存储并用于个性化推荐 |
| `agent_with_state_management.py` | 通过 | 跨轮次管理自选列表状态 |
| `agent_search_over_knowledge.py` | 通过 | 知识加载、混合搜索、生成回答 |
| `custom_tool_for_self_learning.py` | 通过 | 自定义工具保存并检索学习心得 |
| `agent_with_guardrails.py` | 通过 | 全部 4 个护栏测试用例通过（正常、PII、注入、垃圾信息） |
| `human_in_the_loop.py` | 通过 | 通过 stdin 批准完成确认流程 |
| `multi_agent_team.py` | 通过 | 多头/空头团队协作完成 |
| `sequential_workflow.py` | 通过 | 三步工作流约 33.6 秒完成 |
| `run.py` | 通过 | AgentOS 服务器启动验证通过 |

**总计：** 13 通过，0 失败
