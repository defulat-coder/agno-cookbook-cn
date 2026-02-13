"""
Post Hook 输出处理示例
=============================

演示使用 post-hooks 进行输出验证的 Agno Agent 示例。
"""

import asyncio

from agno.agent import Agent
from agno.exceptions import CheckTrigger, OutputCheckError
from agno.models.openai import OpenAIChat
from agno.run.agent import RunOutput
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
class OutputValidationResult(BaseModel):
    is_complete: bool
    is_professional: bool
    is_safe: bool
    concerns: list[str]
    confidence_score: float


def validate_response_quality(run_output: RunOutput) -> None:
    """
    Post-hook：验证 Agent 响应的质量和安全性。

    此 hook 检查：
    - 响应完整性（不能太短或太模糊）
    - 专业语气和措辞
    - 内容的安全性和适当性

    如果验证失败则抛出 OutputCheckError。
    """

    # 跳过空响应的验证
    if not run_output.content or len(run_output.content.strip()) < 10:
        raise OutputCheckError(
            "Response is too short or empty",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )

    # 创建一个验证 Agent
    validator_agent = Agent(
        name="Output Validator",
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions=[
            "You are an output quality validator. Analyze responses for:",
            "1. COMPLETENESS: Response addresses the question thoroughly",
            "2. PROFESSIONALISM: Language is professional and appropriate",
            "3. SAFETY: Content is safe and doesn't contain harmful advice",
            "",
            "Provide a confidence score (0.0-1.0) for overall quality.",
            "List any specific concerns found.",
            "",
            "Be reasonable - don't reject good responses for minor issues.",
        ],
        output_schema=OutputValidationResult,
    )

    validation_result = validator_agent.run(
        input=f"Validate this response: '{run_output.content}'"
    )

    result = validation_result.content

    # 检查验证结果，如果失败则抛出错误
    if not result.is_complete:
        raise OutputCheckError(
            f"Response is incomplete. Concerns: {', '.join(result.concerns)}",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )

    if not result.is_professional:
        raise OutputCheckError(
            f"Response lacks professional tone. Concerns: {', '.join(result.concerns)}",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )

    if not result.is_safe:
        raise OutputCheckError(
            f"Response contains potentially unsafe content. Concerns: {', '.join(result.concerns)}",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )

    if result.confidence_score < 0.6:
        raise OutputCheckError(
            f"Response quality score too low ({result.confidence_score:.2f}). Concerns: {', '.join(result.concerns)}",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )


def simple_length_validation(run_output: RunOutput) -> None:
    """
    简单 post-hook：响应长度的基本验证。

    确保响应既不太短也不过长。
    """
    content = run_output.content.strip()

    if len(content) < 20:
        raise OutputCheckError(
            "Response is too brief to be helpful",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )

    if len(content) > 5000:
        raise OutputCheckError(
            "Response is too lengthy and may overwhelm the user",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )


async def main():
    """演示输出验证 post-hooks。"""
    print("Output Validation Post-Hook Example")
    print("=" * 60)

    # 带有综合输出验证的 Agent
    agent_with_validation = Agent(
        name="Customer Support Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        post_hooks=[validate_response_quality],
        instructions=[
            "You are a helpful customer support agent.",
            "Provide clear, professional responses to customer inquiries.",
            "Be concise but thorough in your explanations.",
        ],
    )

    # 只带有简单验证的 Agent
    agent_simple = Agent(
        name="Simple Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        post_hooks=[simple_length_validation],
        instructions=[
            "You are a helpful assistant. Keep responses focused and appropriate length."
        ],
    )

    # 测试 1：良好的响应（应通过验证）
    print("\n[TEST 1] Well-formed response")
    print("-" * 40)
    try:
        await agent_with_validation.aprint_response(
            input="How do I reset my password on my Microsoft account?"
        )
        print("[OK] Response passed validation")
    except OutputCheckError as e:
        print(f"[ERROR] Validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")

    # 测试 2：强制短响应（应该未通过简单验证）
    print("\n[TEST 2] Too brief response")
    print("-" * 40)
    try:
        # 使用更受限的指令来获得简短响应
        brief_agent = Agent(
            name="Brief Agent",
            model=OpenAIChat(id="gpt-4o-mini"),
            post_hooks=[simple_length_validation],
            instructions=["Answer in 1-2 words only."],
        )
        await brief_agent.aprint_response(input="What is the capital of France?")
    except OutputCheckError as e:
        print(f"[ERROR] Validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")

    # 测试 3：带有简单验证的正常响应
    print("\n[TEST 3] Normal response with simple validation")
    print("-" * 40)
    try:
        await agent_simple.aprint_response(
            input="Explain what a database is in simple terms."
        )
        print("[OK] Response passed simple validation")
    except OutputCheckError as e:
        print(f"[ERROR] Validation failed: {e}")
        print(f"   Trigger: {e.check_trigger}")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
