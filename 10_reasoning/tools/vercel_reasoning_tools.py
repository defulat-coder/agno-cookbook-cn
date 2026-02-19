"""
Vercel 推理工具
======================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.vercel import V0
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=V0(id="v0-1.0-md"),
        tools=[
            ReasoningTools(add_instructions=True, add_few_shot=True),
            WebSearchTools(),
        ],
        instructions=[
            "使用表格展示数据",
            "只输出报告内容，不要其他文字",
        ],
        markdown=True,
    )
    reasoning_agent.print_response(
        "撰写一份关于 TSLA 的报告",
        stream=True,
        show_full_reasoning=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
