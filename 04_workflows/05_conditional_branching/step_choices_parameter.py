"""
步骤选择参数
======================

演示在路由器选择器中使用 `step_choices` 进行动态步骤选择。
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
researcher = Agent(
    name="researcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位研究员。",
)

writer = Agent(
    name="writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位作家。",
)

reviewer = Agent(
    name="reviewer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位审稿人。",
)


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def dynamic_selector(
    step_input: StepInput,
    step_choices: list,
) -> Union[str, Step, List[Step]]:
    user_input = step_input.input.lower()
    step_map = {s.name: s for s in step_choices if hasattr(s, "name") and s.name}

    print(f"可用步骤：{list(step_map.keys())}")

    if "research" in user_input:
        return "researcher"
    if "write" in user_input:
        return step_map.get("writer", step_choices[0])
    if "full" in user_input:
        return [step_map["researcher"], step_map["writer"], step_map["reviewer"]]
    return step_choices[0]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Dynamic Routing (step_choices)",
    steps=[
        Router(
            name="Dynamic Router",
            selector=dynamic_selector,
            choices=[researcher, writer, reviewer],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    workflow.print_response("I need to research something", stream=True)
