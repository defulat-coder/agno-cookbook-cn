"""
使用 A2AClient 进行流式 A2A 消息传递

此示例演示使用 A2A 协议进行实时流式响应。

前置条件：
1. 启动带有 A2A 接口的 AgentOS 服务器：
   python cookbook/06_agent_os/client_a2a/servers/agno_server.py

2. 运行此脚本：
   python cookbook/06_agent_os/client_a2a/02_streaming.py
"""

import asyncio

from agno.client.a2a import A2AClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def basic_streaming():
    """从 A2A agent 流式传输响应。"""
    print("=" * 60)
    print("Streaming A2A Response")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")
    print("\nStreaming response from agent...")
    print("\nResponse: ", end="", flush=True)

    async for event in client.stream_message(
        message="Tell me a short joke.",
    ):
        # 在内容到达时打印
        if event.is_content and event.content:
            print(event.content, end="", flush=True)


async def streaming_with_events():
    """使用详细事件跟踪进行流式传输。"""
    print("\n" + "=" * 60)
    print("Streaming with Event Details")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")
    print("\nEvent log:")

    content_buffer = []

    async for event in client.stream_message(
        message="What is Python?",
    ):
        if event.content:
            content_buffer.append(event.content)

        if event.is_final:
            print("\nFull response:")
            print("".join(content_buffer))


async def main():
    await basic_streaming()
    await streaming_with_events()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
