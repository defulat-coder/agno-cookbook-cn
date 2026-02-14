"""使用 CEL 的条件：基于命名步骤的输出进行分支。
==========================================================

使用 previous_step_outputs 映射按名称检查特定步骤的输出，
使多步骤管道能够具有条件逻辑。

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
researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="研究该主题。如果主题涉及安全风险，在响应中包含 SAFETY_REVIEW_NEEDED。",
    markdown=True,
)

safety_reviewer = Agent(
    name="Safety Reviewer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="审查研究的安全问题并提供建议。",
    markdown=True,
)

publisher = Agent(
    name="Publisher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="准备研究以供发布。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Previous Step Outputs Condition",
    steps=[
        Step(name="Research", agent=researcher),
        Condition(
            name="Safety Check",
            # 按名称检查 Research 步骤输出
            evaluator='previous_step_outputs.Research.contains("SAFETY_REVIEW_NEEDED")',
            steps=[
                Step(name="Safety Review", agent=safety_reviewer),
            ],
        ),
        Step(name="Publish", agent=publisher),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 安全主题（跳过安全审查）---")
    workflow.print_response(input="Write about gardening tips for beginners.")
    print()

    print("--- 安全敏感主题（触发安全审查）---")
    workflow.print_response(
        input="Write about handling hazardous chemicals in a home lab."
    )
