"""
个人身份信息检测
=============================

演示如何在 Agno Agent 中使用个人身份信息（PII）检测护栏。
"""

import asyncio

from agno.agent import Agent
from agno.exceptions import InputCheckError
from agno.guardrails import PIIDetectionGuardrail
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
async def main():
    """演示 PII 检测护栏功能。"""
    print("PII 检测护栏演示")
    print("=" * 50)

    # 创建一个带有 PII 检测防护的 agent
    agent = Agent(
        name="Privacy-Protected Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        pre_hooks=[PIIDetectionGuardrail()],
        description="An agent that helps with customer service while protecting privacy.",
        instructions="You are a helpful customer service assistant. Always protect user privacy and handle sensitive information appropriately.",
    )

    # 测试 1：无 PII 的正常请求（应该通过）
    print("\n[测试 1] 无 PII 的正常请求")
    print("-" * 30)
    try:
        agent.print_response(
            input="Can you help me understand your return policy?",
        )
        print("[成功] 正常请求处理成功")
    except InputCheckError as e:
        print(f"[错误] 意外错误：{e}")

    # 测试 2：包含社会安全号码的请求（应该被拦截）
    print("\n[测试 2] 包含社会安全号码的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="Hi, my Social Security Number is 123-45-6789. Can you help me with my account?",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    # 测试 3：包含信用卡号的请求（应该被拦截）
    print("\n[测试 3] 包含信用卡号的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="I'd like to update my payment method. My new card number is 4532 1234 5678 9012.",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    # 测试 4：包含电子邮件地址的请求（应该被拦截）
    print("\n[测试 4] 包含电子邮件地址的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="Please send the receipt to john.doe@example.com for my recent purchase.",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    # 测试 5：包含电话号码的请求（应该被拦截）
    print("\n[测试 5] 包含电话号码的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="My phone number is 555-123-4567. Please call me about my order status.",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    # 测试 6：上下文中混合 PII（应该被拦截）
    print("\n[测试 6] 一个请求中包含多种 PII 类型")
    print("-" * 30)
    try:
        agent.print_response(
            input="Hi, I'm John Smith. My email is john@company.com and phone is 555.987.6543. I need help with my account.",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    # 测试 7：边缘情况 - 格式不同（仍应被拦截）
    print("\n[测试 7] 不同格式的 PII")
    print("-" * 30)
    try:
        agent.print_response(
            input="Can you verify my credit card ending in 4532123456789012?",
        )
        print("[警告] 这应该被拦截！")
    except InputCheckError as e:
        print(f"[已拦截] PII 已拦截：{e.message}")
        print(f"   触发器：{e.check_trigger}")

    print("\n" + "=" * 50)
    print("PII 检测演示完成")
    print("所有敏感信息已成功拦截！")

    # 创建一个 PII 检测 agent，它会对输入中的 PII 进行掩码处理
    agent = Agent(
        name="Privacy-Protected Agent (Masked)",
        model=OpenAIChat(id="gpt-4o-mini"),
        pre_hooks=[PIIDetectionGuardrail(mask_pii=True)],
        description="An agent that helps with customer service while protecting privacy.",
        instructions="You are a helpful customer service assistant. Always protect user privacy and handle sensitive information appropriately.",
    )

    # 测试 8：包含社会安全号码的请求（应该被掩码）
    print("\n[测试 8] 包含社会安全号码的输入（掩码模式）")
    print("-" * 30)
    agent.print_response(
        input="Hi, my Social Security Number is 123-45-6789. Can you help me with my account?",
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
