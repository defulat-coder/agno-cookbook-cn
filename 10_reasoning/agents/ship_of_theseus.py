"""
忒修斯之船辩论
======================

演示内置推理和 DeepSeek 推理模型在哲学分析中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
task = (
    "请探讨"忒修斯之船"的概念及其对身份认同与变化观念的启示。"
    "分别陈述支持和反对"一个已更换所有组件的物体本质上仍是同一物体"这一观点的论据。"
    "最后给出你自己有理有据的立场。"
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
