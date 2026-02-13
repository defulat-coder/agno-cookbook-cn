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

**Python 文件 Task：**
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

使用 StrReplace 逐段替换。完成后报告翻译的文件数和目录。
```

**Markdown 文件 Task：**
```
翻译 <目录路径> 目录下所有 Markdown 文件的英文内容为中文。

全文翻译：标题、段落、列表、表格。代码块中的注释也翻译，代码本身不翻译。

技术术语保留英文或附中文说明：Agent、Team（团队）、Workflow（工作流）等。

使用 Write 直接写入翻译后内容。完成后报告翻译的文件数。
```

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
1. **首次启动**：2 个 Task（py + md）
2. **检查完成度**：Task 返回后查看是否全部完成
3. **继续推进**：对未完成的 Task 使用 `resume` 参数继续
4. **重复直到完成**：通常 2-3 轮 resume 可完成 100+ 文件

示例：
```python
# 首次启动
Task(prompt="翻译所有Python文件...", subagent_type="generalPurpose")

# 若未完成，resume 继续
Task(
    prompt="继续翻译剩余70个文件...", 
    resume="agent-id-from-first-call",
    subagent_type="generalPurpose"
)
```

### 翻译优先级（大型目录）
在 Python Task 中按优先级翻译：
1. **高频使用**（必须完整）：01_quickstart、session、tools、knowledge
2. **核心功能**（详细翻译）：context、hooks、guardrails、memory
3. **扩展功能**（快速翻译）：仅 docstring + instructions

### 实战经验总结
1. ✅ **先 Glob 两次**：并行查找 py 和 md，避免串行等待
2. ✅ **Markdown 用 Write**：比 StrReplace 快得多
3. ✅ **Python 用 StrReplace**：保持格式和结构
4. ✅ **2 Task + Resume**：比 4 Task 并行更可控、更可靠
5. ✅ **检查进度后 Resume**：Task 返回后立即检查完成度，未完成则继续
6. ❌ **避免 4 个并行 Task**：大量文件时每个 Task 都太重，容易中断
7. ❌ **避免过细拆分**：10 个小 Task 不如 2 个大 Task + resume

### Token 管理
- **中小型任务**：单次会话完成（< 50k tokens）
- **大型任务**：2-3 轮 resume，每轮消耗 30-50k tokens
- **超大型任务**：可能需要新会话继续，但已翻译部分已提交
