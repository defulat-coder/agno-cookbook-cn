"""
团队输入和输出 Schema
=============================

演示使用输入和输出 schema 的 AgentOS 团队。
"""

from typing import List

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
input_schema_db = SqliteDb(
    session_table="team_session",
    db_file="tmp/team.db",
)

output_schema_db = SqliteDb(
    session_table="research_team_sessions",
    db_file="tmp/team_output_schema.db",
)


class ResearchProject(BaseModel):
    """具有验证要求的结构化研究项目。"""

    project_name: str = Field(description="Name of the research project")
    research_topics: List[str] = Field(
        description="List of topics to research", min_length=1
    )
    target_audience: str = Field(description="Intended audience for the research")
    depth_level: str = Field(
        description="Research depth level", pattern="^(basic|intermediate|advanced)$"
    )
    max_sources: int = Field(description="Maximum number of sources to use", default=10)
    include_recent_only: bool = Field(
        description="Whether to focus only on recent sources", default=True
    )


class ResearchReport(BaseModel):
    """结构化的研究报告输出。"""

    topic: str = Field(..., description="Research topic")
    summary: str = Field(..., description="Executive summary")
    key_findings: List[str] = Field(..., description="Key findings")
    recommendations: List[str] = Field(..., description="Action recommendations")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
hackernews_agent = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat(id="o3-mini"),
    tools=[HackerNewsTools()],
    role="Research trending topics and discussions on HackerNews",
    instructions=[
        "搜索相关的讨论和文章",
        "专注于高质量、高参与度的帖子",
        "提取关键见解和技术细节",
    ],
    db=input_schema_db,
)

web_researcher = Agent(
    name="Web Researcher",
    model=OpenAIChat(id="o3-mini"),
    tools=[WebSearchTools()],
    role="Conduct comprehensive web research",
    instructions=[
        "搜索权威来源和文档",
        "查找最新文章和博客文章",
        "收集主题的多样化观点",
    ],
)

researcher = Agent(
    name="Researcher",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    role="Conduct thorough research on assigned topics",
)

analyst = Agent(
    name="Analyst",
    model=OpenAIChat(id="gpt-4o-mini"),
    role="Analyze research findings and provide recommendations",
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
research_team_with_input_schema = Team(
    name="Research Team with Input Validation",
    model=OpenAIChat(id="o3-mini"),
    members=[hackernews_agent, web_researcher],
    delegate_to_all_members=True,
    input_schema=ResearchProject,
    instructions=[
        "根据验证的输入进行彻底研究",
        "协调团队成员之间的工作以避免重复",
        "确保研究深度与指定级别匹配",
        "遵守最大来源限制",
        "如果请求，专注于最新来源",
    ],
)

research_team_with_output_schema = Team(
    name="Research Team",
    id="research-team",
    model=OpenAIChat(id="gpt-4o-mini"),
    members=[researcher, analyst],
    output_schema=ResearchReport,
    markdown=False,
    db=output_schema_db,
)

# ---------------------------------------------------------------------------
# 创建 AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="team-schemas-demo",
    teams=[research_team_with_input_schema, research_team_with_output_schema],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="team_schemas:app", port=7777, reload=True)
