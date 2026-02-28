# 04_manually_add_culture.py — 实现原理分析

> 源文件：`02_agents/culture/04_manually_add_culture.py`

## 概述

本示例展示如何**手动创建文化知识**并在 Agent 中使用：直接构造 `CulturalKnowledge` 数据对象，通过 `CultureManager.add_cultural_knowledge()` 存入数据库，**无需 LLM 参与**。与 01 的区别在于：01 通过 LLM 从自然语言中提炼文化知识，而本例通过代码直接定义结构化的文化知识条目。随后创建 Agent 并启用 `add_culture_to_context=True` 来使用这些手动添加的知识。

**核心配置一览：**

| 配置项 | 值 | 说明 |
|--------|------|------|
| `CultureManager` | `CultureManager(db=db)` | 无 model（手动添加不需要 LLM） |
| `CulturalKnowledge` | 手动构造 dataclass 实例 | 直接定义 name/summary/content 等 |
| `Agent.model` | `Claude(id="claude-sonnet-4-5")` | Anthropic Messages API |
| `Agent.db` | `SqliteDb(db_file="tmp/demo.db")` | SQLite 存储 |
| `Agent.add_culture_to_context` | `True` | 将文化知识注入 system prompt |
| `instructions` | `None` | 未设置 |
| `tools` | `None` | 无工具 |

---

## 架构分层

```
用户代码层                    CultureManager 层              Agent 运行层
┌───────────────────────┐    ┌────────────────────┐    ┌──────────────────┐
│ 04_manually_add_      │    │ CultureManager     │    │ Agent._run()     │
│ culture.py            │    │   (无 model)       │    │                  │
│                       │    │                    │    │ get_system_      │
│ 1. 构造               │    │ add_cultural_      │    │ message()        │
│    CulturalKnowledge  │───>│ knowledge()        │    │  § 3.3.10:       │
│    (dataclass)        │    │   → 直接写入 DB    │    │  culture         │
│                       │    │   （无 LLM 调用）  │    │  injection       │
│ 2. culture_manager.   │    │                    │    │                  │
│    add_cultural_      │    │ get_all_knowledge()│<───│ get_all_         │
│    knowledge(obj)     │    │   → 从 DB 读取     │    │ knowledge()      │
│                       │    │                    │    │                  │
│ 3. Agent(             │    │                    │    │ → system prompt  │
│    add_culture_to_    │    │                    │    │   含文化知识     │
│    context=True)      │──────────────────────────────>│                  │
│                       │    │                    │    │ Claude.invoke_   │
│                       │    │                    │    │ stream()         │
└───────────────────────┘    └────────────────────┘    └──────────────────┘
                                     │                         │
                                     ▼                         ▼
                             ┌──────────────┐          ┌──────────────┐
                             │ SqliteDb     │          │ Anthropic API│
                             │ (tmp/demo.db)│          │ messages.    │
                             └──────────────┘          │ stream()     │
                                                       └──────────────┘
```

---

## 核心组件解析

### CulturalKnowledge 手动构造

直接使用 dataclass 构造文化知识条目：

```python
response_format = CulturalKnowledge(
    name="响应格式标准（Agno）",
    summary="保持响应简洁、可扫描，并在适用时优先提供可运行的内容。",
    categories=["communication", "ux"],
    content=(
        "- 在可能的情况下，优先提供最小可运行的代码片段或示例。\n"
        "- 对于过程使用编号步骤；保持每个步骤可测试。\n"
        "- 优先使用公制单位和明确的默认值（端口、路径、版本）。\n"
        "- 以简短的验证清单结束。"
    ),
    notes=["源自重复反馈，支持可操作的答案。"],
    metadata={"source": "manual_seed", "version": 1},
)
```

`CulturalKnowledge` dataclass（`db/schemas/culture.py:9-31`）的字段：

| 字段 | 类型 | 本例值 | 作用 |
|------|------|--------|------|
| `id` | `Optional[str]` | 自动生成 UUID | 唯一标识 |
| `name` | `Optional[str]` | `"响应格式标准（Agno）"` | 简短标题（system prompt 中显示） |
| `summary` | `Optional[str]` | `"保持响应简洁..."` | 一行摘要（system prompt 中显示） |
| `content` | `Optional[str]` | 4 条规则 | 具体内容（system prompt 中显示） |
| `categories` | `Optional[List[str]]` | `["communication", "ux"]` | 标签分类 |
| `notes` | `Optional[List[str]]` | `["源自重复反馈..."]` | 上下文注释 |
| `metadata` | `Optional[Dict]` | `{"source": "manual_seed", ...}` | 元数据 |
| `created_at` | `Optional[int]` | 自动设置 | 创建时间戳 |
| `updated_at` | `Optional[int]` | 自动设置 | 更新时间戳 |

### add_cultural_knowledge（手动添加）

`CultureManager.add_cultural_knowledge()`（`culture/manager.py:142-170`）直接将 CulturalKnowledge 写入数据库，**不调用 LLM**：

```python
def add_cultural_knowledge(self, knowledge: CulturalKnowledge) -> str:
    """直接将 CulturalKnowledge 条目添加到数据库。"""
    if knowledge.id is None:
        knowledge.id = str(uuid4())     # 自动生成 UUID
    if knowledge.created_at is None:
        knowledge.created_at = int(time())
    if knowledge.updated_at is None:
        knowledge.updated_at = int(time())

    if self.db is not None:
        self.db.upsert_cultural_knowledge(knowledge)
    return f"Cultural knowledge '{knowledge.name}' added successfully."
```

与 01（`create_cultural_knowledge`）的关键区别：

| 方法 | 需要 model | LLM 调用 | 输入 | 适用场景 |
|------|-----------|---------|------|---------|
| `add_cultural_knowledge()` | 否 | 无 | `CulturalKnowledge` 对象 | 手动/编程方式添加 |
| `create_cultural_knowledge()` | 是 | 有（完整工具调用循环） | 自然语言字符串 | 从文本中自动提取 |

### CultureManager 无 model 初始化

```python
culture_manager = CultureManager(db=db)
# → CultureManager(model=None, db=SqliteDb("tmp/demo.db"))
```

这是合法的，因为 `add_cultural_knowledge()` 和 `get_all_knowledge()` 仅与数据库交互，不需要模型。

### Agent 中使用文化知识

Agent 的文化知识注入逻辑与 02 完全相同（`_messages.py:322-354`）：

1. `add_culture_to_context=True` → 触发 § 3.3.10
2. `get_all_knowledge()` → 读取手动添加的 CulturalKnowledge
3. 将 name/summary/content 注入到 `<cultural_knowledge>` 标签中

---

## System Prompt 组装

| 序号 | 组成部分 | 本文件中的值/来源 | 是否生效 |
|------|---------|-----------------|---------|
| 1 | `description` | `None` | 否 |
| 2 | `role` | `None` | 否 |
| 3 | `instructions` | `None` | 否 |
| 4.1 | `markdown` | `True`（print_response 传入） | **生效** |
| 4.2-4.4 | 其余 additional_information | 默认关闭 | 否 |
| 5-9 | tools/memory/knowledge 等 | 均无 | 否 |
| 10 | `add_culture_to_context` | `True` | **生效** |
| 11-12 | session_summary 等 | 默认关闭 | 否 |

### 最终 System Prompt

```text
<additional_information>
- Use markdown to format your answers.
</additional_information>

You have access to shared **Cultural Knowledge**, which provides context, norms, rules and guidance for your reasoning, communication, and decision-making. Cultural Knowledge represents the collective understanding, values, rules and practices that have emerged across agents and teams. It encodes collective experience — including preferred approaches, common patterns, lessons learned, and ethical guardrails.

When performing any task:
- **Reference Cultural Knowledge** to align with shared norms and best practices.
- **Apply it contextually**, not mechanically — adapt principles to the current situation.
- **Preserve consistency** with cultural values (tone, reasoning, and style) unless explicitly told otherwise.
- **Extend it** when you discover new insights — your outputs may become future Cultural Knowledge.
- **Clarify conflicts** if Cultural Knowledge appears to contradict explicit user instructions.

Your goal is to act not only intelligently but also *culturally coherently* — reflecting the collective intelligence of the system.

Below is the currently available Cultural Knowledge for this context:

<cultural_knowledge>
---
Name: 响应格式标准（Agno）
Summary: 保持响应简洁、可扫描，并在适用时优先提供可运行的内容。
Content: - 在可能的情况下，优先提供最小可运行的代码片段或示例。
- 对于过程使用编号步骤；保持每个步骤可测试。
- 优先使用公制单位和明确的默认值（端口、路径、版本）。
- 以简短的验证清单结束。
</cultural_knowledge>
```

---

## 完整 API 请求

仅一次 API 调用（Agent 主流程），无后台 CultureManager 调用：

```python
client.messages.stream(
    model="claude-sonnet-4-5",
    messages=[
        {
            "role": "user",
            "content": [{"type": "text", "text": "如何使用 Docker 设置 FastAPI 服务？"}]
        }
    ],
    system=[
        {
            "type": "text",
            "text": "<additional_information>\n- Use markdown to format your answers.\n</additional_information>\n\nYou have access to shared **Cultural Knowledge**...\n\nBelow is the currently available Cultural Knowledge for this context:\n\n<cultural_knowledge>\n---\nName: 响应格式标准（Agno）\nSummary: 保持响应简洁、可扫描，并在适用时优先提供可运行的内容。\nContent: - 在可能的情况下，优先提供最小可运行的代码片段或示例。\n- 对于过程使用编号步骤；保持每个步骤可测试。\n- 优先使用公制单位和明确的默认值（端口、路径、版本）。\n- 以简短的验证清单结束。\n</cultural_knowledge>\n"
        }
    ],
    max_tokens=8192
)
```

> Agent 会参考 `<cultural_knowledge>` 中的格式标准，在回答中优先提供最小可运行代码片段、使用编号步骤、以验证清单结束。

---

## 手动 vs 自动 vs LLM 提取 对比

```
01 LLM 提取                  03 自动更新                    04 手动添加
┌───────────────────┐    ┌───────────────────┐    ┌───────────────────┐
│ 自然语言文本      │    │ Agent 每次运行后  │    │ 代码直接构造      │
│ ↓                 │    │ ↓                 │    │ CulturalKnowledge │
│ CultureManager    │    │ 后台线程          │    │ ↓                 │
│ .create_cultural_ │    │ start_cultural_   │    │ CultureManager    │
│ knowledge(msg)    │    │ knowledge_future()│    │ .add_cultural_    │
│ ↓                 │    │ ↓                 │    │ knowledge(obj)    │
│ LLM 分析 + 工具   │    │ CultureManager    │    │ ↓                 │
│ ↓                 │    │ .create_cultural_ │    │ 直接写入 DB       │
│ add_cultural_     │    │ knowledge()       │    │ （无 LLM 调用）   │
│ knowledge 工具    │    │ ↓                 │    │                   │
│ ↓                 │    │ LLM 分析 + 工具   │    │                   │
│ 写入 DB           │    │ ↓                 │    │ 需要 model: 否    │
│                   │    │ 写入 DB           │    │ 需要 db: 是       │
│ 需要 model: 是    │    │                   │    │ API 调用: 0       │
│ 需要 db: 是       │    │ 需要 model: 是    │    │                   │
│ API 调用: 1+      │    │ 需要 db: 是       │    │ 适用: 预定义知识  │
│                   │    │ API 调用: 1+      │    │   种子数据        │
│ 适用: 从用户输入  │    │                   │    │   确定性内容      │
│   提取知识        │    │ 适用: 持续学习    │    │                   │
│                   │    │   隐式积累        │    │                   │
└───────────────────┘    └───────────────────┘    └───────────────────┘
```

---

## Mermaid 流程图

```mermaid
flowchart TD
    A["用户代码<br/>构造 CulturalKnowledge 对象"] --> B["CultureManager(db=db)<br/>无 model"]

    B --> C["culture_manager.add_cultural_knowledge(obj)"]

    subgraph 手动添加（无 LLM）
        C --> C1["生成 UUID (id)"]
        C1 --> C2["设置 created_at / updated_at"]
        C2 --> C3["db.upsert_cultural_knowledge()"]
        C3 --> C4["存入 SQLite"]
    end

    C4 --> D["Agent(<br/>  model=Claude,<br/>  db=db,<br/>  add_culture_to_context=True)"]

    D --> E["agent.print_response(<br/>  '如何使用 Docker 设置 FastAPI 服务？')"]
    E --> F["Agent._run()"]

    F --> G["get_system_message()"]

    subgraph System Prompt 组装
        G --> G1["markdown=True → additional_information"]
        G1 --> G2["§ 3.3.10: add_culture_to_context"]
        G2 --> G3["get_all_knowledge()<br/>→ 读取手动添加的 CulturalKnowledge"]
        G3 --> G4["注入引导段 + <cultural_knowledge><br/>Name / Summary / Content"]
    end

    G4 --> H["messages = [system, user]"]
    H --> I["Claude.invoke_stream()"]
    I --> J["format_messages()<br/>→ system 分离"]
    J --> K["client.messages.stream(<br/>  model, messages, system,<br/>  max_tokens=8192)"]
    K --> L["流式输出<br/>（参考文化知识回答）"]

    style A fill:#e1f5fe
    style L fill:#e8f5e9
    style C fill:#fff3e0
    style G2 fill:#e8eaf6
```

---

## 关键源码文件索引

| 文件 | 关键函数/类 | 作用 |
|------|------------|------|
| `agno/culture/manager.py` | `add_cultural_knowledge()` L142 | 手动添加文化知识到 DB（无 LLM） |
| `agno/culture/manager.py` | `get_all_knowledge()` L123 | 从 DB 读取所有文化知识 |
| `agno/db/schemas/culture.py` | `CulturalKnowledge` L9 | 文化知识数据模型 dataclass |
| `agno/agent/_messages.py` | `get_system_message()` L322-354 | § 3.3.10 文化知识注入到 system prompt |
| `agno/agent/_init.py` | `set_culture_manager()` L81 | 自动创建/配置 CultureManager |
| `agno/agent/agent.py` | `add_culture_to_context` L329 | Agent 属性（启用文化知识注入） |
| `agno/models/anthropic/claude.py` | `Claude` L67 | Anthropic 模型适配器 |
| `agno/models/anthropic/claude.py` | `invoke_stream()` L639 | 流式调用 Messages API |
| `agno/models/anthropic/claude.py` | `_prepare_request_kwargs()` L527 | system 参数构建 |
| `agno/utils/models/claude.py` | `format_messages()` L265 | Message → Anthropic 格式（system 分离） |
