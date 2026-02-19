"""
推理流式输出
================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.run.agent import RunEvent  # noqa


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    # 创建启用推理的 Agent
    agent = Agent(
        reasoning_model=OpenAIResponses(
            id="o3-mini",
            reasoning_effort="low",
        ),
        reasoning=True,
        instructions="请逐步思考问题。",
    )

    prompt = "分析导致 1919 年《凡尔赛条约》签订的关键因素，探讨该条约对德国的政治、经济和社会影响，以及它如何促成了第二次世界大战的爆发。请提供包含多元历史视角的深入评估。"

    agent.print_response(prompt, stream=True, stream_events=True)

    # 使用手动事件循环查看所有事件
    # for run_output_event in agent.run(
    #     prompt,
    #     stream=True,
    #     stream_events=True,
    # ):
    #     if run_output_event.event == RunEvent.run_started:
    #         print(f"\n事件: {run_output_event.event}")

    #     elif run_output_event.event == RunEvent.reasoning_started:
    #         print(f"\n事件: {run_output_event.event}")
    #         print("推理开始...\n")

    #     elif run_output_event.event == RunEvent.reasoning_content_delta:
    #         # 这是推理内容的新流式事件
    #         print(run_output_event.reasoning_content, end="", flush=True)

    #     elif run_output_event.event == RunEvent.reasoning_step:
    #         print(f"\n事件: {run_output_event.event}")

    #     elif run_output_event.event == RunEvent.reasoning_completed:
    #         print(f"\n\n事件: {run_output_event.event}")

    #     elif run_output_event.event == RunEvent.run_content:
    #         if run_output_event.content:
    #             print(run_output_event.content, end="", flush=True)

    #     elif run_output_event.event == RunEvent.run_completed:
    #         print(f"\n\n事件: {run_output_event.event}")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
