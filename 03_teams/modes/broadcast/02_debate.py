"""
结构化辩论的广播模式

演示广播模式用于具有
对立观点的 agent 之间的结构化辩论。团队领导者充当主持人，综合
双方的论点。

"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 辩论参与者 -----------------------------------------------------

proponent = Agent(
    name="Proponent",
    role="为命题辩护",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你为给定的命题辩护。",
        "提出强有力的、合乎逻辑的论点和支持证据。",
        "承认反驳论点，但解释为什么你的立场更强。",
        "清楚地组织你的论点：论点、支持要点、结论。",
    ],
)

opponent = Agent(
    name="Opponent",
    role="反对命题",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你反对给定的命题。",
        "提出强有力的、合乎逻辑的反驳论点和支持证据。",
        "针对最强的赞成论点并解释它们的弱点。",
        "清楚地组织你的论点：论点、反驳要点、结论。",
    ],
)

# -- 广播团队作为辩论主持人 --------------------------------------

team = Team(
    name="Debate Team",
    mode=TeamMode.broadcast,
    model=OpenAIResponses(id="gpt-5.2"),
    members=[proponent, opponent],
    instructions=[
        "你是一名辩论主持人。",
        "两位辩论者收到相同的命题并各自辩护。",
        "听完双方意见后，提供：",
        "1. 双方最强论点的摘要",
        "2. 一致的领域（如果有）",
        "3. 你对哪些论点最有说服力的评估及原因",
    ],
    show_members_responses=True,
    markdown=True,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    team.print_response(
        "Proposition: Remote work is better than in-office work for software teams.",
        stream=True,
    )
