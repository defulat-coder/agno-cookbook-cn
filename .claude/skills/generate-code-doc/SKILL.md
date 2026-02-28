---
name: generate-code-doc
description: Use when analyzing agno-cookbook Python source files to generate implementation principle documentation (.md). Use when the user asks to generate code analysis, implementation docs, or principle documentation for .py files.
---

# Agno 代码原理文档生成

分析 agno-cookbook 中的 Python 源文件，生成结构化的实现原理分析文档（.md），覆盖 Agent 配置、prompt 组装、API 请求、源码索引等。

## 适用场景

- 用户要求对某个 `.py` 文件生成原理分析文档
- 用户要求对某个目录批量生成所有 `.py` 文件的原理文档
- 用户提到"实现原理"、"代码分析"、"原理文档"等关键词

## 输出规范

- 文件名：`<源文件名>.md`（如 `few_shot_learning.py` → `few_shot_learning.md`）
- 输出位置：与源 `.py` 文件同目录
- 语言：中文

## 文档模板结构

每个 `.md` 文件必须包含以下章节，按顺序排列：

### 1. 标题与源文件引用

```markdown
# <文件名>.py — 实现原理分析

> 源文件：`<相对路径>/<文件名>.py`
```

### 2. 概述

一段话总结该示例展示的 Agno 核心机制，加粗关键特性名。末尾附「核心配置一览」表格：

```markdown
## 概述

本示例展示 Agno 的 **`<核心特性名>`** 机制：<一句话描述原理和用途>。

**核心配置一览：**

| 配置项 | 值 | 说明 |
|--------|------|------|
| `name` | `"xxx"` | Agent 名称 |
| `model` | `OpenAIChat(id="gpt-4o")` | Chat Completions API |
| `instructions` | ... | ... |
| `tools` | ... | ... |
| ... | ... | ... |
```

配置表规则：
- 列出 Agent 构造函数的**所有显式参数**
- 对未设置的重要参数也要列出（值填 `None`，说明填"未设置"）
- model 列标注 API 类型（Chat Completions / Responses）

### 3. 架构分层

ASCII 文本图，展示用户代码层 → agno.agent 层 → 模型层的数据流：

```markdown
## 架构分层

​```
用户代码层                agno.agent 层
┌──────────────────┐    ┌──────────────────────────────────┐
│ <文件名>.py      │    │ Agent._run()                     │
│                  │    │  ├ _messages.py                  │
│ <关键参数>       │───>│  │  get_system_message()          │
│                  │    │  │    → <处理逻辑概要>            │
│                  │    │  │                                │
│                  │    │  │  get_run_messages()            │
│                  │    │  │    <消息组装概要>              │
└──────────────────┘    └──────────────────────────────────┘
                                │
                                ▼
                        ┌──────────────┐
                        │ <Model类>    │
                        │ <model_id>   │
                        └──────────────┘
​```
```

规则：
- 左侧为用户代码层，展示关键参数
- 右侧为 agno 内部处理层，展示调用链
- 底部为模型层
- 如涉及工具、知识库等额外组件，在右侧或底部扩展

### 4. 核心组件解析

逐个分析该文件使用的 Agno 核心机制，附源码引用：

```markdown
## 核心组件解析

### <组件名1>

`<组件名>` 在 `<函数名>()`（`<文件>:<行号>`）中处理：

​```python
# 关键源码片段（带中文注释）
​```

<解释这段代码的作用和原理>

### <组件名2>
...
```

规则：
- 每个组件单独一个 `###` 子章节
- 引用 agno 源码时标注文件路径和行号
- 代码片段保留关键逻辑，添加中文注释
- 如有对比场景（如有/无某配置），用表格对比

### 5. System Prompt 组装

表格列出 system prompt 的所有组成部分及其在本文件中的状态：

```markdown
## System Prompt 组装

| 序号 | 组成部分 | 本文件中的值/来源 | 是否生效 |
|------|---------|-----------------|---------|
| 1 | `description` | ... | 是/否 |
| 2 | `role` | ... | 是/否 |
| 3 | `instructions` | ... | 是/否 |
| 4.1 | `markdown` | ... | 是/否 |
| 4.2 | `add_datetime_to_context` | ... | 是/否 |
| 4.3 | `add_location_to_context` | ... | 是/否 |
| 4.4 | `add_name_to_context` | ... | 是/否 |
| 5-12 | 其余段落 | ... | 否 |

### 最终 System Prompt

​```text
<实际生成的 system prompt 内容>
​```
```

### 6. 完整 API 请求

模拟实际发送给 LLM 的完整请求：

```markdown
## 完整 API 请求

​```python
client.chat.completions.create(
    model="<model_id>",
    messages=[
        # 1. System Message
        {"role": "developer", "content": "..."},
        # 2. 其他消息（如有 additional_input、history 等）
        ...
        # N. 当前用户输入
        {"role": "user", "content": "..."}
    ],
    tools=[...],  # 如有
    stream=True,
    stream_options={"include_usage": True}
)
​```

> <补充说明>
```

规则：
- 展示完整的 messages 数组
- 如有 tools 参数，也要展示
- 用注释标注每部分消息的来源
- 末尾用引用块补充说明

### 7. Mermaid 流程图

```markdown
## Mermaid 流程图

​```mermaid
flowchart TD
    A["用户代码<br/>agent.print_response(...)"] --> B["Agent._run()"]
    B --> C["get_system_message()"]

    subgraph System Prompt 组装
        C --> C1[...]
        ...
    end

    ... --> E["<Model>.invoke()"]
    E --> F["模型响应"]
    F --> G["流式输出"]

    style A fill:#e1f5fe
    style G fill:#e8f5e9
    style <关键节点> fill:#fff3e0
​```
```

规则：
- 用 `subgraph` 分组相关步骤
- 入口节点用 `#e1f5fe`（浅蓝），出口节点用 `#e8f5e9`（浅绿）
- 关键机制节点用 `#fff3e0`（浅橙）
- 如涉及条件分支，用菱形节点
- 如涉及工具调用循环，展示 agentic loop

### 8. 关键源码文件索引

```markdown
## 关键源码文件索引

| 文件 | 关键函数/类 | 作用 |
|------|------------|------|
| `agno/agent/agent.py` | `<属性名>` L<行号> | <作用> |
| `agno/agent/_messages.py` | `<函数名>()` L<行号> | <作用> |
| ... | ... | ... |
```

规则：
- 只列与本文件核心机制直接相关的源码
- 标注行号（格式 `L<起始>-<结束>` 或 `L<行号>`）
- 按调用链顺序排列

## 分析工作流程

### 单文件模式

1. **Read** 目标 `.py` 文件，理解代码逻辑
2. **定位核心 Agno 特性**：识别 Agent 构造参数中的关键机制
3. **追踪 agno 源码**：
   - `Grep` 搜索 agno 库中相关属性/函数的实现
   - `Read` 关键源码文件（`_messages.py`、`agent.py`、`_tools.py` 等）
   - 记录行号
4. **组装文档**：按模板结构依次生成各章节
5. **Write** 输出到同目录的 `.md` 文件

### 批量模式（整个目录）

1. **Glob** 目标目录下所有 `.py` 文件
2. **过滤**：排除 `__init__.py`、`__pycache__` 等非示例文件
3. **统计**文件数量，决定策略：

| Python 文件数 | 策略 | Agent 数 |
|--------------|------|---------|
| ≤ 5 | 直接处理，不启动 Agent | 0 |
| 6-15 | 启动 2 个 Agent 并行 | 2 |
| 16-30 | 启动 3 个 Agent 并行 | 3 |
| > 30 | 启动 4 个 Agent 并行 | 4 |

4. **分组**：按文件数均匀分配到各 Agent
5. 每个 Agent 的提示词模板：

```
分析以下 agno-cookbook Python 文件，为每个文件生成实现原理文档。

文件列表（共 <N> 个）：
- <文件路径1>
- <文件路径2>
- ...

对每个文件执行以下步骤：
1. Read 文件，理解代码逻辑
2. 识别使用的 Agno 核心特性（Agent 参数、tools、knowledge、storage 等）
3. Grep agno 源码追踪相关实现（_messages.py、agent.py、_tools.py 等），记录行号
4. 按以下模板结构生成 .md 文件（Write 到源文件同目录）：
   - 标题 + 源文件引用
   - 概述 + 核心配置一览表格
   - 架构分层（ASCII 图）
   - 核心组件解析（附源码片段和行号）
   - System Prompt 组装表格 + 最终 prompt
   - 完整 API 请求
   - Mermaid 流程图
   - 关键源码文件索引

语言：中文
输出位置：与源 .py 文件同目录，文件名为 <源文件名>.md

【重要】处理完列表中所有文件后再报告，不要中途停止。
完成后报告已生成的文件数和文件列表。
```

## Agno 源码追踪指南

分析时需要追踪的 agno 核心源码文件：

| 机制 | 关键源码文件 | 关键函数 |
|------|------------|---------|
| System Prompt | `agno/agent/_messages.py` | `get_system_message()` |
| 消息组装 | `agno/agent/_messages.py` | `get_run_messages()` |
| Agent 属性 | `agno/agent/agent.py` | Agent 类定义 |
| 工具处理 | `agno/agent/_tools.py` | `get_tools()` |
| 可调用工厂 | `agno/utils/callables.py` | `invoke_callable_factory()` |
| 知识库 | `agno/knowledge/` | 各 KnowledgeBase 子类 |
| 存储 | `agno/storage/` | 各 Storage 子类 |
| 记忆 | `agno/memory/` | Memory 类 |
| 模型适配 | `agno/models/` | 各模型的 `invoke()` / `ainvoke()` |
| Team | `agno/team/` | Team 类 |
| Workflow | `agno/workflow/` | Workflow 类 |

追踪技巧：
- 用 `Grep` 搜索属性名在 `_messages.py` 中的处理位置
- 关注 `get_system_message()` 的分段注释（`# 3.1`, `# 3.2` 等）
- 记录行号时使用 `L<行号>` 格式

## 注意事项

- **不要虚构行号**：必须通过实际 Read/Grep 确认源码行号
- **不要遗漏配置项**：核心配置一览表要列出所有显式参数
- **API 请求要准确**：根据实际的模型类型确定 role（`developer` for OpenAI Chat，`user` for Responses API 等）
- **Mermaid 节点 ID 不能有空格**：用驼峰或下划线命名
- **跳过已存在的 .md 文件**：批量模式下，如果同名 .md 已存在则跳过
