"""使用 CEL 的路由器：使用 step_choices 索引进行路由。
================================================

使用 step_choices[0]、step_choices[1] 等通过它们在选择列表中的
位置引用步骤，而不是硬编码步骤名称。

这在以下情况下很有用：
- 避免步骤名称中的拼写错误
- 使 CEL 表达式更易于维护
- 根据索引动态引用步骤

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
quick_analyzer = Agent(
    name="Quick Analyzer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="提供对主题的简要、简洁的分析。",
    markdown=True,
)

detailed_analyzer = Agent(
    name="Detailed Analyzer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="提供对主题的全面、深入的分析。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Step Choices Router",
    steps=[
        Router(
            name="Analysis Router",
            # step_choices[0] = "Quick Analysis"（第一个选择）
            # step_choices[1] = "Detailed Analysis"（第二个选择）
            selector='input.contains("quick") || input.contains("brief") ? step_choices[0] : step_choices[1]',
            choices=[
                Step(name="Quick Analysis", agent=quick_analyzer),
                Step(name="Detailed Analysis", agent=detailed_analyzer),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 这将路由到 step_choices[0]（"Quick Analysis"）
    print("=== 快速分析请求 ===")
    workflow.print_response(
        input="Give me a quick overview of quantum computing.", stream=True
    )

    print("\n" + "=" * 50 + "\n")

    # 这将路由到 step_choices[1]（"Detailed Analysis"）
    print("=== 详细分析请求 ===")
    workflow.print_response(input="Explain quantum computing in detail.", stream=True)
