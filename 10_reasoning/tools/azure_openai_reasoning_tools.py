"""
Azure OpenAI 推理工具
============================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.azure.openai_chat import AzureOpenAI
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=AzureOpenAI(id="gpt-4o-mini"),
        tools=[
            WebSearchTools(),
            ReasoningTools(
                enable_think=True,
                enable_analyze=True,
                add_instructions=True,
                add_few_shot=True,
            ),
        ],
        instructions="尽可能使用表格。逐步思考问题。",
        markdown=True,
    )

    reasoning_agent.print_response(
        "撰写一份对比 NVDA 与 TSLA 的报告。",
        stream=True,
        show_full_reasoning=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
