"""
捕获推理内容 - 推理工具
=========================================

演示推理 Cookbook 示例。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.reasoning import ReasoningTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    """测试函数，验证 RunOutput 中的 reasoning_content 是否被正确填充。"""
    print("\n=== 测试 reasoning_content 生成 ===\n")

    # 创建带有 ReasoningTools 的 Agent
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=dedent("""\
            你是一位拥有强大分析能力的专业问题解决助手！请使用逐步推理来解决问题。
            \
        """),
    )

    # 测试 1：非流式模式
    print("使用 stream=False 运行...")
    response = agent.run(
        "前 10 个自然数之和是多少？", stream=False
    )

    # 检查 reasoning_content
    if hasattr(response, "reasoning_content") and response.reasoning_content:
        print("[OK] 非流式响应中找到 reasoning_content")
        print(f"   长度：{len(response.reasoning_content)} 个字符")
        print("\n=== reasoning_content 预览（非流式） ===")
        preview = response.reasoning_content[:1000]
        if len(response.reasoning_content) > 1000:
            preview += "..."
        print(preview)
    else:
        print("[未找到] 非流式响应中不存在 reasoning_content")

    # 处理流式响应以查找最终响应
    print("\n\n=== 测试 2：处理流式输出以找到最终响应 ===\n")

    # 创建另一个新的 Agent
    streaming_agent_alt = Agent(
        model=OpenAIChat(id="gpt-4o"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=dedent("""\
            你是一位拥有强大分析能力的专业问题解决助手！请使用逐步推理来解决问题。
            \
        """),
    )

    # 处理流式响应并查找最终的 RunOutput
    final_response = None
    for event in streaming_agent_alt.run(
        "3!（阶乘）的值是多少？",
        stream=True,
        stream_events=True,
    ):
        # 流中的最终事件应该是 RunOutput 对象
        if hasattr(event, "reasoning_content"):
            final_response = event

    print("--- 检查最终流式事件中的 reasoning_content ---")
    if (
        final_response
        and hasattr(final_response, "reasoning_content")
        and final_response.reasoning_content
    ):
        print("[OK] 最终流式事件中找到 reasoning_content")
        print(f"   长度：{len(final_response.reasoning_content)} 个字符")
        print("\n=== reasoning_content 预览（最终流式事件） ===")
        preview = final_response.reasoning_content[:1000]
        if len(final_response.reasoning_content) > 1000:
            preview += "..."
        print(preview)
    else:
        print("[未找到] 最终流式事件中不存在 reasoning_content")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
