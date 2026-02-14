"""使用 CEL 表达式的路由器：从 additional_data 字段进行路由。
=============================================================

使用 additional_data.route 让调用者指定要运行哪个步骤，
当路由决策在上游（例如 UI）做出时很有用。

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
email_agent = Agent(
    name="Email Writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你撰写专业的邮件。简洁且精炼。",
    markdown=True,
)

blog_agent = Agent(
    name="Blog Writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你撰写引人入胜的博客文章，具有清晰的结构和标题。",
    markdown=True,
)

tweet_agent = Agent(
    name="Tweet Writer",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你撰写简洁有力的推文。保持在 280 个字符以内。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Additional Data Router",
    steps=[
        Router(
            name="Content Format Router",
            selector="additional_data.route",
            choices=[
                Step(name="Email Writer", agent=email_agent),
                Step(name="Blog Writer", agent=blog_agent),
                Step(name="Tweet Writer", agent=tweet_agent),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 路由到邮件 ---")
    workflow.print_response(
        input="Write about our new product launch.",
        additional_data={"route": "Email Writer"},
    )
    print()

    print("--- 路由到推文 ---")
    workflow.print_response(
        input="Write about our new product launch.",
        additional_data={"route": "Tweet Writer"},
    )
