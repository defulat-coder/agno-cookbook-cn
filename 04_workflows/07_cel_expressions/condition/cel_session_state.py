"""使用 CEL 表达式的条件：基于 session_state 进行分支。
==========================================================

使用 session_state.retry_count 实现重试逻辑。
多次运行工作流以显示计数器递增
并最终达到最大重试次数分支。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import (
    CEL_AVAILABLE,
    Condition,
    Step,
    StepInput,
    StepOutput,
    Workflow,
)

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
if not CEL_AVAILABLE:
    print("CEL is not available. Install with: pip install cel-python")
    exit(1)


# ---------------------------------------------------------------------------
# 定义辅助函数
# ---------------------------------------------------------------------------
def increment_retry_count(step_input: StepInput, session_state: dict) -> StepOutput:
    """在 session state 中递增重试计数。"""
    current_count = session_state.get("retry_count", 0)
    session_state["retry_count"] = current_count + 1
    return StepOutput(
        content=f"重试计数递增到 {session_state['retry_count']}",
        success=True,
    )


def reset_retry_count(step_input: StepInput, session_state: dict) -> StepOutput:
    """在 session state 中重置重试计数。"""
    session_state["retry_count"] = 0
    return StepOutput(content="重试计数重置为 0", success=True)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
retry_agent = Agent(
    name="Retry Handler",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你正在处理重试尝试。确认这是重试并尝试不同的方法。",
    markdown=True,
)

max_retries_agent = Agent(
    name="Max Retries Handler",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="已达到最大重试次数。提供有用的后备响应并建议替代方案。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Retry Logic",
    steps=[
        Step(name="Increment Retry", executor=increment_retry_count),
        Condition(
            name="Retry Check",
            evaluator="session_state.retry_count <= 3",
            steps=[
                Step(name="Attempt Retry", agent=retry_agent),
            ],
            else_steps=[
                Step(name="Max Retries Reached", agent=max_retries_agent),
                Step(name="Reset Counter", executor=reset_retry_count),
            ],
        ),
    ],
    session_state={"retry_count": 0},
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    for attempt in range(1, 6):
        print(f"--- 尝试 {attempt} ---")
        workflow.print_response(
            input=f"Process request (attempt {attempt})",
            stream=True,
        )
        print()
