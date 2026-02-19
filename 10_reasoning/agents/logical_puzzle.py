"""
传教士与食人族谜题
=================================

演示内置推理和 DeepSeek 推理模型在逻辑谜题求解中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
task = (
    "三名传教士和三名食人族需要过河。"
    "他们有一艘每次最多能载两人的船。"
    "如果在任何时刻，河的任意一侧食人族人数超过传教士，食人族就会吃掉传教士。"
    "怎样才能让六人全部安全过河？请提供逐步解答，并以 ASCII 图示展示解答过程。"
)

cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 内置思维链（Chain Of Thought） ===")
    cot_agent.print_response(task, stream=True, show_full_reasoning=True)

    print("\n=== DeepSeek 推理模型 ===")
    deepseek_agent.print_response(task, stream=True, show_full_reasoning=True)
