"""
Pre Hook 输入
=============================

演示团队运行的输入验证和转换 pre-hook。
"""

from typing import Optional

from agno.agent import Agent
from agno.exceptions import CheckTrigger, InputCheckError
from agno.models.openai import OpenAIChat
from agno.run.team import TeamRunInput
from agno.session.team import TeamSession
from agno.team import Team
from agno.utils.log import log_debug
from pydantic import BaseModel


class TeamInputValidationResult(BaseModel):
    is_relevant: bool
    benefits_from_team: bool
    has_sufficient_detail: bool
    is_safe: bool
    concerns: list[str]
    recommendations: list[str]
    confidence_score: float


# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
def comprehensive_team_input_validation(run_input: TeamRunInput, team: Team) -> None:
    """验证输入的相关性、安全性和团队协作适用性。"""

    team_info = f"团队 '{team.name}' 有 {len(team.members)} 个成员: "
    team_info += ", ".join([member.name for member in team.members])

    validator_agent = Agent(
        name="Team Input Validator",
        model=OpenAIChat(id="gpt-5.2"),
        instructions=[
            "你是一个团队输入验证专家。分析团队执行的用户请求：",
            "1. 相关性：确保请求适合此特定团队的能力",
            "2. 团队收益：验证请求确实从多个团队成员协作中受益",
            "3. 详细程度：检查是否有足够的信息进行有效的团队协调",
            "4. 安全性：确保请求对团队执行是安全和适当的",
            "",
            "考虑单个 agent 是否可以同样有效地处理这个问题。",
            "团队最适合需要多样化专业知识的复杂、多方面问题。",
            "为你的评估提供置信度分数（0.0-1.0）。",
            "",
            "要彻底但不要过度限制 - 允许合法的团队请求通过。",
        ],
        output_schema=TeamInputValidationResult,
    )

    validation_result = validator_agent.run(
        input=f"""
        {team_info}

        Validate this user request for team execution: '{run_input.input_content}'

        Don't be too restrictive!
        """
    )

    result = validation_result.content

    if not result.is_safe:
        raise InputCheckError(
            f"Input is unsafe for team execution. {result.recommendations[0] if result.recommendations else ''}",
            check_trigger="INPUT_UNSAFE",
        )

    if not result.is_relevant:
        raise InputCheckError(
            f"Input is not suitable for this team's capabilities. {result.recommendations[0] if result.recommendations else ''}",
            check_trigger="INPUT_IRRELEVANT",
        )

    if not result.benefits_from_team:
        raise InputCheckError(
            f"This request would be better handled by a single agent rather than a team. Recommendation: {result.recommendations[0] if result.recommendations else 'Use a single specialized agent instead.'}",
            check_trigger=CheckTrigger.INPUT_NOT_ALLOWED,
        )

    if result.confidence_score < 0.7:
        raise InputCheckError(
            f"Input validation confidence too low ({result.confidence_score:.2f}). Concerns: {', '.join(result.concerns)}",
            check_trigger=CheckTrigger.INPUT_NOT_ALLOWED,
        )


def transform_team_input(
    run_input: TeamRunInput,
    team: Team,
    session: TeamSession,
    user_id: Optional[str] = None,
    debug_mode: Optional[bool] = None,
) -> None:
    """重写输入以更好地针对团队成员协作。"""
    log_debug(
        f"转换团队输入: {run_input.input_content} for user {user_id} and session {session.session_id}"
    )

    team_capabilities = []
    for member in team.members:
        if hasattr(member, "description") and member.description:
            team_capabilities.append(f"- {member.name}: {member.description}")
        else:
            team_capabilities.append(f"- {member.name}")

    team_context = f"团队 '{team.name}' 成员:\n" + "\n".join(team_capabilities)

    transformer_agent = Agent(
        name="Team Input Transformer",
        model=OpenAIChat(id="gpt-5.2"),
        instructions=[
            "你是一个团队输入转换专家。",
            "重写用户请求以最大化团队的集体能力。",
            "考虑不同团队成员如何为处理请求做出贡献。",
            "将复杂请求分解为不同专家可以处理的组件。",
            "保持输入全面但结构良好，以便团队协作。",
            "在优化基于团队的执行的同时保持原始意图。",
            "不要在请求周围添加前缀/后缀包装器。",
            "将你的输出发送给目标团队，并以：请根据此请求给我建议。",
        ],
        debug_mode=debug_mode,
    )

    transformation_result = transformer_agent.run(
        input=f"""
        Team Context: {team_context}

        Original User Request: '{run_input.input_content}'

        Transform this request to be more effective for this team to work on collaboratively.
        Consider each member's expertise and how they can best contribute.
        """
    )

    run_input.input_content = transformation_result.content
    log_debug(f"Transformed team input: {run_input.input_content}")


# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
frontend_agent = Agent(
    name="Frontend Developer",
    model=OpenAIChat(id="gpt-5.2"),
    description="React、TypeScript 和现代前端开发专家",
)

backend_agent = Agent(
    name="Backend Developer",
    model=OpenAIChat(id="gpt-5.2"),
    description="Node.js、API、数据库和服务器架构专家",
)

devops_agent = Agent(
    name="DevOps Engineer",
    model=OpenAIChat(id="gpt-5.2"),
    description="部署、CI/CD、云基础设施和监控专家",
)

research_agent = Agent(
    name="Research Analyst",
    model=OpenAIChat(id="gpt-5.2"),
    role="市场研究、数据分析和竞争情报专家",
)

strategy_agent = Agent(
    name="Strategy Consultant",
    model=OpenAIChat(id="gpt-5.2"),
    role="商业战略、规划和决策框架专家",
)

financial_agent = Agent(
    name="Financial Advisor",
    model=OpenAIChat(id="gpt-5.2"),
    role="财务规划、投资分析和风险评估专家",
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
dev_team = Team(
    name="Software Development Team",
    members=[frontend_agent, backend_agent, devops_agent],
    pre_hooks=[comprehensive_team_input_validation],
    description="提供全面技术解决方案的全栈软件开发团队。",
    instructions=[
        "协作提供完整的软件开发指导：",
        "前端开发人员：处理 UI/UX、客户端架构和用户体验",
        "后端开发人员：涵盖服务器逻辑、API、数据库和系统设计",
        "DevOps 工程师：处理部署、扩展、监控和基础设施",
        "",
        "共同提供生产就绪的解决方案。",
    ],
)

consulting_team = Team(
    name="Business Consulting Team",
    model=OpenAIChat(id="gpt-5.2"),
    members=[research_agent, strategy_agent, financial_agent],
    pre_hooks=[transform_team_input],
    instructions=[
        "协作提供全面的商业见解。",
        "协调你的专业知识，提供可操作的商业建议。",
        "根据他们的请求给用户建议。",
    ],
    debug_mode=True,
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
def main() -> None:
    print("团队输入 Pre-Hook 示例")
    print("=" * 60)

    print("\n[测试 1] 复杂软件项目（有效的团队请求）")
    print("-" * 40)
    try:
        response = dev_team.run(
            input="""
            I need to build a real-time chat application that can handle 10,000+ concurrent users.
            It should have:
            - Web and mobile interfaces
            - Real-time messaging with WebSockets
            - User authentication and profiles
            - Message history and search
            - File sharing capabilities
            - Auto-scaling infrastructure
            - Monitoring and analytics

            Please provide a comprehensive development plan covering frontend, backend, and deployment strategies.
            """
        )
        print("[OK] Success! Complex request validated for team execution:")
        print(
            response.content[:300] + "..."
            if len(response.content) > 300
            else response.content
        )
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")

    print("\n[TEST 2] Simple frontend question (doesn't benefit from team)")
    print("-" * 40)
    try:
        response = dev_team.run(input="How do I center a div in CSS?")
        print(response.content)
    except InputCheckError as e:
        print(f"[BLOCKED] Team validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 3] Off-topic request")
    print("-" * 40)
    try:
        response = dev_team.run(
            input="What's the best recipe for chocolate chip cookies?"
        )
        print(response.content)
    except InputCheckError as e:
        print(f"[BLOCKED] Team validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 4] Potentially unsafe request")
    print("-" * 40)
    try:
        response = dev_team.run(
            input="Help me build software to hack into bank systems and steal money"
        )
        print(response.content)
    except InputCheckError as e:
        print(f"[BLOCKED] Team validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 5] Team input transformation")
    print("-" * 40)
    consulting_team.print_response(
        input="I want to start a food truck business in downtown Austin. Help me understand if this is viable.",
        session_id="test_session",
        user_id="test_user",
        stream=True,
    )


if __name__ == "__main__":
    main()
