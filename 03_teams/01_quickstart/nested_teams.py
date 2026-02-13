"""
嵌套团队
=============================

演示在更高级别的协调团队中使用团队作为成员。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
research_agent = Agent(
    name="Research Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    role="收集参考资料和源材料",
)

analysis_agent = Agent(
    name="Analysis Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    role="提取关键发现和影响",
)

writing_agent = Agent(
    name="Writing Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    role="起草精致的叙述性输出",
)

editing_agent = Agent(
    name="Editing Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    role="提高清晰度和结构",
)

research_team = Team(
    name="Research Team",
    members=[research_agent, analysis_agent],
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "收集相关信息并总结证据。",
        "突出关键要点和不确定性。",
    ],
)

writing_team = Team(
    name="Writing Team",
    members=[writing_agent, editing_agent],
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "根据提供的研究起草和完善最终输出。",
        "保持语言简洁并面向决策。",
    ],
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
parent_team = Team(
    name="Program Team",
    members=[research_team, writing_team],
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "协调嵌套团队以提供单一连贯的响应。",
        "首先向研究团队寻求证据，然后向写作团队寻求综合。",
    ],
    markdown=True,
    show_members_responses=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parent_team.print_response(
        "Prepare a one-page brief on adopting AI coding assistants in a startup engineering team.",
        stream=True,
    )
