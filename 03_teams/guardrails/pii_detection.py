"""
PII 检测
=============================

演示团队输入保护的 PII 检测护栏。
"""

from agno.exceptions import InputCheckError
from agno.guardrails import PIIDetectionGuardrail
from agno.models.openai import OpenAIChat
from agno.team import Team

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
blocking_team = Team(
    name="Privacy-Protected Team",
    members=[],
    model=OpenAIChat(id="gpt-5.2"),
    pre_hooks=[PIIDetectionGuardrail()],
    description="在保护隐私的同时帮助客户服务的团队。",
    instructions="你是一个有用的客户服务助手。始终保护用户隐私并适当处理敏感信息。",
)

masked_team = Team(
    name="Privacy-Protected Team",
    members=[],
    model=OpenAIChat(id="gpt-5.2"),
    pre_hooks=[PIIDetectionGuardrail(mask_pii=True)],
    description="在保护隐私的同时帮助客户服务的团队。",
    instructions="你是一个有用的客户服务助手。始终保护用户隐私并适当处理敏感信息。",
)


# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
def main() -> None:
    """演示 PII 检测护栏功能。"""
    print("PII 检测护栏演示")
    print("=" * 50)

    print("\n[测试 1] 无 PII 的正常请求")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="Can you help me understand your return policy?",
        )
        print("[OK] Normal request processed successfully")
    except InputCheckError as e:
        print(f"[ERROR] Unexpected error: {e}")

    print("\n[TEST 2] Input containing SSN")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="Hi, my Social Security Number is 123-45-6789. Can you help me with my account?",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 3] Input containing credit card")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="I'd like to update my payment method. My new card number is 4532 1234 5678 9012.",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 4] Input containing email address")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="Please send the receipt to john.doe@example.com for my recent purchase.",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 5] Input containing phone number")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="My phone number is 555-123-4567. Please call me about my order status.",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 6] Multiple PII types in one request")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="Hi, I'm John Smith. My email is john@company.com and phone is 555.987.6543. I need help with my account.",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 7] PII with different formatting")
    print("-" * 30)
    try:
        blocking_team.print_response(
            input="Can you verify my credit card ending in 4532123456789012?",
        )
        print("[WARNING] This should have been blocked!")
    except InputCheckError as e:
        print(f"[BLOCKED] PII blocked: {e.message}")
        print(f"   Trigger: {e.check_trigger}")

    print("\n[TEST 8] Input containing SSN (masked mode)")
    print("-" * 30)
    masked_team.print_response(
        input="Hi, my Social Security Number is 123-45-6789. Can you help me with my account?",
    )


if __name__ == "__main__":
    main()
