"""
输入模式
=============================

演示如何使用输入模式验证 Agent 的输入参数。
"""

from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.hackernews import HackerNewsTools
from pydantic import BaseModel, Field


class ResearchTopic(BaseModel):
    """包含特定要求的结构化研究主题"""

    topic: str
    focus_areas: List[str] = Field(description="Specific areas to focus on")
    target_audience: str = Field(description="Who this research is for")
    sources_required: int = Field(description="Number of sources needed", default=5)


# 定义 agents
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    role="Extract key insights and content from Hackernews posts",
    input_schema=ResearchTopic,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 传递一个与输入模式匹配的字典
    hackernews_agent.print_response(
        input={
            "topic": "AI",
            "focus_areas": ["AI", "Machine Learning"],
            "target_audience": "Developers",
            "sources_required": "5",
        }
    )

    # 传递一个与输入模式匹配的 pydantic 模型
    hackernews_agent.print_response(
        input=ResearchTopic(
            topic="AI",
            focus_areas=["AI", "Machine Learning"],
            target_audience="Developers",
            sources_required=5,
        )
    )
