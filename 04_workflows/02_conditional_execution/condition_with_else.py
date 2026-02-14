"""
带 Else 的条件
===================

演示使用 `Condition(..., else_steps=[...])` 在技术支持和常规支持分支之间进行路由。
"""

import asyncio

from agno.agent.agent import Agent
from agno.workflow.condition import Condition
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
diagnostic_agent = Agent(
    name="Diagnostic Agent",
    instructions=(
        "你是一位诊断专家。分析客户描述的技术问题，"
        "并列出最可能的根本原因。保持简洁。"
    ),
)

engineering_agent = Agent(
    name="Engineering Agent",
    instructions=(
        "你是一位资深工程师。根据诊断分析，提供"
        "客户可以遵循的逐步故障排除指南。"
    ),
)

general_support_agent = Agent(
    name="General Support Agent",
    instructions=(
        "你是一位友好的客户支持专员。帮助客户处理"
        "非技术问题——账单、账户、发货、退货等。"
    ),
)

followup_agent = Agent(
    name="Follow-Up Agent",
    instructions=(
        "你是一位跟进专员。总结到目前为止解决的问题，"
        "并询问客户是否还需要其他帮助。"
    ),
)


# ---------------------------------------------------------------------------
# 定义条件评估器
# ---------------------------------------------------------------------------
def is_technical_issue(step_input: StepInput) -> bool:
    text = (step_input.input or "").lower()
    tech_keywords = [
        "error",
        "bug",
        "crash",
        "not working",
        "broken",
        "install",
        "update",
        "password reset",
        "api",
        "timeout",
        "exception",
        "failed",
        "logs",
        "debug",
    ]
    return any(kw in text for kw in tech_keywords)


# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
diagnose_step = Step(
    name="Diagnose",
    description="对技术问题运行诊断",
    agent=diagnostic_agent,
)

engineer_step = Step(
    name="Engineer",
    description="提供工程级故障排除",
    agent=engineering_agent,
)

general_step = Step(
    name="GeneralSupport",
    description="处理非技术客户查询",
    agent=general_support_agent,
)

followup_step = Step(
    name="FollowUp",
    description="以跟进消息结束",
    agent=followup_agent,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="Customer Support Router",
    description="根据查询内容将客户查询路由到技术或常规支持管道",
    steps=[
        Condition(
            name="TechnicalTriage",
            description="根据查询内容路由到技术或常规支持",
            evaluator=is_technical_issue,
            steps=[diagnose_step, engineer_step],
            else_steps=[general_step],
        ),
        followup_step,
    ],
)

workflow_2 = Workflow(
    name="Customer Support Router",
    steps=[
        Condition(
            name="TechnicalTriage",
            evaluator=is_technical_issue,
            steps=[diagnose_step, engineer_step],
            else_steps=[general_step],
        ),
        followup_step,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("测试 1：技术查询（预期 if 分支）")
    print("=" * 60)
    workflow.print_response(
        "My app keeps crashing with a timeout error after the latest update"
    )

    print()
    print("=" * 60)
    print("测试 2：常规查询（预期 else 分支）")
    print("=" * 60)
    workflow_2.print_response("How do I change my shipping address for order #12345?")

    print()
    print("=" * 60)
    print("异步技术查询")
    print("=" * 60)
    asyncio.run(
        workflow.aprint_response(
            "My app keeps crashing with a timeout error after the latest update"
        )
    )

    print()
    print("=" * 60)
    print("异步常规查询")
    print("=" * 60)
    asyncio.run(
        workflow_2.aprint_response(
            "How do I change my shipping address for order #12345?"
        )
    )
