import asyncio

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

fun_facts = """
- 地球是距离太阳第三近的行星，也是已知唯一支持生命的天体。
- 地球表面约71%被水覆盖，其中太平洋是最大的海洋。
- 地球大气主要由氮气（78%）和氧气（21%）组成，还有微量的其他气体。
- 地球每24小时自转一圈，形成昼夜循环。
- 地球有一颗天然卫星——月球，它影响潮汐并稳定地球的轴向倾斜。
- 地球的构造板块不断移动，导致地震和火山爆发等地质活动。
- 地球的最高点是珠穆朗玛峰，海拔8,848米（29,029英尺）。
- 海洋最深处是马里亚纳海沟，深度超过11,000米（36,000英尺）。
- 地球拥有多样化的生态系统，从雨林、沙漠到珊瑚礁和苔原。
- 地球的磁场通过偏转有害的太阳辐射和宇宙射线来保护生命。
"""

# 数据库连接 URL
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    vector_db=PgVector(
        table_name="documents",
        db_url=db_url,
    ),
)

# 创建包含知识的 Agent
agent = Agent(
    knowledge=knowledge,
)


async def main():
    # 加载知识
    await knowledge.ainsert(
        text_content=fun_facts,
    )

    # 向 Agent 询问知识
    await agent.aprint_response("你能告诉我关于地球的信息吗？", markdown=True)


if __name__ == "__main__":
    asyncio.run(main())
