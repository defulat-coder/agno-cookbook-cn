"""
使用摘要策略优化记忆
====================

本示例演示使用摘要策略进行记忆优化，
将所有记忆合并为一条摘要以减少 token 消耗。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager, SummarizeStrategy
from agno.memory.strategies.types import MemoryOptimizationStrategyType
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_file = "tmp/memory_summarize_strategy.db"
db = SqliteDb(db_file=db_file)
user_id = "user2"

# ---------------------------------------------------------------------------
# 创建 Agent 和记忆管理器
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
    update_memory_on_run=True,
)

memory_manager = MemoryManager(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=db,
)

# ---------------------------------------------------------------------------
# 运行优化
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("正在创建记忆...")
    agent.print_response(
        "我有一只很棒的宠物狗叫 Max，3 岁了。他是一只金毛寻回犬，非常友善又精力充沛。"
        "他 8 周大的时候我们就把他接回来了。他喜欢在公园里捡球玩，还喜欢散长步。"
        "Max 也很聪明——他会大约 15 个不同的指令和技巧。照顾他是我人生中最有意义的经历之一。"
        "他现在基本上就是家庭的一员了。",
        user_id=user_id,
    )
    agent.print_response(
        "我目前住在旧金山，虽然有很多挑战，但这是一座很棒的城市。我已经在这里住了大约 5 年。"
        "我在科技行业工作，是一家中型软件公司的产品经理。这里的科技圈非常棒——"
        "有很多聪明人在做有趣的事情。生活成本确实很高，但机会和社区让一切都值得。"
        "我住在 Mission 区，那里有很棒的美食和充满活力的文化。",
        user_id=user_id,
    )
    agent.print_response(
        "周末我很喜欢在湾区周围的美丽地方徒步。有很多很棒的步道——"
        "从塔玛尔佩斯山到大盆地红杉林。我通常和一群朋友一起去徒步，每个月都会尝试探索新的步道。"
        "我还喜欢尝试新餐厅。旧金山的美食圈太棒了，有来自世界各地的菜系。"
        "我总是在寻找隐藏的好去处和新的餐厅。我最喜欢的菜系是日本菜、泰国菜和墨西哥菜。",
        user_id=user_id,
    )
    agent.print_response(
        "我学钢琴大约一年半了。这是我一直想做但从来没时间的事情。"
        "我终于决定坚持下去，几乎每天都练习，通常 30-45 分钟。"
        "我现在在练古典曲目——能弹一些简单的巴赫和莫扎特作品。"
        "我的目标是最终也能弹一些爵士钢琴。有这样一个创意爱好对我的心理健康很有帮助，"
        "拥有一个与日常工作完全不同的事情也很好。",
        user_id=user_id,
    )

    print("\n优化前：")
    memories_before = agent.get_user_memories(user_id=user_id)
    print(f"  记忆条数：{len(memories_before)}")

    strategy = SummarizeStrategy()
    tokens_before = strategy.count_tokens(memories_before)
    print(f"  Token 数量：{tokens_before} tokens")

    print("\n各条记忆：")
    for i, memory in enumerate(memories_before, 1):
        print(f"  {i}. {memory.memory}")

    print("\n使用 'summarize' 策略优化记忆...")
    memory_manager.optimize_memories(
        user_id=user_id,
        strategy=MemoryOptimizationStrategyType.SUMMARIZE,
        apply=True,
    )

    print("\n优化后：")
    memories_after = agent.get_user_memories(user_id=user_id)
    print(f"  记忆条数：{len(memories_after)}")

    tokens_after = strategy.count_tokens(memories_after)
    print(f"  Token 数量：{tokens_after} tokens")

    if tokens_before > 0:
        reduction_pct = ((tokens_before - tokens_after) / tokens_before) * 100
        tokens_saved = tokens_before - tokens_after
        print(f"  缩减：{reduction_pct:.1f}%（节省 {tokens_saved} tokens）")

    if memories_after:
        print("\n摘要后的记忆：")
        print(f"  {memories_after[0].memory}")
    else:
        print("\n 优化后未找到记忆")
