"""
个人身份信息检测
=============================

演示如何在 Agno Agent 中使用个人身份信息（PII）检测护栏。
"""

import asyncio
import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.exceptions import InputCheckError
from agno.guardrails import PIIDetectionGuardrail
from agno.models.openai import OpenAILike

load_dotenv()


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
async def main():
    """演示 PII 检测护栏功能。"""
    print("PII 检测护栏演示")
    print("=" * 50)

    # 创建一个带有 PII 检测防护的 agent
    agent = Agent(
        name="隐私保护 Agent",
        model=OpenAILike(
            id=os.getenv("MODEL_ID", "GLM-4.7"),
            base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
            api_key=os.getenv("MODEL_API_KEY"),
        ),
        pre_hooks=[PIIDetectionGuardrail()],
        description="在保护隐私的同时提供客服帮助的 Agent。",
        instructions="你是一个有帮助的客服助手。请始终保护用户隐私并妥善处理敏感信息。",
    )

    # 测试 1：无 PII 的正常请求（应该通过）
    print("\n[测试 1] 无 PII 的正常请求")
    print("-" * 30)
    try:
        agent.print_response(
            input="你能帮我了解一下你们的退换货政策吗？",
        )
        print("[成功] 正常请求处理成功")
    except InputCheckError as e:
        print(f"[错误] 意外错误：{e}")

    # 测试 2：包含社会安全号码的请求（应该被拦截）
    print("\n[测试 2] 包含社会安全号码的输入")
    print("-" * 30)
    try:
        agent.print_response(
            input="你好，我的社会保障号是 123-45-6789。能帮我处理账户问题吗？",
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
            input="我想更新支付方式。新卡号是 4532 1234 5678 9012。",
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
            input="请将最近购买的收据发送到 john.doe@example.com。",
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
            input="我的电话号码是 555-123-4567。请致电告知我的订单状态。",
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
            input="你好，我是 John Smith。邮箱是 john@company.com，电话 555.987.6543。需要帮忙处理账户。",
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
            input="能帮我核实一下尾号为 4532123456789012 的信用卡吗？",
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
        name="隐私保护 Agent（掩码模式）",
        model=OpenAILike(
            id=os.getenv("MODEL_ID", "GLM-4.7"),
            base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
            api_key=os.getenv("MODEL_API_KEY"),
        ),
        pre_hooks=[PIIDetectionGuardrail(mask_pii=True)],
        description="在保护隐私的同时提供客服帮助的 Agent。",
        instructions="你是一个有帮助的客服助手。请始终保护用户隐私并妥善处理敏感信息。",
    )

    # 测试 8：包含社会安全号码的请求（应该被掩码）
    print("\n[测试 8] 包含社会安全号码的输入（掩码模式）")
    print("-" * 30)
    agent.print_response(
        input="你好，我的社会保障号是 123-45-6789。能帮我处理账户问题吗？",
    )


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
