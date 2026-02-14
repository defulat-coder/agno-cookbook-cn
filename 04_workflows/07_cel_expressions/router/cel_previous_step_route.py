"""使用 CEL 的路由器：基于命名的前一步骤输出进行路由。
===============================================================

使用 previous_step_outputs 映射按名称访问分类器步骤，
然后根据分类路由到适当的处理程序。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import CEL_AVAILABLE, Step, Workflow
from agno.workflow.router import Router

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
        "将请求分类为一个类别。"
        "只回复一个单词：BILLING、TECHNICAL 或 GENERAL。"
    ),
    markdown=False,
)

billing_agent = Agent(
    name="Billing Support",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理账单咨询。帮助处理发票、付款和订阅。",
    markdown=True,
)

technical_agent = Agent(
    name="Technical Support",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理技术问题。帮助调试和配置。",
    markdown=True,
)

general_agent = Agent(
    name="General Support",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你处理一般性咨询。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Previous Step Outputs Router",
    steps=[
        Step(name="Classify", agent=classifier),
        Router(
            name="Support Router",
            # 通过 previous_step_outputs 映射按步骤名称访问分类器输出
            selector=(
                'previous_step_outputs.Classify.contains("BILLING") ? "Billing Support" : '
                'previous_step_outputs.Classify.contains("TECHNICAL") ? "Technical Support" : '
                '"General Support"'
            ),
            choices=[
                Step(name="Billing Support", agent=billing_agent),
                Step(name="Technical Support", agent=technical_agent),
                Step(name="General Support", agent=general_agent),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 账单问题 ---")
    workflow.print_response(input="I was charged twice on my last invoice.")
    print()

    print("--- 技术问题 ---")
    workflow.print_response(input="My API keeps returning 503 errors.")
