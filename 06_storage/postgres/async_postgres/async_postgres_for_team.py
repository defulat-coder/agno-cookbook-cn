"""
1. 运行: `uv pip install openai ddgs newspaper4k lxml_html_clean agno` 安装依赖
2. 运行: `python cookbook/db/async_postgres/async_postgres_for_team.py` 运行团队
"""

import asyncio
from typing import List

from agno.agent import Agent
from agno.db.postgres import AsyncPostgresDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg_async://ai:ai@localhost:5532/ai"
db = AsyncPostgresDb(db_url=db_url)


# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
class Article(BaseModel):
    title: str
    summary: str
    reference_links: List[str]


hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("gpt-4o"),
    role="从 hackernews 获取热门故事。",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    model=OpenAIChat("gpt-4o"),
    role="在网上搜索某个主题的信息",
    tools=[WebSearchTools()],
    add_datetime_to_context=True,
)


hn_team = Team(
    name="HackerNews Team",
    model=OpenAIChat("gpt-4o"),
    members=[hn_researcher, web_searcher],
    db=db,
    instructions=[
        "首先，在 hackernews 上搜索用户询问的内容。",
        "然后，让网络搜索者搜索每个故事以获取更多信息。",
        "最后，提供一个有思想和吸引力的摘要。",
    ],
    output_schema=Article,
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(
        hn_team.aprint_response(
            "Write an article about the top 2 stories on hackernews"
        )
    )
