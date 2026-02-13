"""
Dash - 自学习数据 Agent
=================================

测试:
    python -m agents.dash.agent
"""

from os import getenv

from agno.agent import Agent
from agno.learn import (
    LearnedKnowledgeConfig,
    LearningMachine,
    LearningMode,
    UserMemoryConfig,
    UserProfileConfig,
)
from agno.models.openai import OpenAIResponses
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools
from agno.tools.sql import SQLTools
from db import create_knowledge, db_url, get_postgres_db

from .context.business_rules import BUSINESS_CONTEXT
from .context.semantic_model import SEMANTIC_MODEL_STR
from .tools import create_introspect_schema_tool, create_save_validated_query_tool

# ---------------------------------------------------------------------------
# 数据库 & 知识库
# ---------------------------------------------------------------------------

agent_db = get_postgres_db()

# 知识库：静态、人工维护的（表结构、验证过的查询、业务规则）
dash_knowledge = create_knowledge("Dash Knowledge", "dash_knowledge")

# 学习记录：动态、自动发现的（类型错误、日期格式、业务规则）
dash_learnings = create_knowledge("Dash Learnings", "dash_learnings")

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------

save_validated_query = create_save_validated_query_tool(dash_knowledge)
introspect_schema = create_introspect_schema_tool(db_url)

base_tools: list = [
    SQLTools(db_url=db_url),
    save_validated_query,
    introspect_schema,
    MCPTools(
        url=f"https://mcp.exa.ai/mcp?exaApiKey={getenv('EXA_API_KEY', '')}&tools=web_search_exa"
    ),
]

# ---------------------------------------------------------------------------
# 指令
# ---------------------------------------------------------------------------

INSTRUCTIONS = f"""\
你是 Dash，一个自学习数据 Agent，提供**洞察**，而不仅仅是查询结果。

## 你的目标

你是用户的数据分析师——一个永不遗忘、绝不重复犯错、
每次查询都在变聪明的分析师。

你不只是取数据。你解读数据、提供上下文、解释数据的含义。
你记住那些踩过的坑、类型不匹配、让你犯过错的日期格式。

你的目标：让用户看起来像已经跟这份数据打了多年交道。

## 双知识库系统

**知识库**（静态、人工维护）：
- 表结构、验证过的查询、业务规则
- 每次回复前自动搜索
- 用 `save_validated_query` 保存成功的查询

**学习记录**（动态、自动发现）：
- 你通过报错和修复发现的模式
- 类型踩坑、日期格式、列的特殊之处
- 用 `search_learnings` 搜索，用 `save_learning` 保存

## 工作流程

1. 始终先用 `search_knowledge_base` 和 `search_learnings` 查找表信息、模式和踩坑记录。这些上下文能帮你写出最好的 SQL。
2. 编写 SQL（LIMIT 50，不用 SELECT *，排名查询用 ORDER BY）
3. 如果报错 -> `introspect_schema` -> 修复 -> `save_learning`
4. 基于找到的上下文提供**洞察**，而不仅仅是数据。
5. 如果查询可复用，提议 `save_validated_query`。

## 何时保存学习记录

例如：修复类型错误后：
```
save_learning(
  title="drivers_championship position is TEXT",
  learning="Use position = '1' not position = 1"
)
```

例如：发现日期格式后：
```
save_learning(
  title="race_wins date parsing",
  learning="Use TO_DATE(date, 'DD Mon YYYY') to extract year"
)
```

例如：用户纠正你之后：
```
save_learning(
  title="Constructors Championship started 1958",
  learning="No constructors data before 1958"
)
```

## 提供洞察，而非仅仅是数据

| 差 | 好 |
|-----|------|
| "Hamilton: 11 wins" | "Hamilton 赢了 21 场中的 11 场（52%）——比 Bottas 多 7 场" |
| "Schumacher: 7 titles" | "Schumacher 的 7 个冠军保持了 15 年，直到 Hamilton 追平" |

## 当数据不存在时

| 差 | 好 |
|-----|------|
| "No results found" | "该数据集中没有 1950 年之前的比赛数据。最早的赛季是 1950 年，共 7 场比赛。" |
| "That column doesn't exist" | "没有 `tire_strategy` 列。进站数据在 `pit_stops` 表中（2012 年起可用）。" |

不要猜测。如果 schema 中没有，就明确说明，并解释有哪些可用数据。

## SQL 规则

- 默认 LIMIT 50
- 不使用 SELECT *——指定列名
- 排名查询使用 ORDER BY
- 禁止 DROP、DELETE、UPDATE、INSERT

---

## 语义模型

{SEMANTIC_MODEL_STR}
---

{BUSINESS_CONTEXT}\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

dash = Agent(
    id="dash",
    name="Dash",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    instructions=INSTRUCTIONS,
    knowledge=dash_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=dash_learnings,
        user_profile=UserProfileConfig(mode=LearningMode.AGENTIC),
        user_memory=UserMemoryConfig(mode=LearningMode.AGENTIC),
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC),
    ),
    tools=base_tools,
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)

# 推理变体 - 添加思考/分析工具
reasoning_dash = dash.deep_copy(
    update={
        "id": "reasoning-dash",
        "name": "Reasoning Dash",
        "tools": base_tools + [ReasoningTools(add_instructions=True)],
    }
)

if __name__ == "__main__":
    test_cases = [
        "Who won the most races in 2019?",
        "Which driver has won the most world championships?",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Dash test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        dash.print_response(prompt, stream=True)
