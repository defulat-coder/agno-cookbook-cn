"""
Agent 输入和输出 Schema
==============================

演示使用输入和输出 schema 的 AgentOS agent。
"""

from typing import List

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.hackernews import HackerNewsTools
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
input_schema_db = SqliteDb(
    session_table="agent_session",
    db_file="tmp/agent.db",
)

output_schema_db = SqliteDb(
    session_table="movie_agent_sessions",
    db_file="tmp/agent_output_schema.db",
)


class ResearchTopic(BaseModel):
    """具有特定要求的结构化研究主题。"""

    topic: str
    focus_areas: List[str] = Field(description="Specific areas to focus on")
    target_audience: str = Field(description="Who this research is for")
    sources_required: int = Field(description="Number of sources needed", default=5)


class MovieScript(BaseModel):
    """结构化的电影剧本输出。"""

    title: str = Field(..., description="Movie title")
    genre: str = Field(..., description="Movie genre")
    logline: str = Field(..., description="One-sentence summary")
    main_characters: List[str] = Field(..., description="Main character names")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="Hackernews Agent",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[HackerNewsTools()],
    role="Extract key insights and content from Hackernews posts",
    input_schema=ResearchTopic,
    db=input_schema_db,
)

movie_agent = Agent(
    name="Movie Script Agent",
    id="movie-agent",
    model=OpenAIChat(id="gpt-5.2"),
    description="创建结构化输出 - 默认 MovieScript 格式，但可以被覆盖",
    output_schema=MovieScript,
    markdown=False,
    db=output_schema_db,
)

# ---------------------------------------------------------------------------
# 创建 AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="agent-schemas-demo",
    agents=[hackernews_agent, movie_agent],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="agent_schemas:app", port=7777, reload=True)
