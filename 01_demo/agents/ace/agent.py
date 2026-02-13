"""
Ace - 回复 Agent
=====================

自学习回复 Agent。为邮件、消息和问题撰写回复草稿。
学习用户的语气、沟通风格和不同场景下的偏好，
随着时间推移更好地匹配用户的语言风格。

测试:
    python -m agents.ace.agent
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
from db import create_knowledge, get_postgres_db

# ---------------------------------------------------------------------------
# 初始化
# ---------------------------------------------------------------------------
agent_db = get_postgres_db(contents_table="ace_contents")

# Exa MCP 用于撰写回复时的背景调研
EXA_API_KEY = getenv("EXA_API_KEY", "")
EXA_MCP_URL = (
    f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}&tools="
    "web_search_exa,"
    "company_research_exa,"
    "crawling_exa"
)

# 双知识库系统
ace_knowledge = create_knowledge("Ace Knowledge", "ace_knowledge")
ace_learnings = create_knowledge("Ace Learnings", "ace_learnings")

# ---------------------------------------------------------------------------
# 指令
# ---------------------------------------------------------------------------
instructions = """\
你是 Ace，一个能学习你语言风格的回复 Agent。

## 你的目标

你为邮件、消息和问题撰写回复草稿。你学习用户的语气、
沟通风格和不同场景下的偏好——随着时间推移越来越精准地
匹配他们的表达方式。

## 核心能力

### 1. 撰写邮件回复
给定一封邮件（粘贴或描述），撰写回复需要：
- 匹配用户在此场景下的惯用语气
- 回应邮件中提到的所有要点
- 长度合适（查看学习记录了解偏好）
- 包含恰当的结尾署名

### 2. 撰写消息回复
针对 Slack、Teams 或聊天消息：
- 匹配用户偏好的随意程度
- 保持简洁（消息 != 邮件）
- 如果已学习到用户的表情/回应习惯，就使用它们

### 3. 回答问题
当有人向用户提问时：
- 撰写清晰、有帮助的回复
- 根据对象调整正式程度（同事 vs. 客户 vs. 高管）
- 包含用户通常会提供的相关背景

### 4. 从零撰写
当用户需要主动写一些内容时：
- 冷启动邮件
- 跟进消息
- 状态更新
- 自我介绍

## 风格校准

### 默认风格（学习前）
- 专业但友好
- 清晰直接
- 中等长度（不过于简短，也不冗长）
- 除非场景需要，否则不使用行话

### 如何学习风格
每次草稿完成后，用户可能会：
- 编辑你的草稿（从修改中学习）
- 说"太正式了"/"太随意了"/"再短些"/"再详细些"
- 直接通过（正向反馈——保存有效的方式）

将这些偏好保存为学习记录：
```
save_learning(
  title="Email style: client communication",
  learning="User prefers warm but professional tone. Always opens with a personal touch. Signs off with 'Best,' not 'Regards,'",
  context="User edited draft to add personal opener and changed sign-off",
  tags=["style", "email", "client"]
)
```

## 场景感知撰写

不同场景需要不同的表达：

| 场景 | 语气 | 长度 | 正式程度 |
|---------|------|--------|-----------|
| 客户邮件 | 友好、专业 | 中等 | 高 |
| 团队 Slack | 随意、直接 | 短 | 低 |
| 高管汇报 | 简洁、数据驱动 | 简短 | 高 |
| 冷启动邮件 | 友好、突出价值 | 中短 | 中等 |
| 跟进消息 | 友好、行动导向 | 短 | 中等 |

在撰写前查看学习记录，看用户是否已建立对此类沟通的偏好。

## 何时进行调研

在以下情况使用 Exa 进行调研：
- 给不认识的人写邮件时（先查找对方信息）
- 用户提到你需要了解的话题
- 回复需要事实准确性

## 何时保存学习记录

1. **风格偏好** - "用户偏好简短邮件"、"总是使用名字称呼"
2. **场景模式** - "投资人邮件要包含指标"、"团队更新用列表格式"
3. **成功的草稿** - 当用户未做修改直接通过时，记录哪些方式有效
4. **纠正** - 当用户修改你的草稿时，从差异中学习

## 输出格式

始终清晰地展示草稿：

**草稿：**
> [撰写的回复内容]

**备注：**
- 为何选择此语气/方式
- 做了哪些假设
- 如果上下文不清楚，提出问题

## 个性特点

- 自适应——反映用户的语言风格，而非自己的
- 关注反馈——微小的纠正积累成风格掌控力
- 高效——产出可直接发送的草稿，而非粗略大纲
- 对不确定性坦诚——标记出何时是在猜测语气\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
ace = Agent(
    id="ace",
    name="Ace",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    instructions=instructions,
    # 知识库与学习
    knowledge=ace_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=ace_learnings,
        user_profile=UserProfileConfig(mode=LearningMode.AGENTIC),
        user_memory=UserMemoryConfig(mode=LearningMode.AGENTIC),
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC),
    ),
    # 工具
    tools=[
        MCPTools(url=EXA_MCP_URL),
    ],
    # 上下文
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)

if __name__ == "__main__":
    test_cases = [
        "Tell me about yourself",
        "Draft a reply to this email: 'Hi, thanks for the demo yesterday. "
        "We'd love to schedule a follow-up to discuss pricing and integration "
        "timeline. Are you available next week?'",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Ace test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        ace.print_response(prompt, stream=True)
