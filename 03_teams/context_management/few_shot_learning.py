"""
Few-Shot 学习
=============================

演示使用 additional_input 示例来指导团队支持响应。
"""

from agno.agent import Agent
from agno.models.message import Message
from agno.models.openai.chat import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
support_examples = [
    Message(role="user", content="I forgot my password and can't log in"),
    Message(
        role="assistant",
        content="""
    我会立即帮你重置密码。

    **转接至支持专员**: 请协助此客户重置密码：
    - 引导他们完成密码重置流程
    - 如需要，验证其身份
    - 确保他们能成功登录
    - 提供创建安全密码的提示

    预期结果：客户成功使用新密码登录。
    """.strip(),
    ),
    Message(
        role="user",
        content="I've been charged twice for the same order and your chat bot couldn't help!",
    ),
    Message(
        role="assistant",
        content="""
        我对账单问题和聊天系统带来的困扰深表歉意。

        **转接至升级经理**: 需要立即关注的优先账单问题：
        - 客户对同一订单被收费两次
        - 之前的自动支持未成功
        - 客户自然很沮丧
        - 需要立即解决并可能给予补偿

        预期结果：账单已纠正，客户满意度恢复，并跟进以防止再次发生。
        """.strip(),
    ),
    Message(role="user", content="Your app keeps crashing when I try to upload photos"),
    Message(
        role="assistant",
        content="""
    很抱歉你在上传照片时遇到崩溃问题。让我帮你解决这个问题。

    **转接至支持专员**: 照片上传功能的技术问题：
    - 应用在照片上传过程中崩溃
    - 需要排查设备兼容性和应用版本
    - 如果有可用的临时解决方案请提供
    - 如果是已知错误，则升级到技术团队

    预期结果：上传功能正常工作或提供明确的修复时间表。
        """.strip(),
    ),
]

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
support_agent = Agent(
    name="Support Specialist",
    role="处理客户咨询",
    model=OpenAIChat(id="o3-mini"),
    instructions=[
        "你是一名乐于助人的客户支持专员。",
        "始终保持礼貌、专业和解决方案导向。",
    ],
)

escalation_agent = Agent(
    name="Escalation Manager",
    role="处理复杂问题",
    model=OpenAIChat(id="o3-mini"),
    instructions=[
        "你处理需要管理层关注的升级客户问题。",
        "专注于客户满意度和寻找解决方案。",
    ],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
team = Team(
    name="Customer Support Team",
    members=[support_agent, escalation_agent],
    model=OpenAIChat(id="o3-mini"),
    add_name_to_context=True,
    additional_input=support_examples,
    instructions=[
        "你以卓越和同理心协调客户支持。",
        "遵循既定的模式以正确解决问题。",
        "始终优先考虑客户满意度和清晰沟通。",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    scenarios = [
        "I can't find my order confirmation email",
        "The product I received is damaged",
        "I want to cancel my subscription but the website won't let me",
    ]

    for i, scenario in enumerate(scenarios, 1):
        print(f"场景 {i}: {scenario}")
        print("-" * 50)
        team.print_response(scenario)
