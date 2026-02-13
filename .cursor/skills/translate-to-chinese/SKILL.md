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
- `additional_instructions` 等 prompt 类变量
- 文件底部 `"""..."""` 中的说明文字

不翻译的内容：
- 代码逻辑、变量名、函数名、类名
- import 语句
- 字符串常量（非注释/文档用途的）
- Pydantic Field 的 `description` 参数（保留英文，因为是给模型的 schema）
- `role` 参数值（保留英文）

### Markdown 文件（.md）

全文翻译，包括：
- 标题、段落、列表
- 表格内容
- 代码块中的注释（代码本身不翻译）

### 其他文件

- `.yaml` / `.toml` 中的 `description` 字段
- shell 脚本中的注释

## 工作流程

1. 用 `Glob` 找到目标目录下的所有文件
2. 逐文件 `Read`，识别需要翻译的内容
3. 用 `StrReplace` 逐段替换英文为中文
4. 对于整文件翻译的 markdown，用 `Write` 直接写入

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

## 批量处理

文件较多时使用 `Task` 工具启动子 Agent 并行处理，每个子 Agent 处理一批文件。
