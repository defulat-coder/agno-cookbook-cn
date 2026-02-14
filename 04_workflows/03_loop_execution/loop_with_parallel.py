"""
带并行的循环
==================

演示在最终内容生成之前混合了 `Parallel` 和顺序步骤的循环体。
"""

import asyncio
from typing import List

from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow import Loop, Parallel, Step, Workflow
from agno.workflow.types import StepOutput

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
research_agent = Agent(
    name="Research Agent",
    role="研究专员",
    tools=[HackerNewsTools(), WebSearchTools()],
    instructions="你是一位研究专员。彻底研究给定的主题。",
    markdown=True,
)

analysis_agent = Agent(
    name="Analysis Agent",
    role="数据分析师",
    instructions="你是一位数据分析师。分析和总结研究发现。",
    markdown=True,
)

content_agent = Agent(
    name="Content Agent",
    role="内容创作者",
    instructions="你是一位内容创作者。基于研究创建引人入胜的内容。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_hackernews_step = Step(
    name="Research HackerNews",
    agent=research_agent,
    description="研究 HackerNews 上的热门主题",
)

research_web_step = Step(
    name="Research Web",
    agent=research_agent,
    description="从网络来源研究额外信息",
)

trend_analysis_step = Step(
    name="Trend Analysis",
    agent=analysis_agent,
    description="分析研究中的趋势模式",
)

sentiment_analysis_step = Step(
    name="Sentiment Analysis",
    agent=analysis_agent,
    description="分析研究中的情感和观点",
)

content_step = Step(
    name="Create Content",
    agent=content_agent,
    description="基于研究发现创建内容",
)


# ---------------------------------------------------------------------------
# 定义循环评估器
# ---------------------------------------------------------------------------
def research_evaluator(outputs: List[StepOutput]) -> bool:
    if not outputs:
        return False

    total_content_length = sum(len(output.content or "") for output in outputs)
    if total_content_length > 500:
        print(
            f"[通过] 研究评估通过 - 找到大量内容（总共 {total_content_length} 字符）"
        )
        return True

    print(
        f"[失败] 研究评估失败 - 需要更多实质性研究（当前：{total_content_length} 字符）"
    )
    return False


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Advanced Research and Content Workflow",
    description="在循环中使用并行执行研究主题，直到满足条件，然后创建内容",
    steps=[
        Loop(
            name="Research Loop with Parallel Execution",
            steps=[
                Parallel(
                    research_hackernews_step,
                    research_web_step,
                    trend_analysis_step,
                    name="Parallel Research & Analysis",
                    description="并行执行研究和分析以提高效率",
                ),
                sentiment_analysis_step,
            ],
            end_condition=research_evaluator,
            max_iterations=3,
        ),
        content_step,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    input_text = (
        "Research the latest trends in AI and machine learning, then create a summary"
    )

    # 同步运行
    workflow.print_response(
        input=input_text,
    )

    # 同步流式运行
    workflow.print_response(
        input=input_text,
        stream=True,
    )

    # 异步流式运行
    asyncio.run(
        workflow.aprint_response(
            input=input_text,
            stream=True,
        )
    )
