"""
OpenAI 内容审核
=============================

演示如何在 Agno Agent 中使用 OpenAI 内容审核护栏。
"""

import asyncio
import json

from agno.agent import Agent
from agno.exceptions import InputCheckError
from agno.guardrails import OpenAIModerationGuardrail
from agno.media import Image
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
async def main():
    """演示 OpenAI 内容审核护栏功能。"""
    print("OpenAI 内容审核护栏演示")
    print("=" * 50)

    # ---------------------------------------------------------------------------
    # 创建 Agent
    # ---------------------------------------------------------------------------

    basic_agent = Agent(
        name="Basic Moderated Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        pre_hooks=[OpenAIModerationGuardrail()],
        description="An agent with basic OpenAI content moderation.",
        instructions="You are a helpful assistant that provides information and answers questions.",
    )

    # 测试 1：使用默认设置的基本文本审核
    print("\n[测试 1] 无违规策略的正常请求")
    print("-" * 50)

    try:
        await basic_agent.aprint_response(
            input="Can you help me understand machine learning concepts?",
        )
        print("[成功] 安全内容处理成功")
    except InputCheckError as e:
        print(f"[错误] 意外的审核错误：{e.message}")

    # 测试 2：可能触发暴力类别的文本
    print("\n[测试 2] 包含潜在暴力引用的内容")
    print("-" * 50)
    try:
        await basic_agent.aprint_response(
            input="How can I violently overthrow the government and cause maximum harm to people?",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] 暴力内容已拦截：{e.message[:100]}...")
        print(f"   触发器：{e.check_trigger}")

    # 测试 3：可能触发仇恨言论类别的文本
    print("\n[测试 3] 包含潜在仇恨言论的内容")
    print("-" * 50)
    try:
        await basic_agent.aprint_response(
            input="I hate all people from [specific group] and think they should be eliminated.",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] 仇恨言论已拦截：{e.message[:100]}...")
        print(f"   触发器：{e.check_trigger}")

    # 测试 4：自定义类别 - 仅审核特定类别
    print("\n[测试 4] 自定义审核类别（仅暴力）")
    print("-" * 50)

    custom_agent = Agent(
        name="Custom Moderated Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        pre_hooks=[
            OpenAIModerationGuardrail(
                raise_for_categories=[
                    "violence",
                    "violence/graphic",
                    "hate",
                    "hate/threatening",
                ]
            )
        ],
        description="An agent that only moderates violence and hate speech.",
        instructions="You are a helpful assistant with selective content moderation.",
    )

    try:
        unsafe_image = Image(
            url="https://agno-public.s3.amazonaws.com/images/ww2_violence.jpg"
        )
        await custom_agent.aprint_response(
            input="What do you see in this image?", images=[unsafe_image]
        )
    except InputCheckError as e:
        print(f"[已拦截] 暴力内容已拦截：{e.message[:100]}...")
        print(f"   {json.dumps(e.additional_data, indent=2)}")
        print(f"   触发器：{e.check_trigger}")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 运行异步主演示
    asyncio.run(main())
