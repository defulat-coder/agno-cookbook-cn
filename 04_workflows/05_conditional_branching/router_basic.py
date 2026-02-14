"""
基本路由器
============

演示在内容发布之前在专业研究步骤之间进行基于主题的路由。
"""

import asyncio
from typing import List

from agno.agent.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="HackerNews Researcher",
    instructions="你是一位专门从 Hacker News 寻找最新技术新闻和讨论的研究员。专注于创业趋势、编程主题和技术行业见解。",
    tools=[HackerNewsTools()],
)

web_agent = Agent(
    name="Web Researcher",
    instructions="你是一位全面的网络研究员。搜索包括新闻网站、博客和官方文档在内的多个来源，以收集详细信息。",
    tools=[WebSearchTools()],
)

content_agent = Agent(
    name="Content Publisher",
    instructions="你是一位内容创作者，将研究数据转化为引人入胜、结构良好的文章。使用适当的标题、要点和清晰的结论来格式化内容。",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_hackernews = Step(
    name="research_hackernews",
    agent=hackernews_agent,
    description="从 Hacker News 研究最新技术趋势",
)

research_web = Step(
    name="research_web",
    agent=web_agent,
    description="对主题进行全面的网络研究",
)

publish_content = Step(
    name="publish_content",
    agent=content_agent,
    description="创建并格式化最终内容以供发布",
)


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def research_router(step_input: StepInput) -> List[Step]:
    topic = step_input.previous_step_content or step_input.input or ""
    topic = topic.lower()

    tech_keywords = [
        "startup",
        "programming",
        "ai",
        "machine learning",
        "software",
        "developer",
        "coding",
        "tech",
        "silicon valley",
        "venture capital",
        "cryptocurrency",
        "blockchain",
        "open source",
        "github",
    ]

    if any(keyword in topic for keyword in tech_keywords):
        print(f"检测到技术主题：对 '{topic}' 使用 HackerNews 研究")
        return [research_hackernews]

    print(f"检测到常规主题：对 '{topic}' 使用网络研究")
    return [research_web]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Intelligent Research Workflow",
    description="根据主题自动选择最佳研究方法，然后发布内容",
    steps=[
        Router(
            name="research_strategy_router",
            selector=research_router,
            choices=[research_hackernews, research_web],
            description="根据主题智能选择研究方法",
        ),
        publish_content,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = "Latest developments in artificial intelligence and machine learning"

    # 同步运行
    workflow.print_response(input_text)

    # 同步流式运行
    workflow.print_response(
        input_text,
        stream=True,
    )

    # 异步运行
    asyncio.run(
        workflow.aprint_response(
            input_text,
        )
    )

    # 异步流式运行
    asyncio.run(
        workflow.aprint_response(
            input_text,
            stream=True,
        )
    )
