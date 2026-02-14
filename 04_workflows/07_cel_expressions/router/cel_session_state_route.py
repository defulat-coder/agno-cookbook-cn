"""使用 CEL 表达式的路由器：从 session_state 进行路由。
=====================================================

使用 session_state.preferred_handler 在工作流运行之间
持久化路由偏好。

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
detailed_agent = Agent(
    name="Detailed Analyst",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你提供带有示例和数据的详细、深入的分析。",
    markdown=True,
)

brief_agent = Agent(
    name="Brief Analyst",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你提供简要的、执行摘要风格的分析。保持简短。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Session State Router",
    steps=[
        Router(
            name="Analysis Style Router",
            selector="session_state.preferred_handler",
            choices=[
                Step(name="Detailed Analyst", agent=detailed_agent),
                Step(name="Brief Analyst", agent=brief_agent),
            ],
        ),
    ],
    session_state={"preferred_handler": "Brief Analyst"},
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 使用 session_state 偏好：Brief Analyst ---")
    workflow.print_response(input="Analyze the current state of cloud computing.")
    print()

    # 更改偏好
    workflow.session_state["preferred_handler"] = "Detailed Analyst"
    print("--- 已将偏好更改为：Detailed Analyst ---")
    workflow.print_response(input="Analyze the current state of cloud computing.")
