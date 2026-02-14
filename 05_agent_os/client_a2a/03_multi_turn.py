"""
使用 A2AClient 进行多轮对话

此示例演示如何使用 A2A 协议在多条消息之间维护对话上下文。

前置条件：
1. 启动带有 A2A 接口的 AgentOS 服务器：
   python cookbook/06_agent_os/client_a2a/servers/agno_server.py

2. 运行此脚本：
   python cookbook/06_agent_os/client_a2a/03_multi_turn.py
"""

import asyncio

from agno.client.a2a import A2AClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def multi_turn_conversation():
    """演示带有上下文保留的多轮对话。"""
    print("=" * 60)
    print("Multi-Turn A2A Conversation")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")

    # 第一条消息 - 介绍自己
    print("\nUser: My name is Alice and I love Python programming.")
    result1 = await client.send_message(
        message="My name is Alice and I love Python programming.",
    )
    print(f"Agent: {result1.content}")

    # 获取用于后续消息的 context_id
    context_id = result1.context_id
    print(f"\n[Using context_id: {context_id}]")

    # 第二条消息 - 询问之前的上下文
    print("\nUser: What is my name?")
    result2 = await client.send_message(
        message="What is my name?",
        context_id=context_id,  # 传递 context_id
    )
    print(f"Agent: {result2.content}")

    # 第三条消息 - 继续对话
    print("\nUser: What do I love?")
    result3 = await client.send_message(
        message="What do I love?",
        context_id=context_id,
    )
    print(f"Agent: {result3.content}")


async def streaming_multi_turn():
    """带有流式响应的多轮对话。"""
    print("\n" + "=" * 60)
    print("Streaming Multi-Turn Conversation")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")
    context_id = None

    questions = [
        "I'm planning a trip to Japan.",
        "What's the best time to visit?",
        "Any must-see places?",
    ]

    for question in questions:
        print(f"\nUser: {question}")
        print("Agent: ", end="", flush=True)

        async for event in client.stream_message(
            message=question,
            context_id=context_id,
        ):
            if event.is_content and event.content:
                print(event.content, end="", flush=True)

            # 从第一个响应中捕获 context_id
            if event.context_id and not context_id:
                context_id = event.context_id

        print()  # 每个响应后换行


async def main():
    await multi_turn_conversation()
    await streaming_multi_turn()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
