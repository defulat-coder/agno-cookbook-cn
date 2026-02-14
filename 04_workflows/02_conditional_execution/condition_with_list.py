"""
带列表的条件
===================

演示执行多个步骤列表的条件分支，包括并行条件块。
"""

import asyncio

from agno.agent.agent import Agent
from agno.tools.exa import ExaTools
from agno.tools.hackernews import HackerNewsTools
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

exa_agent = Agent(
    name="Exa Search Researcher",
    instructions="使用 Exa 高级搜索功能进行研究",
    tools=[ExaTools()],
)

content_agent = Agent(
    name="Content Creator",
    instructions="从研究数据创建结构良好的内容",
)

trend_analyzer_agent = Agent(
    name="Trend Analyzer",
    instructions="从研究数据中分析趋势和模式",
)

fact_checker_agent = Agent(
    name="Fact Checker",
    instructions="验证事实并交叉参考信息",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_hackernews_step = Step(
    name="ResearchHackerNews",
    description="从 Hacker News 研究技术新闻",
    agent=hackernews_agent,
)

research_exa_step = Step(
    name="ResearchExa",
    description="使用 Exa 搜索进行研究",
    agent=exa_agent,
)

deep_exa_analysis_step = Step(
    name="DeepExaAnalysis",
    description="使用 Exa 搜索功能进行深入分析",
    agent=exa_agent,
)

trend_analysis_step = Step(
    name="TrendAnalysis",
    description="从研究数据中分析趋势和模式",
    agent=trend_analyzer_agent,
)

fact_verification_step = Step(
    name="FactVerification",
    description="验证事实并交叉参考信息",
    agent=fact_checker_agent,
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


def check_if_comprehensive_research_needed(step_input: StepInput) -> bool:
    topic = step_input.input or step_input.previous_step_content or ""
    comprehensive_keywords = [
        "comprehensive",
        "detailed",
        "thorough",
        "in-depth",
        "complete analysis",
        "full report",
        "extensive research",
    ]
    return any(keyword in topic.lower() for keyword in comprehensive_keywords)


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Conditional Workflow with Multi-Step Condition",
    steps=[
        Parallel(
            Condition(
                name="HackerNewsCondition",
                description="检查我们是否应该搜索 Hacker News 获取技术主题",
                evaluator=check_if_we_should_search_hn,
                steps=[research_hackernews_step],
            ),
            Condition(
                name="ComprehensiveResearchCondition",
                description="检查是否需要全面的多步骤研究",
                evaluator=check_if_comprehensive_research_needed,
                steps=[
                    deep_exa_analysis_step,
                    trend_analysis_step,
                    fact_verification_step,
                ],
            ),
            name="ConditionalResearch",
            description="并行运行条件研究步骤",
        ),
        write_step,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # 同步流式运行
        workflow.print_response(
            input="Comprehensive analysis of climate change research",
            stream=True,
        )

        # 异步运行
        asyncio.run(
            workflow.aprint_response(
                input="Comprehensive analysis of climate change research",
            )
        )
    except Exception as e:
        print(f"[错误] {e}")
    print()
