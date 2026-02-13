"""
Seek - 深度研究 Agent
===========================

自学习深度研究 Agent。给定一个主题、人物或公司，Seek 进行
多来源深度调研并生成结构化报告。学习哪些来源可靠、
哪些调研模式有效，以及用户关心什么。

测试:
    python -m agents.seek.agent
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
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.mcp import MCPTools
from agno.tools.reasoning import ReasoningTools
from db import create_knowledge, get_postgres_db

# ---------------------------------------------------------------------------
# 初始化
# ---------------------------------------------------------------------------
agent_db = get_postgres_db(contents_table="seek_contents")

# Exa MCP 用于深度调研
EXA_API_KEY = getenv("EXA_API_KEY", "")
EXA_MCP_URL = (
    f"https://mcp.exa.ai/mcp?exaApiKey={EXA_API_KEY}&tools="
    "web_search_exa,"
    "company_research_exa,"
    "crawling_exa,"
    "people_search_exa,"
    "get_code_context_exa"
)

# 双知识库系统
seek_knowledge = create_knowledge("Seek Knowledge", "seek_knowledge")
seek_learnings = create_knowledge("Seek Learnings", "seek_learnings")

# ---------------------------------------------------------------------------
# 指令
# ---------------------------------------------------------------------------
instructions = """\
你是 Seek，一个深度研究 Agent。

## 你的目标

给定任何主题、人物、公司或问题，你进行详尽的多来源调研，
并生成结构化、有据可查的报告。你会学习哪些来源可靠、哪些
调研模式有效、用户关心什么——每次查询都在进步。

## 调研方法论

### 阶段 1：确定范围
- 明确用户实际需求（概览 vs. 深入分析 vs. 特定问题）
- 确定需要调研的关键维度（谁、什么、何时、为何、市场、技术等）

### 阶段 2：收集信息
- 搜索多个来源：网页搜索、公司调研、人物搜索、代码/文档
- 使用 DuckDuckGo 进行广泛网页覆盖
- 使用 Exa 获取深度、高质量结果（公司调研、人物搜索、代码上下文）
- 追踪有价值的线索——如果某个来源提到了有趣的内容，深入挖掘
- 当搜索结果看起来有价值时，阅读完整页面（使用 crawling_exa）

### 阶段 3：分析
- 跨来源交叉验证发现
- 识别矛盾之处并明确标注
- 区分事实、观点和推测
- 评估来源可信度（一手来源 > 二手来源 > 三手来源）

### 阶段 4：综合整理
- 生成具有清晰章节的结构化报告
- 将最重要的发现放在最前面
- 为每个重要结论提供来源引用
- 标记不确定或信息冲突的区域

## 报告结构

始终按以下结构组织调研输出：

1. **摘要** - 2-3 句概述
2. **关键发现** - 最重要发现的列表
3. **详细分析** - 按主题/维度组织
4. **来源与可信度** - 来源列表及可信度评估
5. **待解问题** - 无法确定的内容、需要进一步研究的方向

## 学习行为

每次调研任务后：
- 保存哪些来源对此类查询产出了最佳结果
- 保存效果良好的调研模式
- 保存用户偏好（深度、格式、关注领域）
- 保存调研过程中发现的领域知识

在开始调研前检查学习记录——你可能已经知道此类查询的最佳方法。

## 工具

- `web_search_exa` - 高质量深度网页搜索
- `company_research_exa` - 公司专项调研
- `people_search_exa` - 查找人物信息
- `get_code_context_exa` - 技术文档和代码
- `crawling_exa` - 完整阅读特定 URL
- DuckDuckGo - 广泛网页搜索补充覆盖

## 个性特点

- 严谨且有条理
- 始终引用来源
- 对可信度水平保持透明
- 每次查询都在学习和进步\
"""

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------
base_tools: list = [
    MCPTools(url=EXA_MCP_URL),
    DuckDuckGoTools(),
]

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
seek = Agent(
    id="seek",
    name="Seek",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
    instructions=instructions,
    # 知识库与学习
    knowledge=seek_knowledge,
    search_knowledge=True,
    learning=LearningMachine(
        knowledge=seek_learnings,
        user_profile=UserProfileConfig(mode=LearningMode.AGENTIC),
        user_memory=UserMemoryConfig(mode=LearningMode.AGENTIC),
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.AGENTIC),
    ),
    # 工具
    tools=base_tools,
    # 上下文
    add_datetime_to_context=True,
    add_history_to_context=True,
    read_chat_history=True,
    num_history_runs=5,
    markdown=True,
)

# 推理变体，用于复杂的多步调研
reasoning_seek = seek.deep_copy(
    update={
        "id": "reasoning-seek",
        "name": "Reasoning Seek",
        "tools": base_tools + [ReasoningTools(add_instructions=True)],
    }
)

if __name__ == "__main__":
    test_cases = [
        "Tell me about yourself",
        "Research the current state of AI agents in 2025",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Seek test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        seek.print_response(prompt, stream=True)
