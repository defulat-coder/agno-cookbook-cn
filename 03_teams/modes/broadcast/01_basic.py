"""
基础广播模式示例

演示 `mode=broadcast` 模式，团队领导者同时将相同任务
发送给所有成员 agent，然后将他们的响应
综合为统一的答案。

这对于从多个角度看待单个问题非常理想。

"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 视角 agent ------------------------------------------------------

optimist = Agent(
    name="Optimist",
    role="关注机会和积极结果",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你看到每种情况的光明面。",
        "关注机会、增长潜力和积极趋势。",
        "要真诚 -- 不是盲目乐观 -- 但要强调好的方面。",
    ],
)

pessimist = Agent(
    name="Pessimist",
    role="关注风险和潜在的负面影响",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你关注风险、挑战和潜在陷阱。",
        "识别可能出错的地方以及为什么需要谨慎。",
        "要有建设性 -- 提出真正的担忧，而不是毫无根据的恐惧。",
    ],
)

realist = Agent(
    name="Realist",
    role="提供平衡、务实的分析",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你提供平衡的、基于证据的分析。",
        "客观地权衡机会和风险。",
        "根据当前数据关注最可能发生的事情。",
    ],
)

# -- 广播团队 ----------------------------------------------------------

team = Team(
    name="Multi-Perspective Team",
    mode=TeamMode.broadcast,
    model=OpenAIResponses(id="gpt-5.2"),
    members=[optimist, pessimist, realist],
    instructions=[
        "你领导一个多角度分析团队。",
        "所有成员收到相同的问题并独立回答。",
        "将他们的观点综合为一个平衡的摘要，捕捉",
        "关键机会、风险和最可能的结果。",
    ],
    show_members_responses=True,
    markdown=True,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    team.print_response(
        "Should a startup pivot from B2C to B2B in a crowded market?",
        stream=True,
    )
