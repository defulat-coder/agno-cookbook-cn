"""
基础路由模式示例

演示 `mode=route` 模式，团队领导者将每个请求路由到
单个专家 agent 并直接返回他们的响应（无需综合）。

这对于语言路由、域分派或任何场景都非常理想
一个专家应该处理整个请求。

"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.team.mode import TeamMode
from agno.team.team import Team

# -- 特定语言 agent ------------------------------------------------

english_agent = Agent(
    name="English Agent",
    role="仅用英语回复",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=["始终用英语回复，无论输入语言是什么。"],
)

spanish_agent = Agent(
    name="Spanish Agent",
    role="仅用西班牙语回复",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=["始终用西班牙语回复，无论输入语言是什么。"],
)

french_agent = Agent(
    name="French Agent",
    role="仅用法语回复",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=["始终用法语回复，无论输入语言是什么。"],
)

# -- 路由团队 --------------------------------------------------------------

team = Team(
    name="Language Router",
    mode=TeamMode.route,
    model=OpenAIResponses(id="gpt-5.2"),
    members=[english_agent, spanish_agent, french_agent],
    instructions=[
        "你是一个语言路由器。",
        "检测用户消息的语言并路由到匹配的 agent。",
        "如果不支持该语言，默认使用英语 Agent。",
    ],
    show_members_responses=True,
    markdown=True,
)

# -- 运行 ---------------------------------------------------------------------

if __name__ == "__main__":
    # 英语
    team.print_response("What is the capital of France?", stream=True)

    print("\n" + "=" * 60 + "\n")

    # 西班牙语
    team.print_response("Cual es la capital de Francia?", stream=True)

    print("\n" + "=" * 60 + "\n")

    # 法语
    team.print_response("Quelle est la capitale de la France?", stream=True)
