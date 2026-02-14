"""
基本条件
===============

演示在线性工作流中使用事实检查门进行条件步骤执行。
"""

import asyncio

from agno.agent.agent import Agent
from agno.tools.websearch import WebSearchTools
from agno.workflow.condition import Condition
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Researcher",
    instructions="研究给定主题并提供详细发现。",
    tools=[WebSearchTools()],
)

summarizer = Agent(
    name="Summarizer",
    instructions="为研究发现创建清晰的摘要。",
)

fact_checker = Agent(
    name="Fact Checker",
    instructions="验证事实并检查研究的准确性。",
    tools=[WebSearchTools()],
)

writer = Agent(
    name="Writer",
    instructions="根据所有可用的研究和验证撰写一篇全面的文章。",
)


# ---------------------------------------------------------------------------
# 定义条件评估器
# ---------------------------------------------------------------------------
def needs_fact_checking(step_input: StepInput) -> bool:
    summary = step_input.previous_step_content or ""
    fact_indicators = [
        "study shows",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]
    return any(indicator in summary.lower() for indicator in fact_indicators)


# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
research_step = Step(
    name="research",
    description="研究主题",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="总结研究发现",
    agent=summarizer,
)

fact_check_step = Step(
    name="fact_check",
    description="验证事实和声明",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="撰写最终文章",
    agent=writer,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
basic_workflow = Workflow(
    name="Basic Linear Workflow",
    description="研究 -> 总结 -> 条件（事实检查）-> 撰写文章",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="检查是否需要事实检查",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("运行基本线性工作流示例")
    print("=" * 50)

    try:
        # 同步流式运行
        basic_workflow.print_response(
            input="Recent breakthroughs in quantum computing",
            stream=True,
        )

        # 异步流式运行
        asyncio.run(
            basic_workflow.aprint_response(
                input="Recent breakthroughs in quantum computing",
                stream=True,
            )
        )
    except Exception as e:
        print(f"[错误] {e}")
        import traceback

        traceback.print_exc()
