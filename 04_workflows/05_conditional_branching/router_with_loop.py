"""
带循环的路由器
================

演示在简单网络研究和基于迭代循环的深度技术研究之间进行基于路由器的选择。
"""

import asyncio
from typing import List

from agno.agent.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.loop import Loop
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput, StepOutput
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
# 定义循环评估器
# ---------------------------------------------------------------------------
def research_quality_check(outputs: List[StepOutput]) -> bool:
    if not outputs:
        return False

    for output in outputs:
        if output.content and len(output.content) > 300:
            print(
                f"[通过] 研究质量检查通过 - 找到大量内容（{len(output.content)} 字符）"
            )
            return True

    print("[失败] 研究质量检查失败 - 需要更多实质性研究")
    return False


# ---------------------------------------------------------------------------
# 定义循环和路由器
# ---------------------------------------------------------------------------
deep_tech_research_loop = Loop(
    name="Deep Tech Research Loop",
    steps=[research_hackernews],
    end_condition=research_quality_check,
    max_iterations=3,
    description="对技术主题执行迭代深度研究",
)


def research_strategy_router(step_input: StepInput) -> List[Step]:
    topic = step_input.previous_step_content or step_input.input or ""
    topic = topic.lower()

    deep_tech_keywords = [
        "startup trends",
        "ai developments",
        "machine learning research",
        "programming languages",
        "developer tools",
        "silicon valley",
        "venture capital",
        "cryptocurrency analysis",
        "blockchain technology",
        "open source projects",
        "github trends",
        "tech industry",
        "software engineering",
    ]

    if any(keyword in topic for keyword in deep_tech_keywords) or (
        "tech" in topic and len(topic.split()) > 3
    ):
        print(f"检测到深度技术主题：对 '{topic}' 使用迭代研究循环")
        return [deep_tech_research_loop]

    print(f"检测到简单主题：对 '{topic}' 使用基本网络研究")
    return [research_web]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Adaptive Research Workflow",
    description="根据主题复杂度智能选择简单网络研究或深度迭代技术研究",
    steps=[
        Router(
            name="research_strategy_router",
            selector=research_strategy_router,
            choices=[research_web, deep_tech_research_loop],
            description="在简单网络研究或深度技术研究循环之间进行选择",
        ),
        publish_content,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 使用深度技术主题测试 ===")
    workflow.print_response(
        "Latest developments in artificial intelligence and machine learning and deep tech research trends"
    )

    asyncio.run(
        workflow.aprint_response(
            "Latest developments in artificial intelligence and machine learning and deep tech research trends"
        )
    )
