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

### 单个目录（< 10 个文件）
1. 用 `Glob` 找到所有 `.py` 和 `.md` 文件
2. 逐文件 `Read` + `StrReplace` 翻译
3. Markdown 用 `StrReplace` 逐段替换（不用 Write）

### 大型目录（> 10 个文件）
1. **并行 Glob**：同时查找 `.py` 和 `.md` 文件
2. **按功能模块分组**：把相关目录组合成 2-4 个批次
3. **并行启动 Task**：每个 Task 处理 1-2 个目录（推荐 4 个并行任务）
4. **Task 提示词模板**：
   ```
   翻译 <目录路径> 目录下所有 .py 和 .md 文件的英文内容为中文。
   
   翻译规则：
   1. Python文件：翻译注释、docstring、instructions变量内容，保留代码逻辑
   2. Markdown文件：全文翻译
   3. 技术术语保留英文：Agent、Workflow、Knowledge、Storage、Memory等
   4. 用StrReplace逐段替换，保持格式
   
   完成后告诉我翻译了哪些内容。
   ```

### 根目录 + 子目录结构
- 根目录文件单独处理（通常只有 README.md）
- 按子目录分组并行处理
- 例：`02_agents/` 拆分为 4 组并行任务

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

## 性能优化

### 并行处理策略
- **小型任务**（< 10 文件）：直接顺序处理
- **中型任务**（10-50 文件）：2-4 个并行 Task
- **大型任务**（> 50 文件）：按功能模块拆分，4 个并行 Task

### 实战经验
1. **优先并行 Glob**：同时查找 `.py` 和 `.md` 避免等待
2. **合理分组**：相关目录分到同一 Task（如 session/caching/logging 一组）
3. **Task 数量控制**：最多 4 个并行，避免超载
4. **subagent_type**：使用 `generalPurpose`
5. **避免 Write**：Markdown 也用 `StrReplace`，保持一致性

### Task 提示词要点
- 明确目录列表
- 说明翻译规则（4 条核心规则）
- 要求报告翻译内容
- 保持简洁清晰
