"""使用 Async MySQL 作为团队的数据库。
运行 `uv pip install openai duckduckgo-search newspaper4k lxml_html_clean agno sqlalchemy asyncmy` 安装依赖
"""

import asyncio
import uuid
from typing import List

from agno.agent import Agent
from agno.db.base import SessionType
from agno.db.mysql import AsyncMySQLDb
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "mysql+asyncmy://ai:ai@localhost:3306/ai"
db = AsyncMySQLDb(db_url=db_url)


# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
class Article(BaseModel):
    title: str
    summary: str
    reference_links: List[str]


hn_researcher = Agent(
    name="HackerNews Researcher",
    role="从 hackernews 获取热门故事。",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    role="在网上搜索某个主题的信息",
    tools=[WebSearchTools()],
    add_datetime_to_context=True,
)


hn_team = Team(
    name="HackerNews Team",
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
async def main():
    """在同一个事件循环中运行 Agent 查询"""
    session_id = str(uuid.uuid4())
    await hn_team.aprint_response(
        "Write an article about the top 2 stories on hackernews", session_id=session_id
    )
    session_data = await db.get_session(
        session_id=session_id, session_type=SessionType.TEAM
    )
    print("\n=== SESSION DATA ===")
    print(session_data.to_dict())


if __name__ == "__main__":
    asyncio.run(main())
