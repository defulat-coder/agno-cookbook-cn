"""
带状态的指令
=============================

演示如何将函数用作 agent 的指令。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run import RunContext


# 这将是我们的指令函数
def get_run_instructions(run_context: RunContext) -> str:
    """基于运行上下文为 Agent 构建指令。"""
    if not run_context.session_state:
        return "你是一个乐于助人的游戏开发助手，可以回答有关编码和游戏设计的问题。"

    game_genre = run_context.session_state.get("game_genre", "")
    difficulty_level = run_context.session_state.get("difficulty_level", "")

    return dedent(
        f"""
        你是一个专业的游戏开发助手。
        团队目前正在开发一个 {game_genre} 游戏。
        当前项目难度级别设置为 {difficulty_level}。
        在提供编码建议、设计建议或技术指导时，请根据此类型和复杂性级别定制你的响应。"""
    )


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
game_development_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    instructions=get_run_instructions,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    game_development_agent.print_response(
        "What genre are we working on and what should I focus on for the core mechanics?",
        session_state={"game_genre": "platformer", "difficulty_level": "hard"},
    )
