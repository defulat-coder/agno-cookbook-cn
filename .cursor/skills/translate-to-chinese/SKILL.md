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

### 小型目录（< 20 个文件）
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

**关键实践**：Python Task 通常需要 2-3 轮 resume 才能完成所有文件。第一轮可能只完成 25-35%，这是正常的。

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

## 性能优化与实战经验

### 文件类型分离策略（关键优化）
- **Python 和 Markdown 分别处理**：两种文件翻译方式不同，分离后效率更高
  - Python：细致翻译，逐段 StrReplace
  - Markdown：整体翻译，Write 直接写入
- **并行启动 2 个 Task**：Python Task + Markdown Task 同时运行

### Task 数量与分组
- **小型任务**（< 20 文件）：不启动 Task，直接处理
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

**核心发现：Python Task 会在 25-35% 进度时停止，Markdown Task 通常一次完成**

1. ✅ **预期 Python Task 会停止**：不要期待一次完成，50+ Python 文件需要 2-3 轮 resume
2. ✅ **Markdown Task 无需 resume**：50+ md 文件通常一次完成（Write 效率高）
3. ✅ **立即 Resume Python Task**：第一轮返回后立即查看进度，马上 resume 继续
4. ✅ **Resume 提示词要具体**：明确说明"已完成 X/总数，剩余 Y 个"，并列出剩余目录
5. ✅ **先 Glob 两次**：并行查找 py 和 md，避免串行等待
6. ✅ **Markdown 用 Write**：比 StrReplace 快 3-5 倍
7. ✅ **Python 用 StrReplace**：保持格式和结构完整
8. ✅ **2 Task + Resume**：比 4 Task 并行更可控、更可靠
9. ✅ **分离 Python 和 Markdown**：两种文件处理方式不同，分离效率更高
10. ❌ **避免 4 个并行 Task**：大量文件时每个 Task 都太重，容易中断
11. ❌ **避免过细拆分**：10 个小 Task 不如 2 个大 Task + resume
12. ❌ **避免期待 Python Task 一次完成**：50+ 文件必然需要 2-3 轮，这是正常的

**为什么 Python Task 会停止？**
- Python 文件翻译复杂度高（需要 StrReplace 逐段替换）
- Token 消耗积累（每个 Python 文件消耗 1000-3000 tokens）
- 上下文过长（已处理文件的历史记录）
- Task 内置的"合理停止点"判断

**为什么 Markdown Task 不需要 resume？**
- Markdown 文件翻译简单（Write 整体写入）
- 处理速度快（每个文件 500-1500 tokens）
- 文件数量虽多但总 token 消耗低

**如何应对？**
- 接受 Python Task 需要 2-3 轮 resume，这是正常的
- 每轮 resume 时明确剩余文件数和剩余目录，给出清晰指令
- 使用同一个 agent_id 持续 resume，保持上下文

### Token 管理与预期

- **小型任务**（< 20 文件）：5-10k tokens，单次完成
- **中型任务**（20-50 文件）：15-30k tokens，1-2 轮
- **大型任务**（50-100 文件）：40-80k tokens，2-3 轮 resume
- **超大型任务**（> 100 文件）：80-120k tokens，3-5 轮 resume

**关键指标**：
- 每个 Python 文件平均消耗：500-1500 tokens（取决于复杂度）
- 每个 Markdown 文件平均消耗：1000-3000 tokens
- Task 通常在累计消耗 30-40k tokens 后自动停止

**实战案例对比：**

| 目录 | Python 文件数 | Markdown 文件数 | Python 轮数 | Markdown 轮数 | 总耗时 |
|------|--------------|----------------|------------|--------------|--------|
| 03_teams | 118 | 48 | 2 轮（38% 停止）| 1 轮 | 3 次 Task |
| 04_workflows | 79 | 52 | 3 轮（28%→35%→100%）| 1 轮 | 4 次 Task |

**经验教训**：
- Python Task 第一轮完成度：25-38%（视文件复杂度）
- Markdown Task 第一轮完成度：100%（无需 resume）
- Python 文件数 < 50：通常 2 轮
- Python 文件数 50-100：通常 2-3 轮
- Python 文件数 > 100：通常 3-4 轮

## 常见问题

**Q: Python Task 只完成了 28%，是失败了吗？**
A: 不是。这是正常的停止点。立即 resume 继续即可。通常需要 2-3 轮才能完成所有 Python 文件。

**Q: Markdown Task 为什么能一次完成 50+ 文件？**
A: 因为使用 Write 工具整体写入，效率极高。且 md 文件相对简单，token 消耗低。

**Q: 需要手动检查每个文件的翻译质量吗？**
A: 不需要。翻译规则清晰，Task 会保持一致性。最后抽查几个文件即可。

**Q: 多次 resume 会不会重复翻译？**
A: 不会。Task 保持上下文，知道哪些已完成，哪些未完成。

**Q: 什么时候应该放弃 resume，重新启动新 Task？**
A: 如果连续 3 轮 resume 进度都很慢（< 10%），可以考虑重新启动。但通常 2-3 轮就能完成。
