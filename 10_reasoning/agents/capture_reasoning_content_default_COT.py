"""
捕获推理内容
=========================

演示如何在流式和非流式运行中检查 reasoning_content。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------
def print_reasoning_content(response, label: str) -> None:
    """打印运行响应中 reasoning_content 的简短报告。"""
    print(f"\n--- 来自 {label} 的 reasoning_content ---")
    if hasattr(response, "reasoning_content") and response.reasoning_content:
        print("[OK] reasoning_content 已找到")
        print(f"   长度：{len(response.reasoning_content)} 个字符")
        print("\n=== reasoning_content 预览 ===")
        preview = response.reasoning_content[:1000]
        if len(response.reasoning_content) > 1000:
            preview += "..."
        print(preview)
    else:
        print("[未找到] reasoning_content 不存在")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
def run_examples() -> None:
    print("\n=== 示例 1：使用 reasoning=True（默认思维链） ===\n")

    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        reasoning=True,
        markdown=True,
    )

    print("使用 reasoning=True 运行（非流式）...")
    response = agent.run("前 10 个自然数之和是多少？")
    print_reasoning_content(response, label="非流式响应")

    print("\n\n=== 示例 2：使用自定义 reasoning_model ===\n")

    agent_with_reasoning_model = Agent(
        model=OpenAIChat(id="gpt-4o"),
        reasoning_model=OpenAIChat(id="gpt-4o"),
        markdown=True,
    )

    print("使用指定 reasoning_model 运行（非流式）...")
    response = agent_with_reasoning_model.run(
        "前 10 个自然数之和是多少？"
    )
    print_reasoning_content(response, label="非流式响应")

    print("\n\n=== 示例 3：使用 reasoning=True 处理流式输出 ===\n")

    streaming_agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        reasoning=True,
        markdown=True,
    )

    print("使用 reasoning=True 运行（流式）...")
    final_response = None
    for event in streaming_agent.run(
        "5! （阶乘）的值是多少？",
        stream=True,
        stream_events=True,
    ):
        if hasattr(event, "content") and event.content:
            print(event.content, end="", flush=True)

        if hasattr(event, "reasoning_content"):
            final_response = event

    print_reasoning_content(final_response, label="最终流式事件")

    print("\n\n=== 示例 4：使用 reasoning_model 处理流式输出 ===\n")

    streaming_agent_with_model = Agent(
        model=OpenAIChat(id="gpt-4o"),
        reasoning_model=OpenAIChat(id="gpt-4o"),
        markdown=True,
    )

    print("使用指定 reasoning_model 运行（流式）...")
    final_response_with_model = None
    for event in streaming_agent_with_model.run(
        "7! （阶乘）的值是多少？",
        stream=True,
        stream_events=True,
    ):
        if hasattr(event, "content") and event.content:
            print(event.content, end="", flush=True)

        if hasattr(event, "reasoning_content"):
            final_response_with_model = event

    print_reasoning_content(
        final_response_with_model,
        label="最终流式事件（reasoning_model）",
    )


if __name__ == "__main__":
    run_examples()
