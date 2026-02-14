"""
选择中的循环
===============

演示将 `Loop` 组件用作路由器选择之一。
"""

from typing import List, Union

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.loop import Loop
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput, StepOutput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
draft_writer = Agent(
    name="draft_writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="撰写关于给定主题的草稿。保持简洁。",
)

refiner = Agent(
    name="refiner",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="改进和完善给定的草稿。使其更加精炼。",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
quick_response = Step(
    name="quick_response",
    executor=lambda x: StepOutput(content=f"Quick answer: {x.input}"),
)

refinement_loop = Loop(
    name="refinement_loop",
    steps=[Step(name="refine_step", agent=refiner)],
    max_iterations=2,
)


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def loop_selector(
    step_input: StepInput,
    step_choices: list,
) -> Union[str, Step, List[Step]]:
    user_input = step_input.input.lower()

    if "quick" in user_input:
        return step_choices[0]
    if "refine" in user_input or "polish" in user_input:
        return [step_choices[1], step_choices[2]]
    return step_choices[1]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Loop Choice Routing",
    steps=[
        Router(
            name="Content Router",
            selector=loop_selector,
            choices=[quick_response, draft_writer, refinement_loop],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    workflow.print_response(
        "Please refine and polish a blog post about Python",
        stream=True,
    )
