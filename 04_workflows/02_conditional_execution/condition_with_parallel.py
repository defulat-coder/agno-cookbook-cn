"""
带并行的条件
=======================

演示在最终综合步骤之前并行执行的多个条件分支。
"""

import asyncio

from agno.agent import Agent
from agno.tools.exa import ExaTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.condition import Condition
from agno.workflow.parallel import Parallel
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="HackerNews Researcher",
    instructions="从 Hacker News 研究技术新闻和趋势",
    tools=[HackerNewsTools()],
)

web_agent = Agent(
    name="Web Researcher",
    instructions="从网络研究一般信息",
    tools=[WebSearchTools()],
)

exa_agent = Agent(
    name="Exa Search Researcher",
    instructions="使用 Exa 高级搜索功能进行研究",
    tools=[ExaTools()],
)

content_agent = Agent(
    name="Content Creator",
    instructions="从研究数据创建结构良好的内容",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_hackernews_step = Step(
    name="ResearchHackerNews",
    description="从 Hacker News 研究技术新闻",
    agent=hackernews_agent,
)

research_web_step = Step(
    name="ResearchWeb",
    description="从网络研究一般信息",
    agent=web_agent,
)

research_exa_step = Step(
    name="ResearchExa",
    description="使用 Exa 搜索进行研究",
    agent=exa_agent,
)

prepare_input_for_write_step = Step(
    name="PrepareInput",
    description="准备和组织用于写作的研究数据",
    agent=content_agent,
)

write_step = Step(
    name="WriteContent",
    description="根据研究撰写最终内容",
    agent=content_agent,
)


# ---------------------------------------------------------------------------
# 定义条件评估器
# ---------------------------------------------------------------------------
def check_if_we_should_search_hn(step_input: StepInput) -> bool:
    topic = step_input.input or step_input.previous_step_content or ""
    tech_keywords = [
        "ai",
        "machine learning",
        "programming",
        "software",
        "tech",
        "startup",
        "coding",
    ]
    return any(keyword in topic.lower() for keyword in tech_keywords)


def check_if_we_should_search_web(step_input: StepInput) -> bool:
    topic = step_input.input or step_input.previous_step_content or ""
    general_keywords = ["news", "information", "research", "facts", "data"]
    return any(keyword in topic.lower() for keyword in general_keywords)


def check_if_we_should_search_x(step_input: StepInput) -> bool:
    topic = step_input.input or step_input.previous_step_content or ""
    social_keywords = [
        "trending",
        "viral",
        "social",
        "discussion",
        "opinion",
        "twitter",
        "x",
    ]
    return any(keyword in topic.lower() for keyword in social_keywords)


def check_if_we_should_search_exa(step_input: StepInput) -> bool:
    topic = step_input.input or step_input.previous_step_content or ""
    advanced_keywords = ["deep", "academic", "research", "analysis", "comprehensive"]
    return any(keyword in topic.lower() for keyword in advanced_keywords)


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Conditional Workflow",
    steps=[
        Parallel(
            Condition(
                name="HackerNewsCondition",
                description="检查我们是否应该搜索 Hacker News 获取技术主题",
                evaluator=check_if_we_should_search_hn,
                steps=[research_hackernews_step],
            ),
            Condition(
                name="WebSearchCondition",
                description="检查我们是否应该搜索网络获取一般信息",
                evaluator=check_if_we_should_search_web,
                steps=[research_web_step],
            ),
            Condition(
                name="ExaSearchCondition",
                description="检查我们是否应该使用 Exa 进行高级搜索",
                evaluator=check_if_we_should_search_exa,
                steps=[research_exa_step],
            ),
            name="ConditionalResearch",
            description="并行运行条件研究步骤",
        ),
        prepare_input_for_write_step,
        write_step,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # 同步运行
        workflow.print_response(input="Latest AI developments in machine learning")

        # 同步流式运行
        workflow.print_response(
            input="Latest AI developments in machine learning",
            stream=True,
        )

        # 异步运行
        asyncio.run(
            workflow.aprint_response(input="Latest AI developments in machine learning")
        )

        # 异步流式运行
        asyncio.run(
            workflow.aprint_response(
                input="Latest AI developments in machine learning",
                stream=True,
            )
        )
    except Exception as e:
        print(f"[错误] {e}")
    print()
