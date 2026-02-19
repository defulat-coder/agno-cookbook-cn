"""
Claude 推理工具
======================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.reasoning import ReasoningTools
from agno.tools.websearch import WebSearchTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            WebSearchTools(enable_news=False),
        ],
        instructions="使用表格展示数据。",
        markdown=True,
    )

    # 半导体市场分析示例
    reasoning_agent.print_response(
        """\
        请分析以下半导体公司的市场表现：
        - 英伟达 (NVDA)
        - AMD (AMD)
        - 英特尔 (INTC)
        - 台积电 (TSM)
        比较它们的市场地位、增长指标和未来展望。""",
        stream=True,
        show_full_reasoning=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
