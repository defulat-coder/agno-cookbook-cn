"""
推理 Agent 事件
=============================

推理 Agent 事件示例。
"""

import asyncio

from agno.agent import RunEvent
from agno.agent.agent import Agent
from agno.models.openai.chat import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
finance_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
)


async def run_agent_with_events(prompt: str):
    content_started = False
    async for run_output_event in finance_agent.arun(
        prompt,
        stream=True,
        stream_events=True,
    ):
        if run_output_event.event in [RunEvent.run_started, RunEvent.run_completed]:
            print(f"\nEVENT: {run_output_event.event}")

        if run_output_event.event in [RunEvent.reasoning_started]:
            print(f"\nEVENT: {run_output_event.event}")

        if run_output_event.event in [RunEvent.reasoning_step]:
            print(f"\nEVENT: {run_output_event.event}")
            print(f"REASONING CONTENT: {run_output_event.reasoning_content}")  # type: ignore

        if run_output_event.event in [RunEvent.reasoning_completed]:
            print(f"\nEVENT: {run_output_event.event}")

        if run_output_event.event in [RunEvent.run_content]:
            if not content_started:
                print("\nCONTENT:")
                content_started = True
            else:
                print(run_output_event.content, end="")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    task = (
        "分析 1919 年《凡尔赛条约》签署的关键因素。"
        "讨论该条约对德国的政治、经济和社会影响，以及它如何"
        "促成了第二次世界大战的爆发。提供一个细致的评估，包括"
        "多种历史视角。"
    )
    asyncio.run(
        run_agent_with_events(
            task,
        )
    )
