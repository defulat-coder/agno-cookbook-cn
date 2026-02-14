"""
使用 A2AClient 进行错误处理

此示例演示在使用 A2A 协议时如何处理各种错误场景。

前置条件：
1. 启动带有 A2A 接口的 AgentOS 服务器：
   python cookbook/06_agent_os/client_a2a/servers/agno_server.py

2. 运行此脚本：
   python cookbook/06_agent_os/client_a2a/04_error_handling.py
"""

import asyncio

from agno.client.a2a import A2AClient
from agno.exceptions import RemoteServerUnavailableError
from httpx import HTTPStatusError

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def handle_http_error():
    """处理 agent 不存在的情况（404）。"""
    print("=" * 60)
    print("Handling HTTP Errors (e.g., Agent Not Found)")
    print("=" * 60)

    client = A2AClient("http://localhost:7003/a2a/agents/nonexistent-agent")
    try:
        await client.send_message(
            message="Hello",
        )
    except HTTPStatusError as e:
        print(f"\nHTTP Error: {e.response.status_code}")
        print(f"Detail: {e.response.text[:100]}...")
        print("Suggestion: Check if the agent exists on the server")


async def handle_connection_error():
    """处理服务器无法访问的情况。"""
    print("\n" + "=" * 60)
    print("Handling Connection Error")
    print("=" * 60)

    # 尝试连接到不存在的服务器
    client = A2AClient("http://localhost:9999/a2a/agents/any-agent")
    try:
        await client.send_message(
            message="Hello",
        )
    except RemoteServerUnavailableError as e:
        print(f"\nConnection failed: {e.message}")
        print(f"Server URL: {e.base_url}")
        print("Suggestion: Check if the A2A server is running")


async def handle_timeout():
    """处理请求超时。"""
    print("\n" + "=" * 60)
    print("Handling Timeout")
    print("=" * 60)

    # 使用非常短的超时
    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent", timeout=0.001)
    try:
        await client.send_message(
            message="This might timeout",
        )
    except RemoteServerUnavailableError as e:
        print(f"\nRequest failed: {e.message}")
        print("Suggestion: Increase timeout or check server performance")


async def comprehensive_error_handling():
    """演示全面的错误处理模式。"""
    print("\n" + "=" * 60)
    print("Comprehensive Error Handling Pattern")
    print("=" * 60)

    async def safe_send_message(client, message: str):
        """安全地发送消息并进行适当的错误处理。"""
        try:
            result = await client.send_message(
                message=message,
            )

            # 检查任务在应用程序级别是否失败
            if result.is_failed:
                print(f"Error: Task failed - {result.content}")
                return None

            return result

        except HTTPStatusError as e:
            print(f"Error: HTTP {e.response.status_code}")
            return None

        except RemoteServerUnavailableError as e:
            print(f"Error: Server unavailable - {e.message}")
            return None

    client = A2AClient("http://localhost:7003/a2a/agents/basic-agent")

    print("\nTrying valid agent...")
    result = await safe_send_message(client, "Hello!")
    if result:
        print(f"Success: {result.content[:50]}...")

    client = A2AClient("http://localhost:7003/a2a/agents/invalid-agent")
    print("\nTrying invalid agent...")
    result = await safe_send_message(client, "Hello!")
    if result:
        print(f"Success: {result.content}")


async def main():
    await handle_http_error()
    await handle_connection_error()
    await handle_timeout()
    await comprehensive_error_handling()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
