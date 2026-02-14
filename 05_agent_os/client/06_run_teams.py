"""
使用 AgentOSClient 运行团队

此示例演示如何使用 AgentOSClient 执行团队运行，
包括流式和非流式响应。

前置条件：
1. 启动一个配置了团队的 AgentOS 服务器
2. 运行此脚本：python 06_run_teams.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def run_team_non_streaming():
    """执行非流式团队运行。"""
    print("=" * 60)
    print("Non-Streaming Team Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的团队
    config = await client.aget_config()
    if not config.teams:
        print("No teams available")
        return

    team_id = config.teams[0].id
    print(f"Running team: {team_id}")

    # 执行团队
    result = await client.run_team(
        team_id=team_id,
        message="What is the capital of France and what is 15 * 7?",
    )

    print(f"\nRun ID: {result.run_id}")
    print(f"Content: {result.content}")


async def run_team_streaming():
    """执行流式团队运行。"""
    print("\n" + "=" * 60)
    print("Streaming Team Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的团队
    config = await client.aget_config()
    if not config.teams:
        print("No teams available")
        return

    team_id = config.teams[0].id
    print(f"Streaming from team: {team_id}")
    print("\nResponse: ", end="", flush=True)

    from agno.run.team import RunCompletedEvent, RunContentEvent

    # 流式响应
    async for event in client.run_team_stream(
        team_id=team_id,
        message="Tell me about Python programming in 2 sentences.",
    ):
        # 处理不同的事件类型
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
        elif isinstance(event, RunCompletedEvent):
            # 运行完成 - 如果需要，可以在这里访问 event.run_id
            pass

    print("\n")


async def main():
    await run_team_non_streaming()
    await run_team_streaming()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
