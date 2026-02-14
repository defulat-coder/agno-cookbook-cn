"""使用 CEL 表达式的条件：基于 additional_data 进行分支。
============================================================

使用 additional_data.priority 将高优先级请求
路由到专门的 Agent。

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
high_priority_agent = Agent(
    name="High Priority Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理高优先级任务。全面且详细。",
    markdown=True,
)

low_priority_agent = Agent(
    name="Low Priority Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理标准任务。乐于助人且简洁。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Priority Routing",
    steps=[
        Condition(
            name="Priority Gate",
            evaluator="additional_data.priority > 5",
            steps=[
                Step(name="High Priority", agent=high_priority_agent),
            ],
            else_steps=[
                Step(name="Low Priority", agent=low_priority_agent),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 高优先级 (8) ---")
    workflow.print_response(
        input="Review this critical security report.",
        additional_data={"priority": 8},
    )
    print()

    print("--- 低优先级 (2) ---")
    workflow.print_response(
        input="Update the FAQ page.",
        additional_data={"priority": 2},
    )
