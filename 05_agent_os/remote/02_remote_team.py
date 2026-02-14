"""
演示 AgentOSRunner 进行远程执行的示例。

运行 `agent_os_setup.py` 以启动远程 AgentOS 实例。
"""

import asyncio

from agno.team import RemoteTeam

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def remote_agent_example():
    """调用托管在另一个 AgentOS 实例上的远程 agent。"""
    # 创建一个指向远程 agent 的 runner
    team = RemoteTeam(
        base_url="http://localhost:7778",
        team_id="research-team",
    )

    response = await team.arun(
        "What is the capital of France?",
        user_id="user-123",
        session_id="session-456",
    )
    print(response.content)


async def remote_streaming_example():
    """从远程 agent 流式传输响应。"""
    team = RemoteTeam(
        base_url="http://localhost:7778",
        team_id="research-team",
    )

    async for chunk in team.arun(
        "Tell me a 2 sentence horror story",
        session_id="session-456",
        user_id="user-123",
        stream=True,
    ):
        if hasattr(chunk, "content") and chunk.content:
            print(chunk.content, end="", flush=True)


async def main():
    """在单个事件循环中运行所有示例。"""
    print("=" * 60)
    print("RemoteTeam Examples")
    print("=" * 60)

    # 运行示例
    # 注意：远程示例需要运行中的 AgentOS 实例

    print("\n1. Remote Team Example:")
    await remote_agent_example()

    print("\n2. Remote Streaming Example:")
    await remote_streaming_example()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
