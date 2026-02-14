"""
基础 AgentOSClient 示例

此示例演示如何使用 AgentOSClient 连接到
远程 AgentOS 实例并执行基本操作。

前置条件：
1. 启动一个 AgentOS 服务器：
   python -c "
   from agno.agent import Agent
   from agno.models.openai import OpenAIChat
   from agno.os import AgentOS

   agent = Agent(
       name='Assistant',
       model=OpenAIChat(id='gpt-5.2'),
       instructions='You are a helpful assistant.',
   )
   agent_os = AgentOS(agents=[agent])
   agent_os.serve()
   "

2. 运行此脚本：python 01_basic_client.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def main():
    # 使用异步上下文管理器连接到 AgentOS
    client = AgentOSClient(base_url="http://localhost:7777")
    # 获取 AgentOS 配置
    config = await client.aget_config()
    print(f"Connected to: {config.name or config.os_id}")
    print(f"Available agents: {[a.id for a in (config.agents or [])]}")
    print(f"Available teams: {[t.id for t in (config.teams or [])]}")
    print(f"Available workflows: {[w.id for w in (config.workflows or [])]}")

    # 获取特定 agent 的详细信息
    if config.agents:
        agent_id = config.agents[0].id
        agent = await client.aget_agent(agent_id)
        print("\nAgent Details:")
        print(f"  Name: {agent.name}")
        print(f"  Model: {agent.model}")
        print(f"  Tools: {len(agent.tools or [])}")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
