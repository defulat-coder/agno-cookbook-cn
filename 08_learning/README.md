# Agents 2.0: The Learning Machine（学习机器）

构建能够学习、适应和改进的 agent 的全面指南。

## 概述

LearningMachine 是一个统一的学习系统，使 agent 能够从每次交互中学习。它协调多个**学习存储（learning stores）**，每个存储处理不同类型的知识：

| Store（存储） | 捕获内容 | 作用范围 | 使用场景 |
|-------|------------------|-------|----------|
| **User Profile**（用户档案） | 结构化字段（姓名、偏好） | 每个用户 | 个性化 |
| **User Memory**（用户记忆） | 关于用户的非结构化观察 | 每个用户 | 上下文、偏好 |
| **Session Context**（会话上下文） | 目标、计划、进度、摘要 | 每个会话 | 任务连续性 |
| **Entity Memory**（实体记忆） | 事实、事件、关系 | 可配置 | CRM、知识图谱 |
| **Learned Knowledge**（学习知识） | 洞察、模式、最佳实践 | 可配置 | 集体智能 |

## 快速开始

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIResponses

# 设置
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 最简单的学习 agent
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=True,  # 就这样！
)

# 使用它
agent.print_response(
    "I'm Alex, I prefer concise answers.",
    user_id="alex@example.com",
    session_id="session_1",
)
```

## Cookbook 结构

```
cookbook/08_learning/
├── 01_basics/              # 从这里开始 - 基础示例
│   ├── 1a_user_profile_always.py
│   ├── 1b_user_profile_agentic.py
│   ├── 2a_user_memory_always.py
│   ├── 2b_user_memory_agentic.py
│   ├── 3a_session_context_summary.py
│   ├── 3b_session_context_planning.py
│   ├── 4_learned_knowledge.py
│   ├── 5a_entity_memory_always.py
│   └── 5b_entity_memory_agentic.py
│
├── 02_user_profile/        # 用户档案深入探讨
│   ├── 01_always_extraction.py
│   ├── 02_agentic_mode.py
│   └── 03_custom_schema.py
│
├── 03_session_context/     # 会话跟踪深入探讨
│   ├── 01_summary_mode.py
│   └── 02_planning_mode.py
│
├── 04_entity_memory/       # 实体记忆深入探讨
│   ├── 01_facts_and_events.py
│   └── 02_entity_relationships.py
│
├── 05_learned_knowledge/   # 学习知识深入探讨
│   ├── 01_agentic_mode.py
│   └── 02_propose_mode.py
│
└── 07_patterns/            # 真实世界模式
    ├── personal_assistant.py
    └── support_agent.py
```

## 运行 Cookbook

### 1. 克隆仓库

```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

### 2. 创建虚拟环境并安装依赖

使用设置脚本（需要 `uv`）：

```bash
./cookbook/08_learning/setup_venv.sh
```

或手动操作：
```bash
python -m venv .venv
source .venv/bin/activate
uv pip install -r cookbook/08_learning/requirements.txt
```

### 3. 导出环境变量

```bash
# 访问 OpenAI 模型所需
export OPENAI_API_KEY=your-openai-api-key
```

### 4. 运行 Postgres 与 PgVector

Postgres 存储 agent 会话、记忆、知识和状态。安装 [Docker Desktop](https://docs.docker.com/desktop/install/mac-install/) 并运行：

```bash
./cookbook/scripts/run_pgvector.sh
```

或直接运行：
```bash
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql \
  -v pgvolume:/var/lib/postgresql \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:18
```

### 5. 运行 Cookbook

```bash
# 从基础开始
python cookbook/08_learning/01_basics/1a_user_profile_always.py

# 或运行任何特定示例
python cookbook/08_learning/02_user_profile/03_custom_schema.py
python cookbook/08_learning/07_patterns/personal_assistant.py
```

---

## 核心概念

### 目标
在第 1000 次交互时的 agent 从根本上优于第 1 次交互时的它。

### 优势
无需分别构建记忆、知识和反馈系统，只需配置一个系统，以一致的模式处理所有学习。

### 三个 DX 级别

```python
# 级别 1：极其简单
agent = Agent(model=model, db=db, learning=True)

# 级别 2：选择你想要的
agent = Agent(
    model=model,
    db=db,
    learning=LearningMachine(
        user_profile=True,
        session_context=True,
        entity_memory=False,
        learned_knowledge=False,
    ),
)

# 级别 3：完全控制
agent = Agent(
    model=model,
    db=db,
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.AGENTIC,
        ),
        session_context=SessionContextConfig(
            enable_planning=True,
        ),
    ),
)
```

### 学习模式

每个 Learning Store 可以配置为在不同模式下运行：

```python
from agno.learn import LearningMode

# ALWAYS（user_profile、session_context 的默认值）
# - 对话后自动提取
# - 不需要 agent 工具
# - 每次交互额外一次 LLM 调用

# AGENTIC（learned_knowledge 的默认值）
# - Agent 通过工具决定何时保存
# - 更多控制，更少噪音
# - 无额外 LLM 调用

# PROPOSE
# - Agent 提议，用户确认
# - 人在回路中的质量控制
# - 适合高风险知识
```

### 内置学习存储

#### 1. User Profile Store（用户档案存储）

捕获关于用户的结构化档案字段。永久保存。随着新信息的学习而更新。

**支持的模式：** ALWAYS、AGENTIC

**存储的数据：** `name`、`preferred_name` 以及您定义的任何自定义字段。

另见：**Memories Store**（记忆存储）用于不适合字段的非结构化观察。

```python
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, UserProfileConfig

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    learning=LearningMachine(
        user_profile=UserProfileConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
)

# 会话 1
agent.run("I'm Alice, I work at Netflix", user_id="alice")

# 会话 2
agent.run("What do you know about me?", user_id="alice")
# -> "You're Alice, you work at Netflix"
```

#### 2. User Memory Store（用户记忆存储）

捕获关于用户的非结构化观察，这些观察不适合结构化档案字段。

**支持的模式：** ALWAYS、AGENTIC

**何时使用：** 用于像"喜欢详细解释"、"从事 ML 项目"这样的上下文 - 有用但不结构化的观察。

```python
from agno.learn import LearningMachine, UserMemoryConfig, LearningMode

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    learning=LearningMachine(
        user_memory=UserMemoryConfig(
            mode=LearningMode.ALWAYS,
        ),
    ),
)

# 会话 1
agent.run("I prefer code examples over explanations", user_id="alice")

# 会话 2 - 记忆保持
agent.run("Explain async/await", user_id="alice")
# Agent 知道 Alice 喜欢代码示例并调整响应
```

#### 3. Session Context Store（会话上下文存储）

捕获当前会话的状态和摘要。

**支持的模式：** 仅 ALWAYS

**存储的数据：**
- **Summary**（摘要）：当前会话的简要摘要
- **Goal**（目标）：当前会话的目标（需要 `enable_planning=True`）
- **Plan**（计划）：实现目标的步骤（需要 `enable_planning=True`）
- **Progress**（进度）：已完成的步骤（需要 `enable_planning=True`）

```python
from agno.learn import LearningMachine, SessionContextConfig

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    learning=LearningMachine(
        session_context=SessionContextConfig(
            enable_planning=True,
        ),
    ),
)

# 会话上下文自动跟踪目标、计划、进度
```

#### 4. Learned Knowledge Store（学习知识存储）

捕获适用于跨用户和会话的可重用洞察、模式和规则。

**支持的模式：** AGENTIC、PROPOSE、ALWAYS

**需要知识库**（向量数据库）进行语义搜索。

```python
from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.learn import LearningMachine, LearnedKnowledgeConfig, LearningMode
from agno.vectordb.pgvector import PgVector, SearchType

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    vector_db=PgVector(
        db_url=db_url,
        table_name="agent_learnings",
        search_type=SearchType.hybrid,
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    ),
)

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        knowledge=knowledge,
        learned_knowledge=LearnedKnowledgeConfig(
            mode=LearningMode.AGENTIC,
        ),
    ),
)
```

#### 5. Entity Memory Store（实体记忆存储）

捕获关于外部实体的知识：公司、项目、人员、产品、系统。

**支持的模式：** ALWAYS、AGENTIC

**三种类型的实体数据：**
- **Facts**（事实，语义记忆）：永恒的真理 - "使用 PostgreSQL"
- **Events**（事件，情景记忆）：时间相关的发生 - "在 1 月 15 日发布 v2"
- **Relationships**（关系，图边）：连接 - "Bob 是 Acme 的 CTO"

```python
from agno.learn import LearningMachine, EntityMemoryConfig

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai"),
    learning=LearningMachine(
        entity_memory=EntityMemoryConfig(
            namespace="global",
        ),
    ),
)

# Agent 从对话中学习实体
agent.run("Acme Corp just migrated to PostgreSQL and hired Bob as CTO")

# 稍后，agent 可以回忆并使用这些知识
agent.run("What database does Acme use?")
# -> "Acme Corp uses PostgreSQL"
```

### 自定义模式

使用类型化字段扩展基础模式以适应您的领域：

```python
from dataclasses import dataclass, field
from typing import Optional
from agno.learn.schemas import UserProfile

@dataclass
class CustomerProfile(UserProfile):
    """客户支持的扩展用户档案。"""

    company: Optional[str] = field(
        default=None,
        metadata={"description": "公司或组织"}
    )
    plan_tier: Optional[str] = field(
        default=None,
        metadata={"description": "订阅等级：free | pro | enterprise"}
    )

# 使用自定义模式
learning = LearningMachine(
    user_profile=UserProfileConfig(
        schema=CustomerProfile,
    ),
)
```

## 了解更多

- [Agno 文档](https://docs.agno.com)

Built with 💜 by the Agno team
