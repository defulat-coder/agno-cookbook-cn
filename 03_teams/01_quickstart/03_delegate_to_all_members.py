"""
委托给所有成员
=============================

演示具有委托给所有成员行为的协作团队执行。
"""

import asyncio
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
reddit_researcher = Agent(
    name="Reddit Researcher",
    role="在 Reddit 上研究主题",
    model=OpenAIChat(id="o3-mini"),
    tools=[WebSearchTools()],
    add_name_to_context=True,
    instructions=dedent("""
    你是一名 Reddit 研究员。
    你将被给予一个在 Reddit 上研究的主题。
    你需要在 Reddit 上找到最相关的帖子。
    """),
)

hackernews_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("o3-mini"),
    role="在 HackerNews 上研究主题。",
    tools=[HackerNewsTools()],
    add_name_to_context=True,
    instructions=dedent("""
    你是一名 HackerNews 研究员。
    你将被给予一个在 HackerNews 上研究的主题。
    你需要在 HackerNews 上找到最相关的帖子。
    """),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
agent_team = Team(
    name="Discussion Team",
    model=OpenAIChat("o3-mini"),
    members=[
        reddit_researcher,
        hackernews_researcher,
    ],
    instructions=[
        "你是一名讨论主持人。",
        "当你认为团队已达成共识时，你必须停止讨论。",
    ],
    markdown=True,
    delegate_to_all_members=True,
    show_members_responses=True,
)


async def run_async_collaboration() -> None:
    await agent_team.aprint_response(
        input="Start the discussion on the topic: 'What is the best way to learn to code?'",
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- 同步 ---
    agent_team.print_response(
        input="Start the discussion on the topic: 'What is the best way to learn to code?'",
        stream=True,
    )

    # --- 异步 ---
    asyncio.run(run_async_collaboration())
