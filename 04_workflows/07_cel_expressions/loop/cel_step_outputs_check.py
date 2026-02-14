"""使用 CEL 结束条件的循环：检查命名步骤的输出。
=========================================================

使用 step_outputs 映射按名称访问特定步骤并
在决定停止循环之前检查其内容。

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
    instructions="研究给定主题。",
    markdown=True,
)

reviewer = Agent(
    name="Reviewer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=(
        "审查研究。如果研究彻底且完整，"
        "在响应中包含 APPROVED。"
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Step Outputs Check Loop",
    steps=[
        Loop(
            name="Research Loop",
            max_iterations=5,
            # 当 Reviewer 步骤批准研究时停止
            end_condition='step_outputs.Review.contains("APPROVED")',
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
    print('使用 CEL 结束条件的循环：step_outputs.Review.contains("APPROVED")')
    print("=" * 60)
    workflow.print_response(
        input="Research renewable energy trends",
        stream=True,
    )
