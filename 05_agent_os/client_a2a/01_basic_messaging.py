"""
使用 A2AClient 进行基础 A2A 消息传递

此示例演示使用 A2A 协议进行简单的消息发送和用户识别。

前置条件：
1. 启动带有 A2A 接口的 AgentOS 服务器：
   python cookbook/06_agent_os/client_a2a/servers/agno_server.py

2. 运行此脚本：
   python cookbook/06_agent_os/client_a2a/01_basic_messaging.py
"""

import asyncio

from agno.client.a2a import A2AClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def main():
    """发送带有用户识别的消息。"""
    print("=" * 60)
    print("A2A Messaging with User ID")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")
    result = await client.send_message(
        message="Remember my name is Alice.",
        user_id="alice-123",
    )

    print(f"\nTask ID: {result.task_id}")
    print(f"Context ID: {result.context_id}")
    print(f"Status: {result.status}")
    print(f"\nResponse: {result.content}")

    if result.is_completed:
        print("\nTask completed successfully!")
    elif result.is_failed:
        print("\nTask failed!")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
