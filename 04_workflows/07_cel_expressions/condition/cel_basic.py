"""使用 CEL 表达式的条件：根据输入内容进行路由。
============================================================

使用 input.contains() 检查请求是否紧急，
通过 if/else 步骤分支到不同的 Agent。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import CEL_AVAILABLE, Condition, Step, Workflow

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
if not CEL_AVAILABLE:
    print("CEL is not available. Install with: pip install cel-python")
    exit(1)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
urgent_handler = Agent(
    name="Urgent Handler",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理高优先级的紧急请求。简洁且以行动为导向。",
    markdown=True,
)

normal_handler = Agent(
    name="Normal Handler",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你彻底且深思熟虑地处理正常请求。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Input Routing",
    steps=[
        Condition(
            name="Urgent Check",
            evaluator='input.contains("urgent")',
            steps=[
                Step(name="Handle Urgent", agent=urgent_handler),
            ],
            else_steps=[
                Step(name="Handle Normal", agent=normal_handler),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 紧急请求 ---")
    workflow.print_response(
        input="This is an urgent request - please help immediately!"
    )
    print()

    print("--- 正常请求 ---")
    workflow.print_response(input="I have a general question about your services.")
