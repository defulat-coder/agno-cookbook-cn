"""
演示如何连接到远程 Agno A2A agent 的示例。

此示例展示如何使用 RemoteAgent 与 A2A 协议来连接
通过 A2A 接口暴露的 Agno agent。

前置条件：
1. 启动 Agno A2A 服务器：
   python cookbook/06_agent_os/remote/agno_a2a_server.py

   服务器将在 http://localhost:7779 上运行

2. 设置你的 OPENAI_API_KEY 环境变量
"""

import asyncio

from agno.agent import RemoteAgent

# ---------------------------------------------------------------------------
# Create Example
# ---------------------------------------------------------------------------


async def remote_agno_a2a_agent_example():
    """调用通过 A2A 接口暴露的远程 Agno agent。"""
    # 连接到远程 Agno A2A agent
    # protocol="a2a" 告诉 RemoteAgent 使用 A2A 协议
    # a2a_protocol="rest" 使用 REST API（Agno A2A 服务器的默认设置）
    agent = RemoteAgent(
        base_url="http://localhost:7779/a2a/agents/assistant-agent-2",
        agent_id="assistant-agent-2",  # 来自 A2A 服务器的 Agent ID
        protocol="a2a",
        a2a_protocol="rest",
    )

    print("正在调用远程 Agno A2A agent...")
    response = await agent.arun(
        "What is 15 * 23? Use the calculator tool.",
        user_id="user-123",
        session_id="session-456",
    )
    print(f"Response: {response.content}")


async def remote_agno_a2a_streaming_example():
    """从远程 Agno A2A agent 流式传输响应。"""
    agent = RemoteAgent(
        base_url="http://localhost:7779/a2a/agents/researcher-agent-2",
        agent_id="researcher-agent-2",
        protocol="a2a",
        a2a_protocol="rest",
    )

    print("\n正在从远程 Agno A2A agent 流式传输响应...")
    async for chunk in agent.arun(
        "Tell me a brief 2-sentence story about space exploration",
        session_id="session-456",
        user_id="user-123",
        stream=True,
        stream_events=True,
    ):
        if hasattr(chunk, "content") and chunk.content:
            print(chunk.content, end="", flush=True)
    print()  # 流式传输后换行


async def remote_agno_a2a_agent_info_example():
    """获取有关远程 Agno A2A agent 的信息。"""
    agent = RemoteAgent(
        base_url="http://localhost:7779/a2a/agents/assistant-agent-2",
        agent_id="assistant-agent-2",
        protocol="a2a",
        a2a_protocol="rest",
    )

    print("\n正在获取 agent 信息...")
    config = await agent.get_agent_config()
    print(f"Agent ID: {config.id}")
    print(f"Agent Name: {config.name}")
    print(f"Agent Description: {config.description}")


async def main():
    """在单个事件循环中运行所有示例。"""
    print("=" * 60)
    print("远程 Agno A2A Agent 示例")
    print("=" * 60)
    print("\n注意：确保 Agno A2A 服务器在端口 7779 上运行")
    print("使用以下命令启动：python cookbook/06_agent_os/remote/agno_a2a_server.py\n")

    # 运行示例
    print("1. 远程 Agno A2A Agent 示例：")
    await remote_agno_a2a_agent_example()

    print("\n2. 远程 Agno A2A 流式传输示例：")
    await remote_agno_a2a_streaming_example()

    print("\n3. 远程 Agno A2A Agent 信息示例：")
    await remote_agno_a2a_agent_info_example()


# ---------------------------------------------------------------------------
# Run Example
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
