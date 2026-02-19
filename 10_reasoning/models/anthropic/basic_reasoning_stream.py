"""
基础推理流式输出
======================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.run.agent import RunEvent  # noqa


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    # 创建启用推理的 Agent
    agent = Agent(
        reasoning_model=Claude(
            id="claude-sonnet-4-5",
            thinking={"type": "enabled", "budget_tokens": 1024},
        ),
        reasoning=True,
        instructions="请逐步思考问题。",
    )

    prompt = "25 * 37 等于多少？请展示你的推理过程。"

    agent.print_response(prompt, stream=True, stream_events=True)

    # # 或者可以使用以下方式捕获事件
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
    #         # 这是推理内容的新流式事件，实时流式传输生成的原始内容
    #         print(run_output_event.reasoning_content, end="", flush=True)

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
