"""
选择器类型
==============

演示路由器选择器在字符串、步骤对象、列表和嵌套选择返回模式中的灵活性。
"""

from typing import List, Union

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 为字符串选择器创建 Agent
# ---------------------------------------------------------------------------
tech_expert = Agent(
    name="tech_expert",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位技术专家。提供技术分析。",
)

biz_expert = Agent(
    name="biz_expert",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位商业专家。提供商业见解。",
)

generalist = Agent(
    name="generalist",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位通才。提供一般信息。",
)

tech_step = Step(name="Tech Research", agent=tech_expert)
business_step = Step(name="Business Research", agent=biz_expert)
general_step = Step(name="General Research", agent=generalist)


# ---------------------------------------------------------------------------
# 定义选择器
# ---------------------------------------------------------------------------
def route_by_topic(step_input: StepInput) -> Union[str, Step, List[Step]]:
    topic = step_input.input.lower()

    if "tech" in topic or "ai" in topic or "software" in topic:
        return "Tech Research"
    if "business" in topic or "market" in topic or "finance" in topic:
        return "Business Research"
    return "General Research"


# ---------------------------------------------------------------------------
# 创建工作流（字符串选择器）
# ---------------------------------------------------------------------------
workflow_string_selector = Workflow(
    name="Expert Routing (String Selector)",
    steps=[
        Router(
            name="Topic Router",
            selector=route_by_topic,
            choices=[tech_step, business_step, general_step],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 为 step_choices 选择器创建 Agent
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
# 创建工作流（step_choices）
# ---------------------------------------------------------------------------
workflow_step_choices = Workflow(
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
# 为嵌套选择选择器创建 Agent
# ---------------------------------------------------------------------------
step_a = Agent(name="step_a", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step A")
step_b = Agent(name="step_b", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step B")
step_c = Agent(name="step_c", model=OpenAIChat(id="gpt-4o-mini"), instructions="Step C")


def nested_selector(
    step_input: StepInput,
    step_choices: list,
) -> Union[str, Step, List[Step]]:
    user_input = step_input.input.lower()

    if "single" in user_input:
        return step_choices[0]
    return step_choices[1]


# ---------------------------------------------------------------------------
# 创建工作流（嵌套选择）
# ---------------------------------------------------------------------------
workflow_nested = Workflow(
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
    print("=" * 60)
    print("示例 1：基于字符串的选择器（返回步骤名称）")
    print("=" * 60)
    workflow_string_selector.print_response("Tell me about AI trends", stream=True)

    print("\n" + "=" * 60)
    print("示例 2：step_choices 参数")
    print("=" * 60)
    workflow_step_choices.print_response("I need to research something", stream=True)

    print("\n" + "=" * 60)
    print("示例 3：嵌套选择")
    print("=" * 60)
    workflow_nested.print_response("Run the sequence", stream=True)
