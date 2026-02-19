"""
推理金融 Agent
=======================

演示内置推理和 DeepSeek 推理模型在金融报告中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools()],
    instructions="使用表格展示数据",
    use_json_mode=True,
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools()],
    instructions=["尽可能使用表格"],
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    prompt = "撰写一份对比 NVDA 与 TSLA 的报告"

    print("=== 内置思维链（Chain Of Thought） ===")
    cot_agent.print_response(prompt, stream=True, show_full_reasoning=True)

    print("\n=== DeepSeek 推理模型 ===")
    deepseek_agent.print_response(prompt, stream=True, show_full_reasoning=True)
