---
name: translate-to-chinese
description: Translate Python project files (comments, docstrings, instructions, markdown) from English to Chinese. Use when the user asks to translate code comments, README, documentation, or AI prompt instructions to Chinese in a Python project.
---

# 项目文件中英翻译

将 Python 项目中的英文内容翻译为中文，覆盖注释、文档字符串、instructions prompt、markdown 文件等。

## 翻译范围

### Python 文件（.py）

需要翻译的内容：
- 模块顶部的 docstring（`"""..."""`）
- 行内注释（`# ...`）
- 函数/类的 docstring
- `instructions = """..."""` 变量中的 AI prompt 内容
- `additional_instructions` / `compression_prompt` / `message` 等 prompt 类变量
- 打印输出文本（`print()` 中的字符串）
- 用户查询示例（示例对话内容）
- 文件底部 `"""..."""` 中的说明文字

不翻译的内容：
- 代码逻辑、变量名、函数名、类名
- import 语句
- 字符串常量（非注释/文档用途的，如 API key、URL）
- Pydantic Field 的 `description` 参数（保留英文，因为是给模型的 schema）
- `role` 参数值（保留英文）
- 文件路径和命令（如 `python xxx.py`）
- 代码块中的代码（仅翻译注释）

### Markdown 文件（.md）

全文翻译，包括：
- 标题、段落、列表
- 表格内容
- 代码块中的注释（代码本身不翻译）

### 其他文件

- `.yaml` / `.toml` 中的 `description` 字段
- shell 脚本中的注释

## 工作流程

### 极小型目录（< 15 个文件）
**直接处理，效率最高**
1. 并行 `Glob` 查找 `.py` 和 `.md` 文件
2. Python 文件：`Read` + 多次 `StrReplace`，逐段翻译
3. Markdown 文件：`Read` + `Write` 整体写入
4. 预计耗时：10-20 分钟

**翻译优先级**：
- 优先：用户可见文本（示例提示、print 输出、错误信息）
- 其次：模块 docstring、函数 docstring
- 最后：instructions 等 AI prompt（如果时间允许）

### 小型目录（15-20 个文件）
1. 并行 `Glob` 查找 `.py` 和 `.md` 文件
2. 逐文件 `Read` + `StrReplace` 翻译
3. Markdown 用 `Write` 整体写入（效率更高）

### 中型目录（20-50 个文件）
1. 先并行 `Glob` `.py` 和 `.md`
2. **分离处理**：
   - Python 文件：启动 1 个 Task
   - Markdown 文件：启动 1 个 Task（单独处理，效率高）
3. 两个 Task 并行运行

### 大型目录（> 50 个文件）
1. **分析文件分布**：先 `Glob` 统计各子目录文件数
2. **按文件类型拆分**：
   - Python 文件：启动 1 个 Task，内部按功能模块批量处理
   - Markdown 文件：启动 1 个 Task，全部一起处理（md 文件通常少）
3. **Python Task 策略**：
   - 优先翻译高频使用目录（01_quickstart、session、tools、knowledge）
   - 次要目录可批量快速处理（仅翻译 docstring + instructions）
   - 使用 `resume` 参数持续推进，直到全部完成

### Task 提示词模板

**Python 文件 Task（关键要点）：**
```
翻译 <目录路径> 目录下所有 Python 文件的英文内容为中文。

需要翻译：
- 模块顶部 docstring
- 行内注释 # ...
- 函数/类 docstring  
- instructions/additional_instructions 等 prompt 变量内容

不翻译：
- 代码逻辑、变量名、import
- Pydantic Field description
- role 参数值

技术术语统一：Agent、Team（团队）、Workflow（工作流）、Knowledge（知识库）、Storage（存储）、Memory（记忆）、Tool（工具）

使用 StrReplace 逐段替换。

【重要】继续翻译直到所有文件完成，不要中途停止总结。即使文件很多也要全部处理完。
```

**关键实践**：Python Task 通常需要 2-5 轮 resume 才能完成所有文件。第一轮完成度视文件结构而定：
- 简单结构（文件相似度高、子目录独立）：第一轮可达 60-70%
- 复杂结构（深层嵌套、文件差异大）：第一轮约 25-35%

**Markdown 文件 Task：**
```
翻译 <目录路径> 目录下所有 Markdown 文件的英文内容为中文。

全文翻译：标题、段落、列表、表格。代码块中的注释也翻译，代码本身不翻译。

技术术语保留英文或附中文说明：Agent、Team（团队）、Workflow（工作流）等。

使用 Write 直接写入翻译后内容。完成后报告翻译的文件数。
```

**关键实践**：Markdown Task 通常能一次性完成所有文件（50+ 个也可以），因为 Write 效率高且 md 文件相对简单。

## 翻译原则

- 技术术语保留英文或附中文括号说明，如 Agent、Workflow、Knowledge Base（知识库）
- 翻译要自然通顺，不生硬直译
- 保留原有代码结构、缩进、格式不变
- **用户可见文本优先翻译**：示例提示、print 输出、错误消息
- 常用术语统一：
  - Agent → Agent
  - Team → 团队
  - Workflow → 工作流
  - Knowledge → 知识库
  - Storage → 存储
  - Memory → 记忆
  - Guardrail → 护栏
  - Tool → 工具
  - Instructions → 指令
  - Embedder → 嵌入器
  - Vector DB → 向量数据库
  - Hybrid search → 混合搜索
  - Structured output → 结构化输出
  - Human in the loop → 人机协作
  - Session → Session
  - State → State
  - RAG → RAG
  - Multimodal → 多模态
  - Parser → Parser
  - Hook → Hook
  - Event → 事件
  - Run → Run
  - Step → 步骤

## 性能优化与实战经验

### 文件类型分离策略（关键优化）
- **Python 和 Markdown 分别处理**：两种文件翻译方式不同，分离后效率更高
  - Python：细致翻译，逐段 StrReplace
  - Markdown：整体翻译，Write 直接写入
- **并行启动 2 个 Task**：Python Task + Markdown Task 同时运行

### Task 数量与分组
- **极小型任务**（< 15 文件）：不启动 Task，直接处理（10-20 分钟搞定）
- **小型任务**（15-20 文件）：不启动 Task，直接处理
- **中型任务**（20-50 文件）：2 个 Task（py + md 分离）
- **大型任务**（> 50 文件）：2 个 Task + resume 持续推进
  - **避免启动 4 个并行 Task**：实际效率不如 2 个 Task + 多次 resume
  - **原因**：大量文件导致每个 Task 都很重，4 个并行容易超时或不完整

### Resume 策略（大型任务核心）

**关键经验：Python Task 会自动停止总结，需要主动推进**

1. **首次启动**：2 个 Task（py + md）并行
2. **检查进度**：Task 返回后立即查看进度
   - **Markdown Task**：通常一次完成 100%（50+ 文件也可以）✅
   - **Python Task**：第一轮通常只完成 25-35%，需要 resume ⚠️
3. **立即 Resume Python Task**：不要等待，直接用 `resume` 参数继续推进
4. **明确指令**：Resume 时明确告诉 Task"继续翻译所有剩余文件"
5. **重复 2-4 步**：Python Task 通常需要 2-3 轮 resume 才能完成

**Resume 提示词模板：**
```
继续翻译 <目录> 所有剩余的 Python 文件。

已完成：<X>/<总数> 文件（<百分比>%）
剩余：约 <Y> 个文件

剩余目录：
- <子目录1>（<文件数>个）
- <子目录2>（<文件数>个）

【关键】继续翻译所有剩余的<Y>个文件，不要中途停止。全部完成后再报告。

使用 StrReplace 逐段翻译。保持高效批量处理。
```

**实战示例（04_workflows 翻译）：**
```python
# 第 1 轮：并行启动 2 个 Task
task_py = Task(prompt="翻译所有 Python 文件...", subagent_type="generalPurpose")
task_md = Task(prompt="翻译所有 Markdown 文件...", subagent_type="generalPurpose")

# Markdown Task 返回：52/52 文件完成（100%）✅
# Python Task 返回：22/79 文件完成（28%）⚠️

# 第 2 轮：仅 Resume Python Task
task_py_2 = Task(
    prompt="继续翻译剩余的所有 Python 文件（已完成 22/79，剩余 57 个）...", 
    resume=task_py.agent_id,
    subagent_type="generalPurpose"
)
# 返回：28/79 文件完成（35%）⚠️

# 第 3 轮：再次 Resume
task_py_3 = Task(
    prompt="继续翻译所有剩余 Python 文件（已完成 28/79，剩余 51 个）...", 
    resume=task_py.agent_id,
    subagent_type="generalPurpose"
)
# 返回：79/79 文件全部完成（100%）✅
```

**关键发现**：
- ✅ Markdown Task 一次完成，无需 resume
- ⚠️ Python Task 需要 2-3 轮，第一轮约 25-35%
- 📊 总耗时：3 轮 Task 调用（2 次 resume）

### 翻译优先级（大型目录）
在 Python Task 中按优先级翻译：
1. **高频使用**（必须完整）：01_quickstart、session、tools、knowledge
2. **核心功能**（详细翻译）：context、hooks、guardrails、memory
3. **扩展功能**（快速翻译）：仅 docstring + instructions

### 实战经验总结

**核心发现：Python Task 第一轮完成度 25-70%，视文件结构而定**

1. ✅ **极小型目录（< 15 文件）直接处理**：启动 Task 反而慢，逐文件翻译 10-20 分钟搞定
2. ✅ **预期 Python Task 需要多轮**：第一轮完成度差异大，需根据结构调整预期
   - **简单结构**（如 07_knowledge）：第一轮 60-70%，2-3 轮完成
   - **复杂结构**（如 05_agent_os）：第一轮 25-35%，4-5 轮完成
3. ✅ **Markdown Task 无需 resume**：50+ md 文件通常一次完成（Write 效率高）
4. ✅ **立即 Resume Python Task**：第一轮返回后立即查看进度，马上 resume 继续
5. ✅ **Resume 提示词要具体**：明确说明"已完成 X/总数，剩余 Y 个"，并列出剩余目录
6. ✅ **先 Glob 两次**：并行查找 py 和 md，避免串行等待
7. ✅ **Markdown 用 Write**：比 StrReplace 快 3-5 倍
8. ✅ **Python 用 StrReplace**：保持格式和结构完整
9. ✅ **2 Task + Resume**：比 4 Task 并行更可控、更可靠
10. ✅ **分离 Python 和 Markdown**：两种文件处理方式不同，分离效率更高
11. ✅ **评估文件结构**：第一轮前先分析子目录独立性和文件相似度，预测完成轮数
12. ✅ **翻译优先级**：用户可见文本（示例提示、print）> docstring > instructions
13. ✅ **增量翻译天然支持**：Task 会自动检测已翻译文件并跳过，无需人工筛选。已翻译目录可直接重跑，安全幂等
14. ✅ **部分翻译目录（如多次迭代后）**：直接启动 Task，Task 会自动识别哪些文件已完成，只处理剩余文件
15. ❌ **避免 4 个并行 Task**：大量文件时每个 Task 都太重，容易中断
16. ❌ **避免过细拆分**：10 个小 Task 不如 2 个大 Task + resume
17. ❌ **避免固定预期**：不同目录结构差异大，灵活调整 resume 策略

**为什么 Python Task 第一轮完成度差异大？**

**影响完成度的关键因素：**
1. **文件相似度**：
   - 高相似度（如 07_knowledge 的多个 embedder 文件）→ 70% 完成度
   - 低相似度（如 05_agent_os 的混合功能文件）→ 30% 完成度
2. **子目录独立性**：
   - 独立子目录（如 readers/, embedders/ 互不依赖）→ 翻译流畅
   - 强耦合子目录（如 core/, utils/ 相互引用）→ 翻译慢
3. **代码复杂度**：
   - 示例代码居多（如 07_knowledge）→ StrReplace 快速
   - 核心逻辑复杂（如 05_agent_os）→ StrReplace 慢

**技术原因：**
- Python 文件翻译复杂度高（需要 StrReplace 逐段替换）
- Token 消耗积累（每个 Python 文件消耗 1000-3000 tokens）
- 上下文过长（已处理文件的历史记录）
- Task 内置的"合理停止点"判断

**为什么 Markdown Task 不需要 resume？**
- Markdown 文件翻译简单（Write 整体写入）
- 处理速度快（每个文件 500-1500 tokens）
- 文件数量虽多但总 token 消耗低

**如何应对？**
- 接受 Python Task 需要 2-5 轮 resume（视文件结构而定）
- **第一轮前快速评估**：用 `ls -R` 查看子目录结构，预判相似度
  - 看到多个同类子目录（如 embedders/, vector_db/）→ 预期 60-70%
  - 看到混合功能文件（如 core/, utils/, hooks/）→ 预期 30-35%
- 每轮 resume 时明确剩余文件数和剩余目录，给出清晰指令
- 使用同一个 agent_id 持续 resume，保持上下文

### Token 管理与预期

- **极小型任务**（< 15 文件）：3-8k tokens，单次完成，10-20 分钟
- **小型任务**（15-20 文件）：8-15k tokens，单次完成
- **中型任务**（20-50 文件）：15-30k tokens，1-2 轮
- **大型任务**（50-100 文件）：40-80k tokens，2-3 轮 resume
- **超大型任务**（100-200 文件）：80-150k tokens，4-5 轮 resume

**关键指标**：
- 每个 Python 文件平均消耗：500-1500 tokens（取决于复杂度）
- 每个 Markdown 文件平均消耗：1000-3000 tokens
- Task 通常在累计消耗 30-40k tokens 后自动停止

**实战案例对比：**

| 目录 | Python 文件数 | Markdown 文件数 | Python 轮数 | Markdown 轮数 | 总耗时 |
|------|--------------|----------------|------------|--------------|--------|
| 00_quickstart | 13 | 3 | 直接处理 | 直接处理 | 20 分钟 |
| 03_teams | 118 | 48 | 2 轮（38% 停止）| 1 轮 | 3 次 Task |
| 04_workflows | 79 | 52 | 3 轮（28%→35%→100%）| 1 轮 | 4 次 Task |
| 05_agent_os | 168 | 66 | 5 轮（32%→67%→71%→82%→88%）| 1 轮 | 6 次 Task |
| 07_knowledge | 137 | 63 | 3 轮（70%→85%→100%）✨| 1 轮 | 4 次 Task |
| 09_evals | 38 | 19 | 1 轮（29/38已译，仅补9个新文件）✨| 1 轮（已译直接跳过）| 2 次 Task |

**经验教训**：
- **极小型目录（< 15 文件）直接处理最快**：启动 Task 反而慢，直接逐文件翻译 10-20 分钟搞定
- Python Task 第一轮完成度：25-70%（视文件复杂度和结构）
  - 简单结构目录（如 07_knowledge）：第一轮可达 70%
  - 复杂嵌套目录（如 05_agent_os）：第一轮约 30-35%
- Markdown Task 第一轮完成度：100%（无需 resume）
- Python 文件数 < 15：直接处理（无需 Task）
- Python 文件数 15-50：通常 2 轮
- Python 文件数 50-100：通常 2-3 轮
- Python 文件数 100-200：通常 3-5 轮（取决于文件结构）
- 超长文件（800+ 行）可能因格式复杂无法完全翻译，需单独处理

**关键发现（07_knowledge 案例）**：
- ✅ **第一轮达 70%**：文件结构清晰、子目录独立时，完成度显著提高
- ✅ **3 轮完成 137 文件**：比预期更高效（原预期 4-5 轮）
- 💡 **影响因素**：
  - 文件相似度高（如多个 vector_db 子目录结构相似）→ 完成度高
  - 子目录独立性强（如 embedders/, readers/ 互不依赖）→ 翻译效率高
  - 代码复杂度低（如示例代码居多）→ StrReplace 速度快

## 常见问题

**Q: Python Task 第一轮只完成了 28% 还是 70%，哪个是正常的？**
A: **都是正常的**，取决于文件结构：
- **70% 完成**：文件相似度高、子目录独立（如 07_knowledge 的 embedders/, readers/）
- **28-35% 完成**：文件复杂、深层嵌套（如 05_agent_os 的 core/, hooks/）
- 第一轮前快速用 `ls -R` 评估目录结构，预判完成度

**Q: Markdown Task 为什么能一次完成 50+ 文件？**
A: 因为使用 Write 工具整体写入，效率极高。且 md 文件相对简单，token 消耗低。

**Q: 需要手动检查每个文件的翻译质量吗？**
A: 不需要。翻译规则清晰，Task 会保持一致性。最后抽查几个文件即可。

**Q: 多次 resume 会不会重复翻译？**
A: 不会。Task 保持上下文，知道哪些已完成，哪些未完成。

**Q: 什么时候应该放弃 resume，重新启动新 Task？**
A: 如果连续 3 轮 resume 进度都很慢（< 10%），可以考虑重新启动。但通常 2-3 轮就能完成。

**Q: 超大型任务（150+ Python 文件）需要多少轮 resume？**
A: **2-5 轮**，取决于文件结构：
- **简单结构**（如 07_knowledge 137 文件）：3 轮完成（70%→85%→100%）
- **复杂结构**（如 05_agent_os 168 文件）：5 轮完成（32%→67%→71%→82%→88%）
- 核心功能文件优先完成，超长文件（800+ 行）可能需要单独处理

**Q: 为什么有些超长文件无法完全翻译？**
A: 超长文件（800+ 行）因格式复杂、嵌套深度大，StrReplace 可能遇到格式匹配问题。建议最后单独处理这些文件，或手动分段翻译。

**Q: 某个目录之前已部分翻译，现在新增了文件，怎么处理？**
A: 直接按正常流程启动 Task 即可。Task 会自动检测哪些文件已翻译（内容为中文）并跳过，只处理新增或未翻译的文件。翻译操作是**幂等的**，重复运行不会破坏已翻译内容。典型案例：09_evals 有 29/38 个 Python 文件已提前翻译，Task 1 轮内仅翻译了剩余 9 个文件，效率极高。

**Q: 如何判断一个目录是否"已经翻译过"，需不需要跳过？**
A: 不需要手动判断，直接运行即可。Task 内部会逐文件检查内容语言，已翻译的直接跳过。
