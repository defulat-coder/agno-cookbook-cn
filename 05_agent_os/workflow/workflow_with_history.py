"""
带历史的工作流
=====================

演示带历史的工作流。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.workflow.step import Step, StepInput, StepOutput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 定义用于餐食规划对话的专业 agent
meal_suggester = Agent(
    name="Meal Suggester",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "你是一个友好的餐食规划助手，建议餐食类别和菜系。",
        "考虑一天中的时间、星期几以及对话中的任何上下文。",
        "保持建议宽泛（意大利菜、亚洲菜、健康食品、舒适食品、快餐等）",
        "提出后续问题以更好地了解偏好。",
    ],
)

recipe_specialist = Agent(
    name="Recipe Specialist",
    model=OpenAIChat(id="gpt-4o"),
    instructions=[
        "你是一位食谱专家，提供具体、详细的食谱推荐。",
        "密切关注完整对话以了解用户偏好和限制。",
        "如果用户提到避免某些食物或想要更健康的选择，请尊重这一点。",
        "提供实用、易于遵循的食谱建议，包括配料和基本步骤。",
        "自然地引用对话（例如，'既然你提到想要更健康的东西...'）",
    ],
)


def analyze_food_preferences(step_input: StepInput) -> StepOutput:
    """
    分析对话历史以了解用户食物偏好的智能函数
    """
    current_request = step_input.input
    conversation_context = step_input.previous_step_content or ""

    # 基于对话的简单偏好分析
    preferences = {
        "dietary_restrictions": [],
        "cuisine_preferences": [],
        "avoid_list": [],
        "cooking_style": "any",
    }

    # 分析对话模式
    full_context = f"{conversation_context} {current_request}".lower()

    # 饮食限制和偏好
    if any(word in full_context for word in ["healthy", "healthier", "light", "fresh"]):
        preferences["dietary_restrictions"].append("healthy")
    if any(word in full_context for word in ["vegetarian", "veggie", "no meat"]):
        preferences["dietary_restrictions"].append("vegetarian")
    if any(word in full_context for word in ["quick", "fast", "easy", "simple"]):
        preferences["cooking_style"] = "quick"
    if any(word in full_context for word in ["comfort", "hearty", "filling"]):
        preferences["cooking_style"] = "comfort"

    # 要避免的食物/菜系（最近提到）
    if "italian" in full_context and (
        "had" in full_context or "yesterday" in full_context
    ):
        preferences["avoid_list"].append("Italian")
    if "chinese" in full_context and (
        "had" in full_context or "recently" in full_context
    ):
        preferences["avoid_list"].append("Chinese")

    # 积极提到的首选菜系
    if "love asian" in full_context or "like asian" in full_context:
        preferences["cuisine_preferences"].append("Asian")
    if "mediterranean" in full_context:
        preferences["cuisine_preferences"].append("Mediterranean")

    # 为食谱 agent 创建指导
    guidance = []
    if preferences["dietary_restrictions"]:
        guidance.append(
            f"Focus on {', '.join(preferences['dietary_restrictions'])} options"
        )
    if preferences["avoid_list"]:
        guidance.append(
            f"Avoid {', '.join(preferences['avoid_list'])} cuisine since user had it recently"
        )
    if preferences["cuisine_preferences"]:
        guidance.append(
            f"Consider {', '.join(preferences['cuisine_preferences'])} options"
        )
    if preferences["cooking_style"] != "any":
        guidance.append(f"Prefer {preferences['cooking_style']} cooking style")

    analysis_result = f"""
        PREFERENCE ANALYSIS:
        Current Request: {current_request}

        Detected Preferences:
        {chr(10).join(f"• {g}" for g in guidance) if guidance else "• No specific preferences detected"}

        RECIPE AGENT GUIDANCE:
        Based on the conversation history, please provide recipe recommendations that align with these preferences.
        Reference the conversation naturally and explain why these recipes fit their needs.
    """.strip()

    return StepOutput(content=analysis_result)


# 定义工作流步骤
suggestion_step = Step(
    name="Meal Suggestion",
    agent=meal_suggester,
)

preference_analysis_step = Step(
    name="Preference Analysis",
    executor=analyze_food_preferences,
)

recipe_step = Step(
    name="Recipe Recommendations",
    agent=recipe_specialist,
)

# 创建对话式餐食规划工作流
meal_workflow = Workflow(
    name="Conversational Meal Planner",
    description="Smart meal planning with conversation awareness and preference learning",
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/meal_workflow.db",
    ),
    steps=[suggestion_step, preference_analysis_step, recipe_step],
    add_workflow_history_to_steps=True,
    num_history_runs=3,
)

agent_os = AgentOS(
    description="Example OS setup",
    workflows=[meal_workflow],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="workflow_with_history:app", reload=True)
