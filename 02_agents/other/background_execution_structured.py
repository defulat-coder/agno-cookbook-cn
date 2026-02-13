"""
演示带有结构化输出的后台执行示例。

将后台执行（非阻塞、异步）与 Pydantic output_schema 结合，
使完成的运行返回类型化的结构化数据。

要求：
- 运行 PostgreSQL（./cookbook/scripts/run_pgvector.sh）
- 设置 OPENAI_API_KEY

使用方法：
    .venvs/demo/bin/python cookbook/02_agents/other/background_execution_structured.py
"""

import asyncio
from typing import List

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.run.base import RunStatus
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# 输出 Schema
# ---------------------------------------------------------------------------


class CityFact(BaseModel):
    city: str = Field(..., description="Name of the city")
    country: str = Field(..., description="Country the city is in")
    population: str = Field(..., description="Approximate population")
    fun_fact: str = Field(..., description="An interesting fact about the city")


class CityFactsResponse(BaseModel):
    cities: List[CityFact] = Field(..., description="List of city facts")


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

db = PostgresDb(
    db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    session_table="bg_structured_sessions",
)


# ---------------------------------------------------------------------------
# 创建并运行后台示例
# ---------------------------------------------------------------------------


async def example_structured_background_run():
    """通过 output_schema 返回结构化数据的后台运行。"""
    print("=" * 60)
    print("带有结构化输出的后台执行")
    print("=" * 60)

    agent = Agent(
        name="CityFactsAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="提供城市结构化信息的 agent。",
        db=db,
    )

    # 启动带有结构化输出的后台运行
    run_output = await agent.arun(
        "给我提供关于东京、巴黎和纽约的信息。",
        output_schema=CityFactsResponse,
        background=True,
    )

    print(f"Run ID: {run_output.run_id}")
    print(f"状态: {run_output.status}")
    assert run_output.status == RunStatus.pending

    # 轮询完成状态
    print("\n轮询完成中...")
    for i in range(30):
        await asyncio.sleep(1)
        result = await agent.aget_run_output(
            run_id=run_output.run_id,
            session_id=run_output.session_id,
        )
        if result is None:
            print(f"  [{i + 1}s] 尚未在数据库中")
            continue

        print(f"  [{i + 1}s] 状态: {result.status}")

        if result.status == RunStatus.completed:
            print("\n完成！结构化输出:")

            # 解析 JSON 内容为 Pydantic 模型
            try:
                content = result.content
                if isinstance(content, str):
                    import json

                    content = json.loads(content)
                parsed = CityFactsResponse.model_validate(content)
                for city_fact in parsed.cities:
                    print(f"\n  {city_fact.city}, {city_fact.country}")
                    print(f"    人口: {city_fact.population}")
                    print(f"    趣闻: {city_fact.fun_fact}")
            except Exception:
                print(f"  原始内容: {result.content}")
            break
        elif result.status == RunStatus.error:
            print(f"\n失败: {result.content}")
            break
    else:
        print("\n等待完成超时")


async def example_multiple_background_runs():
    """同时启动多个后台运行并收集结果。"""
    from uuid import uuid4

    print()
    print("=" * 60)
    print("多个并发后台运行")
    print("=" * 60)

    agent = Agent(
        name="QuizAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="回答问答题的 agent。",
        db=db,
    )

    questions = [
        "世界上最高的山是什么？一句话回答。",
        "最深的海沟是什么？一句话回答。",
        "世界上最长的河流是什么？一句话回答。",
    ]

    # 同时启动所有运行，每个都有自己的会话以避免冲突
    runs = []
    for question in questions:
        session_id = str(uuid4())
        run_output = await agent.arun(question, background=True, session_id=session_id)
        runs.append(run_output)
        print(f"已启动: {run_output.run_id} - {question[:50]}...")

    # 轮询所有运行直到全部完成
    print("\n等待所有运行完成...")
    results = {}
    for attempt in range(30):
        await asyncio.sleep(1)
        all_done = True
        for run in runs:
            if run.run_id in results:
                continue
            result = await agent.aget_run_output(
                run_id=run.run_id,
                session_id=run.session_id,
            )
            if result and result.status in (RunStatus.completed, RunStatus.error):
                results[run.run_id] = result
            else:
                all_done = False

        if all_done:
            break

    # 打印结果
    print(f"\n完成 {len(results)}/{len(runs)} 个运行:")
    for i, run in enumerate(runs):
        result = results.get(run.run_id)
        if result:
            print(f"\n  问题: {questions[i]}")
            print(f"  答案: {result.content}")
            print(f"  状态: {result.status}")
        else:
            print(f"\n  问题: {questions[i]}")
            print("  状态: 仍在运行或未找到")


async def main():
    await example_structured_background_run()
    await example_multiple_background_runs()
    print("\n所有示例完成！")


if __name__ == "__main__":
    asyncio.run(main())
