"""
缓存团队响应
=============================

演示团队领导者和成员响应的两层缓存。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Researcher",
    role="研究和收集信息",
    model=OpenAIChat(id="gpt-4o", cache_response=True),
)

writer = Agent(
    name="Writer",
    role="编写清晰且引人入胜的内容",
    model=OpenAIChat(id="gpt-4o", cache_response=True),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
content_team = Team(
    members=[researcher, writer],
    model=OpenAIChat(id="gpt-4o", cache_response=True),
    markdown=True,
    debug_mode=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    content_team.print_response(
        "Write a very very very explanation of caching in software"
    )
