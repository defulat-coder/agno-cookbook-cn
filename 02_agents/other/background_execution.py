"""
演示后台执行与轮询和取消的示例。

后台执行允许你启动一个 agent 运行，它会立即返回 PENDING 状态，
而实际工作在后台继续执行。然后你可以轮询完成状态或取消运行。

要求：
- 运行 PostgreSQL（./cookbook/scripts/run_pgvector.sh）
- 设置 OPENAI_API_KEY

使用方法：
    .venvs/demo/bin/python cookbook/02_agents/other/background_execution.py
"""

import asyncio

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.run.base import RunStatus

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    session_table="background_exec_sessions",
)


# ---------------------------------------------------------------------------
# 创建并运行后台示例
# ---------------------------------------------------------------------------


async def example_background_run_with_polling():
    """启动一个后台运行并轮询直到完成。"""
    print("=" * 60)
    print("示例 1：带轮询的后台运行")
    print("=" * 60)

    agent = Agent(
        name="BackgroundAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="在后台运行的 agent",
        db=db,
    )

    # 启动后台运行 — 立即返回 PENDING 状态
    run_output = await agent.arun(
        "法国的首都是什么？用一句话回答。",
        background=True,
    )

    print(f"Run ID: {run_output.run_id}")
    print(f"Session ID: {run_output.session_id}")
    print(f"Status: {run_output.status}")
    assert run_output.status == RunStatus.pending, (
        f"Expected PENDING, got {run_output.status}"
    )

    # 轮询完成状态
    print("\n轮询完成中...")
    for i in range(30):
        await asyncio.sleep(1)
        result = await agent.aget_run_output(
            run_id=run_output.run_id,
            session_id=run_output.session_id,
        )
        if result is None:
            print(f"  [{i + 1}s] 尚未在数据库中找到运行")
            continue

        print(f"  [{i + 1}s] 状态: {result.status}")

        if result.status == RunStatus.completed:
            print(f"\n完成！内容: {result.content}")
            break
        elif result.status == RunStatus.error:
            print(f"\n失败！内容: {result.content}")
            break
    else:
        print("\n等待完成超时")

    print()


async def example_cancel_background_run():
    """启动一个后台运行并在完成前取消它。"""
    print("=" * 60)
    print("示例 2：取消后台运行")
    print("=" * 60)

    agent = Agent(
        name="CancellableAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="可以取消运行的 agent",
        db=db,
    )

    # 启动一个长时间的后台运行
    run_output = await agent.arun(
        "写一篇关于计算机历史的非常详细的文章。"
        "至少 5000 字，包含章节和小节。",
        background=True,
    )

    print(f"Run ID: {run_output.run_id}")
    print(f"状态: {run_output.status}")

    # 等待一会儿让运行启动
    await asyncio.sleep(2)

    # 取消运行
    print("取消运行中...")
    cancelled = await agent.acancel_run(run_id=run_output.run_id)
    print(f"取消结果: {cancelled}")

    # 检查最终状态
    await asyncio.sleep(1)
    result = await agent.aget_run_output(
        run_id=run_output.run_id,
        session_id=run_output.session_id,
    )
    if result:
        print(f"最终状态: {result.status}")
    print()


async def example_cancel_before_start():
    """在运行开始前取消（提前取消语义）。"""
    print("=" * 60)
    print("示例 3：启动前取消")
    print("=" * 60)

    from agno.run.cancel import cancel_run

    agent = Agent(
        name="PreCancelAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="在启动前就被取消的 agent",
        db=db,
    )

    # 预先生成一个 run ID
    from uuid import uuid4

    run_id = str(uuid4())

    # 在运行启动之前取消它
    print(f"提前取消运行 {run_id}...")
    cancel_run(run_id)

    # 现在使用该 ID 启动运行 — 它应该检测到取消
    run_output = await agent.arun(
        "这应该在运行前被取消。",
        background=True,
        run_id=run_id,
    )

    print(f"Run ID: {run_output.run_id}")
    print(f"初始状态: {run_output.status}")

    # 等待并检查 — 后台任务应该检测到取消
    await asyncio.sleep(2)
    result = await agent.aget_run_output(
        run_id=run_output.run_id,
        session_id=run_output.session_id,
    )
    if result:
        print(f"最终状态: {result.status}")
    print()


async def main():
    await example_background_run_with_polling()
    await example_cancel_background_run()
    await example_cancel_before_start()
    print("所有示例完成！")


if __name__ == "__main__":
    asyncio.run(main())
