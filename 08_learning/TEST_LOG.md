# Learning Cookbook 测试日志

最后更新：2026-01-27

## 测试环境
- 数据库：PostgreSQL with PgVector at localhost:5532
- Python：`.venvs/demo/bin/python`
- 模型：gpt-5.2 (OpenAI)

---

## 优先级 1：最近更改直接影响的部分

### 05_learned_knowledge/01_agentic_mode.py

**状态：** PASS

**描述：** 使用重组提示（规则 1-4 整合在 CRITICAL RULES 部分）测试 LearnedKnowledgeStore 的 AGENTIC 模式。

**结果：** Agent 正确地：
- 在回答实质性问题之前进行搜索（规则 1）
- 当用户说"我们正在努力减少云出口成本"时保存团队目标（规则 4）
- 在后续会话中检索并应用学习内容

---

### 05_learned_knowledge/02_propose_mode.py

**状态：** PASS

**描述：** 测试 PROPOSE 模式，其中 agent 在保存之前提议学习供用户批准。

**结果：** Agent 正确地：
- 以标题/上下文/洞察格式提议学习（无表情符号 - 已验证修复）
- 当用户说"不，不要保存那个"时未保存
- 搜索现有学习内容

---

### 06_quick_tests/02_learning_true_shorthand.py

**状态：** PASS

**描述：** 测试 `learning=True` 简写，现在默认启用 UserProfile 和 UserMemory 存储。

**结果：**
- 创建的 LearningMachine 包含两个存储：`['user_profile', 'user_memory']`
- UserProfileStore 提取：Name "Charlie Brown"，Preferred Name "Chuck"
- UserMemoryStore 提取："用户名是 Charlie Brown；朋友叫他 Chuck"
- 会话 2 正确回忆 "Chuck"

---

## 优先级 2：烟雾测试

### 00_quickstart/01_always_learn.py

**状态：** PASS

**描述：** 基本 ALWAYS 模式学习，带自动提取。

**结果：** Agent 学习了用户信息（Alice，Anthropic 研究科学家，喜欢简洁的响应）并在会话 2 中回忆它。

---

### 00_quickstart/02_agentic_learn.py

**状态：** PASS

**描述：** 基本 AGENTIC 模式，其中 agent 有工具来更新记忆。

**结果：** Agent 使用 `update_user_memory` 工具并正确回忆用户信息。

---

### 00_quickstart/03_learned_knowledge.py

**状态：** PASS

**描述：** 测试跨用户共享的学习知识。

**结果：**
- 用户 1 保存了"减少云出口成本"目标
- 用户 2 收到的建议纳入了出口成本考虑（"鉴于你们组织减少出口成本的目标，这应该是一个首要的鉴别器"）

---

## 优先级 3：用户档案/记忆

### 01_basics/1a_user_profile_always.py

**状态：** PASS

**描述：** 使用 ALWAYS 模式提取的 UserProfileStore。

**结果：** 提取的档案（Alice Chen / Ali）并在会话 2 中正确回忆。

---

### 01_basics/2a_user_memory_always.py

**状态：** PASS

**描述：** 使用 ALWAYS 模式提取的 UserMemoryStore。

**结果：** 提取了关于用户工作和偏好的记忆，在会话 2 响应中应用它们。

---

## 优先级 4：其他存储

### 01_basics/3a_session_context_summary.py

**状态：** PASS

**描述：** SessionContextStore 跟踪对话状态。

**结果：** 在各轮次中维护会话摘要，当问"我们决定了什么？"时正确总结 API 设计讨论。

---

### 01_basics/4_learned_knowledge.py

**状态：** PASS

**描述：** 基本 LearnedKnowledgeStore 功能。

**结果：** Agent 搜索学习内容，将出口成本目标纳入云提供商推荐。

---

## 总结

| 类别 | 测试 | 通过 | 失败 |
|----------|-------|--------|--------|
| 优先级 1（最近更改） | 3 | 3 | 0 |
| 优先级 2（烟雾测试） | 3 | 3 | 0 |
| 优先级 3（用户档案/记忆） | 2 | 2 | 0 |
| 优先级 4（其他存储） | 2 | 2 | 0 |
| **总计** | **10** | **10** | **0** |

经过以下更改后所有测试通过：
1. `learning=True` 现在默认启用 `user_profile` 和 `user_memory`
2. LearnedKnowledgeStore 提示重组，规则 1-4 在 CRITICAL RULES 部分
3. 添加了规则 3（明确保存请求）和规则 4（组织目标/约束/政策）
4. 从 PROPOSE 模式中删除表情符号
5. 修复了 `learning_saved` 状态重置错误
6. 简化了工具文档字符串（删除了冗余的"何时保存"标准）
7. 更新了提取提示，采用更清晰的两类结构
