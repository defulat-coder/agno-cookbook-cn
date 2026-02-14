"""
嵌套选择
==============

演示路由器选择中的嵌套列表，这些列表将转换为顺序 `Steps` 容器。
"""

from typing import List, Union

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
step_a = Agent(name="step_a", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step A")
step_b = Agent(name="step_b", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step B")
step_c = Agent(name="step_c", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step C")


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def nested_selector(
    step_input: StepInput,
    step_choices: list,
) -> Union[str, Step, List[Step]]:
    user_input = step_input.input.lower()

    if "single" in user_input:
        return step_choices[0]
    return step_choices[1]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Nested Choices Routing",
    steps=[
        Router(
            name="Nested Router",
            selector=nested_selector,
            choices=[step_a, [step_b, step_c]],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    workflow.print_response("Run the sequence", stream=True)
