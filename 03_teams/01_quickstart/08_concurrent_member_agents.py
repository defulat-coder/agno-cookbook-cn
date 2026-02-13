"""
并发成员 Agent
=============================

演示并发委托给团队成员，并流式传输成员事件。
"""

import asyncio
import time

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    role="处理 hackernews 请求",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[HackerNewsTools()],
    instructions="始终包含来源",
    stream=True,
    stream_events=True,
)

news_agent = Agent(
    name="News Agent",
    role="处理新闻请求和当前事件分析",
    model=OpenAIChat(id="gpt-4.1"),
    tools=[WebSearchTools()],
    instructions=[
        "使用表格显示新闻信息和发现。",
        "清楚地说明来源和发布日期。",
        "专注于提供当前和相关的新闻见解。",
    ],
    stream=True,
    stream_events=True,
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
research_team = Team(
    name="Reasoning Research Team",
    model=OpenAIChat(id="gpt-4.1"),
    members=[hackernews_agent, news_agent],
    instructions=[
        "协作提供全面的研究和新闻见解",
        "研究最新的世界新闻和 hackernews 帖子",
        "使用表格和图表清晰专业地展示数据",
    ],
    markdown=True,
    show_members_responses=True,
    stream_member_events=True,
)


async def test() -> None:
    print("启动 agent 运行...")
    start_time = time.time()

    generator = research_team.arun(
        """Research and compare recent developments in AI Agents:
        1. Get latest news about AI Agents from all your sources
        2. Compare and contrast the news from all your sources
        3. Provide a summary of the news from all your sources""",
        stream=True,
        stream_events=True,
    )

    async for event in generator:
        current_time = time.time() - start_time

        if hasattr(event, "event"):
            if "ToolCallStarted" in event.event:
                print(f"[{current_time:.2f}s] {event.event} - {event.tool.tool_name}")
            elif "ToolCallCompleted" in event.event:
                print(f"[{current_time:.2f}s] {event.event} - {event.tool.tool_name}")
            elif "RunStarted" in event.event:
                print(f"[{current_time:.2f}s] {event.event}")

    total_time = time.time() - start_time
    print(f"总执行时间: {total_time:.2f}s")


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(test())
