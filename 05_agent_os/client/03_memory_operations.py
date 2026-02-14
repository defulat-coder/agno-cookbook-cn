"""
使用 AgentOSClient 进行记忆操作

此示例演示如何使用 AgentOSClient 管理用户记忆。

前置条件：
1. 启动一个带有 update_memory_on_run=True 的 agent 的 AgentOS 服务器
2. 运行此脚本：python 03_memory_operations.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def main():
    client = AgentOSClient(base_url="http://localhost:7777")
    user_id = "example-user"

    print("=" * 60)
    print("Memory Operations")
    print("=" * 60)

    # 创建记忆
    print("\n1. Creating a memory...")
    memory = await client.create_memory(
        memory="User prefers dark mode for all applications",
        user_id=user_id,
        topics=["preferences", "ui"],
    )
    print(f"   Created memory: {memory.memory_id}")
    print(f"   Content: {memory.memory}")
    print(f"   Topics: {memory.topics}")

    # 列出用户的记忆
    print("\n2. Listing memories...")
    memories = await client.list_memories(user_id=user_id)
    print(f"   Found {len(memories.data)} memories for user {user_id}")
    for mem in memories.data:
        print(f"   - {mem.memory_id}: {mem.memory[:50]}...")

    # 获取特定记忆
    print(f"\n3. Getting memory {memory.memory_id}...")
    retrieved = await client.get_memory(memory.memory_id, user_id=user_id)
    print(f"   Memory: {retrieved.memory}")

    # 更新记忆
    print("\n4. Updating memory...")
    updated = await client.update_memory(
        memory_id=memory.memory_id,
        memory="User strongly prefers dark mode for all applications and websites",
        user_id=user_id,
        topics=["preferences", "ui", "accessibility"],
    )
    print(f"   Updated memory: {updated.memory}")
    print(f"   Updated topics: {updated.topics}")

    # 获取记忆主题（可选 - 如果不支持可能会失败）
    print("\n5. Getting all memory topics...")
    try:
        topics = await client.get_memory_topics()
        print(f"   Topics: {topics}")
    except Exception as e:
        print(f"   Skipped (endpoint may not be available): {type(e).__name__}")

    # 获取用户记忆统计（可选 - 如果不支持可能会失败）
    print("\n6. Getting user memory stats...")
    try:
        stats = await client.get_user_memory_stats()
        print(f"   Stats: {len(stats.data)} entries")
    except Exception as e:
        print(f"   Skipped (endpoint may not be available): {type(e).__name__}")

    # 删除记忆
    print(f"\n7. Deleting memory {memory.memory_id}...")
    await client.delete_memory(memory.memory_id, user_id=user_id)
    print("   Memory deleted")

    # 验证删除
    print("\n8. Verifying deletion...")
    memories_after = await client.list_memories(user_id=user_id)
    print(f"   Remaining memories: {len(memories_after.data)}")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
