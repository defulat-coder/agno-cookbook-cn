"""使用 CEL 结束条件的循环：N 次迭代后停止。
=====================================================

使用 current_iteration 在特定次数的迭代后停止，
独立于 max_iterations。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import CEL_AVAILABLE, Loop, Step, Workflow

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
if not CEL_AVAILABLE:
    print("CEL is not available. Install with: pip install cel-python")
    exit(1)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
writer = Agent(
    name="Writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="撰写一个扩展主题的简短段落。在之前的内容基础上构建。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Iteration Limit Loop",
    steps=[
        Loop(
            name="Writing Loop",
            max_iterations=10,
            # 在 2 次迭代后停止，即使最大值为 10
            end_condition="current_iteration >= 2",
            steps=[
                Step(name="Write", agent=writer),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("使用 CEL 结束条件的循环：current_iteration >= 2 (max_iterations=10)")
    print("=" * 60)
    workflow.print_response(
        input="Write about the history of the internet",
        stream=True,
    )
