"""使用 CEL 表达式的条件：基于前一步骤输出进行分支。
=================================================================

首先运行分类器步骤，然后使用 previous_step_content.contains()
决定下一步。

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
classifier = Agent(
    name="Classifier",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=(
        "将请求分类为技术类或常规类。"
        "只用一个单词回复：TECHNICAL 或 GENERAL。"
    ),
    markdown=False,
)

technical_agent = Agent(
    name="Technical Support",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你是一位技术支持专家。提供详细的技术帮助。",
    markdown=True,
)

general_agent = Agent(
    name="General Support",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理一般性咨询。友好且乐于助人。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Classify and Route",
    steps=[
        Step(name="Classify", agent=classifier),
        Condition(
            name="Route by Classification",
            evaluator='previous_step_content.contains("TECHNICAL")',
            steps=[
                Step(name="Technical Help", agent=technical_agent),
            ],
            else_steps=[
                Step(name="General Help", agent=general_agent),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 技术问题 ---")
    workflow.print_response(
        input="My API returns 500 errors when I send POST requests with JSON payloads."
    )
    print()

    print("--- 常规问题 ---")
    workflow.print_response(input="What are your business hours?")
