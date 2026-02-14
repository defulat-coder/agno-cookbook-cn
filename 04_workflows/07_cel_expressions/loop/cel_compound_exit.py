"""使用 CEL 结束条件的循环：复合退出条件。
=====================================================

结合 all_success 和 current_iteration，在两个条件都满足时停止：
所有步骤成功 AND 运行了足够的迭代次数。

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
researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="研究给定主题并提供详细发现。",
    markdown=True,
)

reviewer = Agent(
    name="Reviewer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="审查研究的完整性和准确性。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Compound Exit Loop",
    steps=[
        Loop(
            name="Research Loop",
            max_iterations=5,
            end_condition="all_success && current_iteration >= 2",
            steps=[
                Step(name="Research", agent=researcher),
                Step(name="Review", agent=reviewer),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("使用 CEL 结束条件的循环：all_success && current_iteration >= 2")
    print("=" * 60)
    workflow.print_response(
        input="Research the impact of AI on healthcare",
        stream=True,
    )
