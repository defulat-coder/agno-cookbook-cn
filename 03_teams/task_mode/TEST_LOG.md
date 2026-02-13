# Task Mode Cookbook - 测试日志

## 测试环境
- 虚拟环境：`.venvs/demo/bin/python`
- 日期：2026-02-10

---

### 01_basic_task_mode.py

**状态：** PASS

**描述：** 测试具有 3 个成员 agent（Researcher、Writer、Critic）的任务模式团队。团队领导将量子计算简报请求分解为离散任务，分配给成员，并综合结果。

**结果：** 团队成功创建 3 个研究任务并通过 `execute_tasks_parallel` 并行执行，然后创建具有适当依赖关系的顺序写作和审查任务。所有任务成功完成。使用摘要调用 `mark_all_complete`。响应时间：~60s。

---

### 02_parallel_tasks.py

**状态：** PASS

**描述：** 测试具有 3 个分析师 agent（Market、Tech、Financial）的并行任务执行。团队领导创建独立的分析任务并并发运行它们。

**结果：** 团队创建 3 个分析任务分配给正确的专家，并通过 `execute_tasks_parallel` 并行执行全部 3 个任务。完成后，使用综合摘要调用 `mark_all_complete`。响应时间：~35s。

---

### 03_task_mode_with_tools.py

**状态：** PASS

**描述：** 测试带工具的任务模式。Web Researcher 使用 DuckDuckGo 工具搜索网络，Summarizer 整理发现。

**结果：** 团队创建一个网络研究任务（由使用 DuckDuckGo 搜索的 Web Researcher 执行），然后创建一个依赖于研究的摘要任务。任务按正确的依赖顺序执行。最终摘要涵盖了 LLM 发展，包括多模态能力、SFT 改进、可扩展性和新指标。响应时间：~34s。

---

### 04_async_task_mode.py

**状态：** PASS

**描述：** 测试异步 API（`arun`）与任务模式。项目团队（Planner、Executor、Reviewer）通过计划-执行-审查流程创建入职检查清单。

**结果：** 团队成功使用异步执行路径（`OpenAI Async Response`）。创建具有适当依赖关系的计划、执行和审查任务。所有任务完成并调用 `mark_all_complete`。演示了异步任务模式端到端工作。

---

### 05_dependency_chain.py

**状态：** PASS

**描述：** 测试产品发布流程中具有 4 个 agent 的复杂依赖链（Market Researcher -> Product Strategist -> Content Creator -> Launch Coordinator）。

**结果：** 团队创建 4 个具有链式 `depends_on` 关系的任务。任务按依赖顺序顺序执行：首先市场研究，然后策略（依赖于研究），然后内容（依赖于策略），然后发布计划（依赖于所有三个）。响应时间：~83s。

---

### 06_custom_tools.py

**状态：** PASS

**描述：** 测试使用自定义 Python 函数工具（复利计算器、贷款支付计算器、风险评估器）的 agent 的任务模式。

**结果：** 团队创建 3 个任务（抵押贷款计算、投资计算、风险评估）并通过 `execute_tasks_parallel` 并行运行。成员 agent 正确调用其自定义工具 - Financial Calculator 计算每月 $2,275.44 抵押贷款和 $246,340.14 投资增长；Risk Assessor 评估中等风险（得分 70/100）。Financial Advisor 然后综合建议。响应时间：~37s。

---

### 07_multi_run_session.py

**状态：** PASS

**描述：** 测试多运行会话持久化。两个连续运行使用相同的 `session_id`，第二次运行引用第一次运行的发现。

**结果：** 两次运行都使用会话 ID `task-mode-demo-session`。运行 1 研究微服务与单体架构。运行 2 成功基于先前分析提供具体建议（5 人创业公司使用单体架构）。任务状态在同一会话内的运行之间持久保存。

---
