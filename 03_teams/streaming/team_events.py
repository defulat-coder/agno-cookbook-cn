"""
团队事件
===========

演示在类似同步和异步事件流中监控团队和成员事件。
"""

import asyncio
from uuid import uuid4

from agno.agent import Agent, RunEvent
from agno.models.anthropic.claude import Claude
from agno.models.openai import OpenAIChat
from agno.team import Team, TeamRunEvent
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
hacker_news_agent = Agent(
    id="hacker-news-agent",
    name="Hacker News Agent",
    role="在 Hacker News 中搜索信息",
    tools=[HackerNewsTools()],
    instructions=[
        "在 Hacker News 中查找关于该公司的文章",
    ],
)

website_agent = Agent(
    id="website-agent",
    name="Website Agent",
    role="在网站上搜索信息",
    model=OpenAIChat(id="o3-mini"),
    tools=[WebSearchTools()],
    instructions=[
        "在网站上搜索信息",
    ],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
user_id = str(uuid4())
team_id = str(uuid4())

company_info_team = Team(
    name="Company Info Team",
    id=team_id,
    user_id=user_id,
    model=Claude(id="claude-3-7-sonnet-latest"),
    members=[hacker_news_agent, website_agent],
    markdown=True,
    instructions=[
        "你是一个寻找公司信息的团队。",
        "首先在网络和 Hacker News 上搜索有关该公司的信息。",
        "如果你能找到公司的网站 URL，则抓取首页和关于页面。",
    ],
    show_members_responses=True,
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
async def run_team_with_events(prompt: str) -> None:
    content_started = False
    async for run_output_event in company_info_team.arun(
        prompt,
        stream=True,
        stream_events=True,
    ):
        if run_output_event.event in [
            TeamRunEvent.run_started,
            TeamRunEvent.run_completed,
        ]:
            print(f"\n团队事件: {run_output_event.event}")

        if run_output_event.event in [TeamRunEvent.tool_call_started]:
            print(f"\n团队事件: {run_output_event.event}")
            print(f"工具调用: {run_output_event.tool.tool_name}")
            print(f"工具调用参数: {run_output_event.tool.tool_args}")

        if run_output_event.event in [TeamRunEvent.tool_call_completed]:
            print(f"\n团队事件: {run_output_event.event}")
            print(f"工具调用: {run_output_event.tool.tool_name}")
            print(f"工具调用结果: {run_output_event.tool.result}")

        if run_output_event.event in [RunEvent.tool_call_started]:
            print(f"\n成员事件: {run_output_event.event}")
            print(f"AGENT ID: {run_output_event.agent_id}")
            print(f"工具调用: {run_output_event.tool.tool_name}")
            print(f"工具调用参数: {run_output_event.tool.tool_args}")

        if run_output_event.event in [RunEvent.tool_call_completed]:
            print(f"\n成员事件: {run_output_event.event}")
            print(f"AGENT ID: {run_output_event.agent_id}")
            print(f"工具调用: {run_output_event.tool.tool_name}")
            print(f"工具调用结果: {run_output_event.tool.result}")

        if run_output_event.event in [TeamRunEvent.run_content]:
            if not content_started:
                print("内容")
                content_started = True
            else:
                print(run_output_event.content, end="")


if __name__ == "__main__":
    # 异步事件流式传输
    asyncio.run(
        run_team_with_events(
            "Write me a full report on everything you can find about Agno, the company building AI agent infrastructure.",
        )
    )
