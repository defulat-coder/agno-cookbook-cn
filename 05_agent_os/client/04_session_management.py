"""
使用 AgentOSClient 进行 Session 管理

此示例演示如何使用 AgentOSClient 管理 session。

前置条件：
1. 启动一个带有 agent 的 AgentOS 服务器
2. 运行此脚本：python 04_session_management.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的 agent
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    user_id = "example-user"

    print("=" * 60)
    print("Session Management")
    print("=" * 60)

    # 创建 session
    print("\n1. Creating a session...")
    session = await client.create_session(
        agent_id=agent_id,
        user_id=user_id,
        session_name="My Test Session",
    )
    print(f"   Session ID: {session.session_id}")
    print(f"   Session Name: {session.session_name}")

    # 列出 session
    print("\n2. Listing sessions...")
    sessions = await client.get_sessions(user_id=user_id)
    print(f"   Found {len(sessions.data)} sessions")
    for sess in sessions.data[:5]:  # 显示前 5 个
        print(f"   - {sess.session_id}: {sess.session_name or 'Unnamed'}")

    # 获取 session 详情
    print(f"\n3. Getting session {session.session_id}...")
    details = await client.get_session(session.session_id)
    print(f"   Agent ID: {details.agent_id}")
    print(f"   User ID: {details.user_id}")
    print(
        f"   Runs: {len(details.runs) if hasattr(details, 'runs') and details.runs else 0}"
    )

    # 在 session 中运行一些消息
    print("\n4. Running messages in session...")
    await client.run_agent(
        agent_id=agent_id,
        message="Hello!",
        session_id=session.session_id,
    )
    await client.run_agent(
        agent_id=agent_id,
        message="How are you?",
        session_id=session.session_id,
    )

    # 获取 session 运行
    print("\n5. Getting session runs...")
    runs = await client.get_session_runs(session_id=session.session_id)
    print(f"   Found {len(runs)} runs in session")
    for run in runs:
        content_preview = (
            (run.content[:50] + "...")
            if run.content and len(str(run.content)) > 50
            else run.content
        )
        print(f"   - {run.run_id}: {content_preview}")

    # 重命名 session
    print("\n6. Renaming session...")
    renamed = await client.rename_session(
        session_id=session.session_id,
        session_name="Renamed Test Session",
    )
    print(f"   New name: {renamed.session_name}")

    # 删除 session
    print(f"\n7. Deleting session {session.session_id}...")
    await client.delete_session(session.session_id)
    print("   Session deleted")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
