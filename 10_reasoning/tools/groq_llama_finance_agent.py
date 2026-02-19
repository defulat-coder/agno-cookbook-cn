"""
Groq Llama 金融 Agent
========================

演示推理 Cookbook 示例。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    thinking_llama = Agent(
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        tools=[
            ReasoningTools(),
            WebSearchTools(),
        ],
        instructions=dedent("""\
        ## 通用指令
        - 始终先使用 think 工具梳理完成任务所需的步骤。
        - 收到工具结果后，使用 think 工具作为草稿本验证结果的正确性。
        - 在回复用户之前，使用 think 工具记录最终想法和思路。
        - 尽可能以整洁的表格呈现最终输出。

        ## 使用 think 工具
        在每个步骤中，使用 think 工具作为草稿本：
        - 用自己的话重述目标，确保完全理解。
        - 列出适用于当前请求的具体规则。
        - 检查是否已收集所有必要信息且信息有效。
        - 验证计划的行动是否能完成任务。\
        """),
        markdown=True,
    )
    thinking_llama.print_response("撰写一份对比 NVDA 与 TSLA 的报告", stream=True)


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
