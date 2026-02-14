"""
字符串选择器
===============

演示从路由器选择器返回步骤名称字符串。
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

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
tech_step = Step(name="Tech Research", agent=tech_expert)
business_step = Step(name="Business Research", agent=biz_expert)
general_step = Step(name="General Research", agent=generalist)


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def route_by_topic(step_input: StepInput) -> Union[str, Step, List[Step]]:
    topic = step_input.input.lower()

    if "tech" in topic or "ai" in topic or "software" in topic:
        return "Tech Research"
    if "business" in topic or "market" in topic or "finance" in topic:
        return "Business Research"
    return "General Research"


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
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
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    workflow.print_response("Tell me about AI trends", stream=True)
