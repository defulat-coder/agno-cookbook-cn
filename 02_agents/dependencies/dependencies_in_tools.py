"""
工具中的依赖
=============================

示例展示工具如何访问传递给 agent 的依赖。
"""

from datetime import datetime

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run import RunContext


def get_current_context() -> dict:
    """获取当前上下文信息，如时间、天气等。"""
    return {
        "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": "PST",
        "day_of_week": datetime.now().strftime("%A"),
    }


def analyze_user(user_id: str, run_context: RunContext) -> str:
    """
    分析特定用户的个人资料并提供洞察。

    该工具使用可用的数据源分析用户行为和偏好。
    使用要分析的 user_id 调用此工具。

    Args:
        user_id: 要分析的用户 ID（例如 'john_doe'、'jane_smith'）
        run_context: 包含依赖的运行上下文（自动提供）

    Returns:
        关于用户的详细分析和洞察
    """
    dependencies = run_context.dependencies
    if not dependencies:
        return "No data sources available for analysis."

    print(f"--> Tool received data sources: {list(dependencies.keys())}")

    results = [f"=== USER ANALYSIS FOR {user_id.upper()} ==="]

    # 如果可用，使用用户资料数据
    if "user_profile" in dependencies:
        profile_data = dependencies["user_profile"]
        results.append(f"Profile Data: {profile_data}")

        # 根据资料添加分析
        if profile_data.get("role"):
            results.append(
                f"Professional Analysis: {profile_data['role']} with expertise in {', '.join(profile_data.get('preferences', []))}"
            )

    # 如果可用，使用当前上下文数据
    if "current_context" in dependencies:
        context_data = dependencies["current_context"]
        results.append(f"Current Context: {context_data}")
        results.append(
            f"Time-based Analysis: Analysis performed on {context_data['day_of_week']} at {context_data['current_time']}"
        )

    print(f"--> Tool returned results: {results}")

    return "\n\n".join(results)


# 使用分析工具函数创建一个 agent
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[analyze_user],
    name="User Analysis Agent",
    description="An agent specialized in analyzing users using integrated data sources.",
    instructions=[
        "你是一个用户分析专家，可以访问用户分析工具。",
        "当被要求分析任何用户时，使用 analyze_user 工具。",
        "该工具通过集成的数据源访问用户资料和当前上下文。",
        "获取工具结果后，根据分析提供额外的洞察和建议。",
        "在分析中要详尽，并解释工具发现了什么。",
    ],
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== Tool Dependencies Access Example ===\n")

    response = agent.run(
        input="Please analyze user 'john_doe' and provide insights about their professional background and preferences.",
        dependencies={
            "user_profile": {
                "name": "John Doe",
                "preferences": ["AI/ML", "Software Engineering", "Finance"],
                "location": "San Francisco, CA",
                "role": "Senior Software Engineer",
            },
            "current_context": get_current_context,
        },
        session_id="test_tool_dependencies",
    )

    print(f"\nAgent Response: {response.content}")
