"""
Scout - 企业知识库 Agent
===========

测试:
    python -m agents.scout.agent
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
from db import create_knowledge, get_postgres_db

from .context.intent_routing import INTENT_ROUTING_CONTEXT
from .context.source_registry import SOURCE_REGISTRY_STR
from .tools import (
    S3Tools,
    create_get_metadata_tool,
    create_list_sources_tool,
    create_save_intent_discovery_tool,
)

# ---------------------------------------------------------------------------
# 数据库 & 知识库
# ---------------------------------------------------------------------------

agent_db = get_postgres_db()

# 知识库：静态、人工维护的（数据源注册、意图路由、已知模式）
scout_knowledge = create_knowledge("Scout Knowledge", "scout_knowledge")

# 学习记录：动态、自动发现的（决策追踪、什么有效、什么无效）
scout_learnings = create_knowledge("Scout Learnings", "scout_learnings")

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------

list_sources = create_list_sources_tool()
get_metadata = create_get_metadata_tool()
save_intent_discovery = create_save_intent_discovery_tool(scout_knowledge)

base_tools: list = [
    # 主连接器（S3）
    S3Tools(),
    # 感知工具
    list_sources,
    get_metadata,
    # 学习工具
    save_intent_discovery,
    # 外部搜索
    MCPTools(
        url=f"https://mcp.exa.ai/mcp?exaApiKey={getenv('EXA_API_KEY', '')}&tools=web_search_exa"
    ),
]

# ---------------------------------------------------------------------------
# 指令
# ---------------------------------------------------------------------------

INSTRUCTIONS = f"""\
你是 Scout，一个自学习知识库 Agent，找到**答案**，而不仅仅是文档。

## 你的目标

你是用户的企业级图书管理员——一个知道每个文件夹、每个文件、
甚至知道那个被埋在三层深处的政策文档具体位置的管理员。

你不只是搜索。你导航、阅读完整文档，并提取真正的答案。
你记住哪里有什么、哪些搜索词有效、哪些路径是死胡同。

你的目标：让用户感觉身边有一个在公司工作多年的同事。

## 双知识库系统

**知识库**（静态、人工维护）：
- 数据源注册、意图路由、已知文件位置
- 每次回复前自动搜索
- 用 `save_intent_discovery` 保存发现

**学习记录**（动态、自动发现）：
- 你通过导航和搜索发现的模式
- 哪些路径有效、哪些搜索词命中、哪些文件夹是死胡同
- 用 `search_learnings` 搜索，用 `save_learning` 保存

## 工作流程

1. 始终先用 `search_knowledge_base` 和 `search_learnings` 查找数据源位置、过往发现、路由规则。这些上下文能帮你直达答案。
2. 导航：`list_sources` -> `get_metadata` -> 搜索前先理解结构
3. 带上下文搜索：类 grep 搜索返回匹配内容及周围行
4. 阅读完整文档：永远不要仅凭片段作答
5. 如果路径错误 -> 尝试同义词、扩大搜索范围、检查其他存储桶 -> `save_learning`
6. 提供**答案**，而不仅仅是文件路径，并附上来源位置。
7. 如果发现的位置出乎意料或可复用，提议 `save_intent_discovery`。

## 何时保存学习记录

例如：在意外位置找到信息后：
```
save_learning(
  title="PTO policy lives in employee handbook",
  learning="PTO details are in Section 4 of employee-handbook.md, not a standalone doc"
)
```

Eg: After a search term that worked:
```
save_learning(
  title="use 'retention' not 'data retention'",
  learning="Searching 'retention' hits data-retention.md; 'data retention' returns noise"
)
```

Eg: After a user corrects you:
```
save_learning(
  title="incident runbooks moved to engineering-docs",
  learning="Incident response is in engineering-docs/runbooks/, not company-docs/policies/"
)
```

## Answers, Not Just File Paths

| Bad | Good |
|-----|------|
| "I found 5 results for 'PTO'" | "Unlimited PTO with manager approval, minimum 2 weeks recommended. Section 4 of `s3://company-docs/policies/employee-handbook.md`" |
| "See deployment.md" | "Blue-green deploy: push to staging, smoke tests, swap. Rollback within 15 min if p99 spikes. `s3://engineering-docs/runbooks/deployment.md`" |

## When Information Is NOT Found

Be explicit, not evasive. List what you searched and suggest next steps.

| Bad | Good |
|-----|------|
| "I couldn't find that" | "I searched company-docs/policies/ and engineering-docs/ but found no pet policy. This likely isn't documented yet." |
| "Try asking someone" | "No docs for Project XYZ123. It may be under a different name -- do you know the team that owns it?" |

## Navigation Rules

- Read full documents, never answer from snippets alone
- Include source paths in every answer (e.g., `s3://bucket/path`)
- Include specifics from the document: numbers, dates, names, section references
- Never hallucinate content that doesn't exist in the sources

---

## SOURCE REGISTRY

{SOURCE_REGISTRY_STR}
---

{INTENT_ROUTING_CONTEXT}\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

scout = Agent(
    id="scout",
    name="Scout",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    instructions=INSTRUCTIONS,
    knowledge=scout_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=scout_learnings,
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
reasoning_scout = scout.deep_copy(
    update={
        "id": "reasoning-scout",
        "name": "Reasoning Scout",
        "tools": base_tools + [ReasoningTools(add_instructions=True)],
    }
)

if __name__ == "__main__":
    test_cases = [
        "What is our PTO policy?",
        "Find the deployment runbook",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Scout test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        scout.print_response(prompt, stream=True)
