"""
直接响应路由团队
=============================

演示将多语言请求路由到专门成员并直接响应的功能。
"""

import asyncio

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建成员
# ---------------------------------------------------------------------------
english_agent = Agent(
    name="English Agent",
    role="You only answer in English",
    model=OpenAIChat(id="o3-mini"),
)
japanese_agent = Agent(
    name="Japanese Agent",
    role="You only answer in Japanese",
    model=OpenAIChat(id="o3-mini"),
)
chinese_agent = Agent(
    name="Chinese Agent",
    role="You only answer in Chinese",
    model=OpenAIChat(id="o3-mini"),
)
spanish_agent = Agent(
    name="Spanish Agent",
    role="You can only answer in Spanish",
    model=OpenAIChat(id="o3-mini"),
)
french_agent = Agent(
    name="French Agent",
    role="You can only answer in French",
    model=OpenAIChat(id="o3-mini"),
)
german_agent = Agent(
    name="German Agent",
    role="You can only answer in German",
    model=OpenAIChat(id="o3-mini"),
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
multi_language_team = Team(
    name="Multi Language Team",
    model=OpenAIChat("o3-mini"),
    respond_directly=True,
    members=[
        english_agent,
        spanish_agent,
        japanese_agent,
        french_agent,
        german_agent,
        chinese_agent,
    ],
    markdown=True,
    instructions=[
        "你是一个语言路由器，将问题引导到合适的语言 agent。",
        "如果用户使用的语言的 agent 不在团队成员中，用英语回复：",
        "'I can only answer in the following languages: English, Spanish, Japanese, French and German. Please ask your question in one of these languages.'",
        "在路由到 agent 之前，始终检查用户输入的语言。",
        "对于不支持的语言（如意大利语），用英语回复上述消息。",
    ],
    show_members_responses=True,
)


async def run_async_router() -> None:
    # 用所有支持的语言询问 "你好吗？"
    await multi_language_team.aprint_response(
        "How are you?",
        stream=True,  # 英语
    )

    await multi_language_team.aprint_response(
        "你好吗？",
        stream=True,  # 中文
    )

    await multi_language_team.aprint_response(
        "お元気ですか?",
        stream=True,  # 日语
    )

    await multi_language_team.aprint_response("Comment allez-vous?", stream=True)

    await multi_language_team.aprint_response(
        "Wie geht es Ihnen?",
        stream=True,  # 德语
    )

    await multi_language_team.aprint_response(
        "Come stai?",
        stream=True,  # 意大利语
    )


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- 同步 ---
    multi_language_team.print_response("How are you?", stream=True)

    # --- 异步 ---
    asyncio.run(run_async_router())
