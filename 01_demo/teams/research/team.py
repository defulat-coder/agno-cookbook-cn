"""
研究团队
==============

Seek + Scout + Dex 协同完成深度研究任务。团队领导协调三个 Agent，
从外部资料、内部知识库和人脉关系中生成全面的研究报告。

测试:
    python -m teams.research.team
"""

from agents.dex import dex
from agents.scout import scout
from agents.seek import seek
from agno.models.openai import OpenAIResponses
from agno.team.team import Team
from db import get_postgres_db

# ---------------------------------------------------------------------------
# 团队
# ---------------------------------------------------------------------------
research_team = Team(
    id="research-team",
    name="Research Team",
    model=OpenAIResponses(id="gpt-5.2"),
    db=get_postgres_db(contents_table="research_team_contents"),
    members=[seek, scout, dex],
    instructions=[
        "你领导一个拥有三位专家的研究团队：",
        "- Seek：深度网络研究员。用于外部调研、公司分析和主题深入研究。",
        "- Scout：企业知识库导航员。用于在内部文档和知识库中查找信息。",
        "- Dex：人脉情报专家。用于人物调研、构建画像和人际关系背景分析。",
        "",
        "对于研究任务：",
        "1. 将研究问题分解为多个维度（外部事实、内部知识、人脉/关系）",
        "2. 将每个维度委派给相应的专家",
        "3. 将各专家的发现综合为一份全面、结构清晰的报告",
        "4. 交叉对照各 Agent 的发现，识别规律和矛盾之处",
        "",
        "始终生成结构化报告，包含：",
        "- 执行摘要",
        "- 关键发现（按维度组织）",
        "- 信息来源和置信度",
        "- 待解决问题和建议的后续步骤",
    ],
    show_members_responses=True,
    markdown=True,
    add_datetime_to_context=True,
)

if __name__ == "__main__":
    test_cases = [
        "Research Anthropic - the AI company. What do we know about them, "
        "their products, key people, and recent developments?",
        "Research OpenAI and summarize products, key people, and recent enterprise moves.",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Research team test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        research_team.print_response(prompt, stream=True)
