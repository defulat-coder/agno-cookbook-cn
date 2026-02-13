"""
支持团队
=============

Ace + Scout + Dash 协同处理传入的问题。团队领导将问题路由给合适的 Agent，
并生成准确、有据可查的回复。

测试:
    python -m teams.support.team
"""

from agents.ace import ace
from agents.dash import dash
from agents.scout import scout
from agno.models.openai import OpenAIResponses
from agno.team.team import Team
from db import get_postgres_db

# ---------------------------------------------------------------------------
# 团队
# ---------------------------------------------------------------------------
support_team = Team(
    id="support-team",
    name="Support Team",
    model=OpenAIResponses(id="gpt-5.2"),
    db=get_postgres_db(contents_table="support_team_contents"),
    members=[ace, scout, dash],
    respond_directly=True,
    instructions=[
        "你领导一个支持团队，通过将传入的问题路由给合适的专家来处理：",
        "- Ace：回复 Agent。将需要撰写邮件、消息或对语气和风格有要求的回复任务路由到此。",
        "- Scout：企业知识库导航 Agent。将关于内部文档、政策、运维手册、架构的问题路由到此。",
        "- Dash：数据分析 Agent。将数据问题、SQL 查询、指标和分析任务路由到此。",
        "",
        "路由规则：",
        "- 数据/指标/SQL 问题 -> Dash",
        "- 内部知识/政策/文档问题 -> Scout",
        "- 撰写回复/邮件/消息 -> Ace",
        "- 如果不确定，事实性问题优先交给 Scout，沟通任务优先交给 Ace。",
        "- 如果问题需要多个 Agent 协作，交给最主要的那个。",
    ],
    show_members_responses=True,
    markdown=True,
    add_datetime_to_context=True,
)

if __name__ == "__main__":
    test_cases = [
        "What is our company's PTO policy?",
        "Draft a reply to this message: Thanks for the demo. "
        "Can we discuss pricing next week?",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Support team test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        support_team.print_response(prompt, stream=True)
