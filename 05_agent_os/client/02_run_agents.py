"""
使用 AgentOSClient 运行 Agent

此示例演示如何使用 AgentOSClient 执行 agent 运行，
包括流式和非流式响应。

前置条件：
1. 启动一个带有 agent 的 AgentOS 服务器
2. 运行此脚本：python 02_run_agents.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def run_agent_non_streaming():
    """执行非流式 agent 运行。"""
    print("=" * 60)
    print("Non-Streaming Agent Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")
    # 获取可用的 agent
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    print(f"Running agent: {agent_id}")

    # 执行 agent
    result = await client.run_agent(
        agent_id=agent_id,
        message="What is 2 + 2? Explain your answer briefly.",
    )

    print(f"\nRun ID: {result.run_id}")
    print(f"Content: {result.content}")
    print(f"Tokens: {result.metrics.total_tokens if result.metrics else 'N/A'}")


async def run_agent_streaming():
    """执行流式 agent 运行。"""
    print("\n" + "=" * 60)
    print("Streaming Agent Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的 agent
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    print(f"Streaming from agent: {agent_id}")
    print("\nResponse: ", end="", flush=True)

    from agno.run.agent import RunCompletedEvent, RunContentEvent

    full_content = ""
    async for event in client.run_agent_stream(
        agent_id=agent_id,
        message="Tell me a short joke.",
    ):
        # 处理不同的事件类型
        if isinstance(event, RunContentEvent):
            print(event.content, end="", flush=True)
            full_content += event.content
        elif isinstance(event, RunCompletedEvent):
            # 运行完成 - 如果需要，可以在这里访问 event.run_id
            pass

    print("\n")


async def main():
    await run_agent_non_streaming()
    await run_agent_streaming()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
