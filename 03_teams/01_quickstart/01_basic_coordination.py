"""
基础协作
=============================

演示团队协调工作流，支持同步和异步执行模式。
"""

import asyncio
from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.newspaper4k import Newspaper4kTools
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel, Field


class Article(BaseModel):
    title: str = Field(..., description="The title of the article")
    summary: str = Field(..., description="A summary of the article")
    reference_links: List[str] = Field(
        ..., description="A list of reference links to the article"
    )


# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
sync_hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("gpt-5.2"),
    role="从 hackernews 获取热门故事。",
    tools=[HackerNewsTools()],
)

sync_article_reader = Agent(
    name="Article Reader",
    model=OpenAIChat("gpt-5.2"),
    role="从 URL 读取文章。",
    tools=[Newspaper4kTools()],
)

async_hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("o3-mini"),
    role="从 hackernews 获取热门故事。",
    tools=[HackerNewsTools()],
)

async_web_searcher = Agent(
    name="Web Searcher",
    model=OpenAIChat("o3-mini"),
    role="在网络上搜索主题相关信息",
    tools=[WebSearchTools()],
    add_datetime_to_context=True,
)

async_article_reader = Agent(
    name="Article Reader",
    role="从 URL 读取文章。",
    tools=[Newspaper4kTools()],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
sync_hn_team = Team(
    name="HackerNews Team",
    model=OpenAIChat("gpt-5.2"),
    members=[sync_hn_researcher, sync_article_reader],
    instructions=[
        "First, search hackernews for what the user is asking about.",
        "Then, ask the article reader to read the links for the stories to get more information.",
        "Important: you must provide the article reader with the links to read.",
        "Then, ask the web searcher to search for each story to get more information.",
        "Finally, provide a thoughtful and engaging summary.",
    ],
    output_schema=Article,
    add_member_tools_to_context=False,
    markdown=True,
    show_members_responses=True,
)

async_hn_team = Team(
    name="HackerNews Team",
    model=OpenAIChat("o3"),
    members=[async_hn_researcher, async_web_searcher, async_article_reader],
    instructions=[
        "首先，在 hackernews 上搜索用户询问的内容。",
        "然后，让文章阅读器读取故事链接以获取更多信息。",
        "重要：你必须向文章阅读器提供要读取的链接。",
        "接着，让网络搜索器搜索每个故事以获取更多信息。",
        "最后，提供一个深思熟虑且引人入胜的摘要。",
    ],
    output_schema=Article,
    add_member_tools_to_context=False,
    markdown=True,
    show_members_responses=True,
)


async def run_async_coordination() -> None:
    await async_hn_team.aprint_response(
        input="Write an article about the top 2 stories on hackernews"
    )


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- 同步 ---
    sync_hn_team.print_response(
        input="Write an article about the top 2 stories on hackernews", stream=True
    )

    # --- 异步 ---
    asyncio.run(run_async_coordination())
