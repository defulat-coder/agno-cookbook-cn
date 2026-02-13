"""
基础协作模式示例

演示默认的 `mode=coordinate` 模式，团队领导者：
1. 分析用户的请求
2. 选择最合适的成员 agent
3. 为每个选定的成员制定特定任务
4. 将成员响应综合为最终答案

"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 成员 agent -----------------------------------------------------------

researcher = Agent(
    name="Researcher",
    role="研究专家，查找和总结信息",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你是一名研究专家。",
        "提供关于任何主题的清晰、事实性摘要。",
        "组织发现时要有结构并引用局限性。",
    ],
)

writer = Agent(
    name="Writer",
    role="内容作者，制作精美、引人入胜的文本",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你是一名熟练的内容作者。",
        "将原始信息转化为结构良好、可读的文本。",
        "使用标题、要点和清晰的散文。",
    ],
)

# -- 协作团队 ---------------------------------------------------------

team = Team(
    name="Research & Writing Team",
    mode=TeamMode.coordinate,
    model=OpenAIResponses(id="gpt-5.2"),
    members=[researcher, writer],
    instructions=[
        "你领导一个研究和写作团队。",
        "对于信息请求，首先让研究员收集事实，",
        "然后让作者将发现打磨成最终作品。",
        "将所有内容综合为一个连贯的响应。",
    ],
    show_members_responses=True,
    markdown=True,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    team.print_response(
        "Write a brief overview of how large language models are trained, "
        "covering pre-training, fine-tuning, and RLHF.",
        stream=True,
    )
