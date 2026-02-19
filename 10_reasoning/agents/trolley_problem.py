"""
电车难题分析
========================

演示内置推理和 DeepSeek 推理模型在伦理分析中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
cot_prompt = (
    "请解答电车难题，评估多种伦理框架，并用 ASCII 图示展示你的解答。"
)

deepseek_prompt = (
    "你是一位哲学家，任务是分析经典的"电车难题"。在这个场景中，一辆失控的电车正沿轨道高速冲向五名被绑住无法动弹的人。"
    "你站在轨道上方的一座天桥上，旁边站着一个陌生的高大男子。"
    "救下那五个人的唯一办法是把这个陌生人推下桥，让他落到下面的轨道上。这样会杀死这个陌生人，但能救下轨道上的五个人。"
    "你应该把这个陌生人推下去以拯救那五个人吗？"
    "请从功利主义、义务论和美德伦理学三种框架出发，给出有理有据的回答，并附上简单的 ASCII 艺术图来说明这个场景。"
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
    cot_agent.print_response(cot_prompt, stream=True, show_full_reasoning=True)

    print("\n=== DeepSeek 推理模型 ===")
    deepseek_agent.print_response(deepseek_prompt, stream=True)
