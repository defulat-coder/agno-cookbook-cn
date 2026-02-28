"""
自定义记忆优化策略
==================

本示例展示如何通过继承 MemoryOptimizationStrategy 来创建和应用自定义记忆优化策略。
"""

from datetime import datetime
from typing import List

from agno.agent import Agent
from agno.db.schemas import UserMemory
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager, MemoryOptimizationStrategy
from agno.models.base import Model
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建自定义策略
# ---------------------------------------------------------------------------
class RecentOnlyStrategy(MemoryOptimizationStrategy):
    """仅保留最近的 N 条记忆。"""

    def __init__(self, keep_count: int = 2):
        self.keep_count = keep_count

    def optimize(
        self,
        memories: List[UserMemory],
        model: Model,
    ) -> List[UserMemory]:
        """仅保留最近的 N 条记忆。"""
        sorted_memories = sorted(
            memories,
            key=lambda m: m.updated_at or m.created_at or datetime.min,
            reverse=True,
        )
        return sorted_memories[: self.keep_count]

    async def aoptimize(
        self,
        memories: List[UserMemory],
        model: Model,
    ) -> List[UserMemory]:
        """optimize 的异步版本。"""
        sorted_memories = sorted(
            memories,
            key=lambda m: m.updated_at or m.created_at or datetime.min,
            reverse=True,
        )
        return sorted_memories[: self.keep_count]


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_file = "tmp/custom_memory_strategy.db"
db = SqliteDb(db_file=db_file)
user_id = "user3"

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
        "我目前在学习机器学习，到目前为止这是一段非常棒的旅程。我大约 6 个月前从基础开始——"
        "线性回归、决策树和简单的分类算法。现在我正在深入更高级的主题，比如深度学习和神经网络。"
        "我使用 Python 以及 scikit-learn、TensorFlow 和 PyTorch 等库。"
        "数学有时很有挑战性，尤其是微积分和线性代数，但我在一步步攻克。",
        user_id=user_id,
    )
    agent.print_response(
        "我最近在 Coursera 上完成了一门关于神经网络的优秀在线课程。课程涵盖了从基础感知机到 CNN 和 RNN 等复杂架构的所有内容。"
        "讲师对反向传播和梯度下降讲解得非常好。"
        "我完成了所有编程作业，从零构建了神经网络，也使用了 TensorFlow。"
        "期末项目是构建一个图像分类器，在测试集上达到了 92% 的准确率。我为这个成果感到很自豪。",
        user_id=user_id,
    )
    agent.print_response(
        "我的最终目标是构建自己的 AI 项目来解决现实问题。我有几个想探索的想法——"
        "也许是推荐系统、客服聊天机器人，或者计算机视觉方面的项目。"
        "我在尝试找到 AI 能真正发挥作用的问题，以及我有能力构建有意义成果的领域。"
        "我知道还需要更多经验和练习，但我会坚持做个人项目来丰富作品集。",
        user_id=user_id,
    )
    agent.print_response(
        "我对自然语言处理应用特别感兴趣。大语言模型的最新进展令人着迷。"
        "我一直在尝试 Transformer 架构，试图理解注意力机制的工作原理。"
        "我很想做文本分类、情感分析，甚至构建对话式 AI 的项目。"
        "NLP 感觉目前正处于最前沿，这个领域有很多有趣的问题等待解决。",
        user_id=user_id,
    )

    print("\n优化前：")
    memories_before = agent.get_user_memories(user_id=user_id)
    print(f"  记忆条数：{len(memories_before)}")

    custom_strategy = RecentOnlyStrategy(keep_count=2)
    tokens_before = custom_strategy.count_tokens(memories_before)
    print(f"  Token 数量：{tokens_before} tokens")

    print("\n所有记忆：")
    for i, memory in enumerate(memories_before, 1):
        print(f"  {i}. {memory.memory}")

    print("\n使用自定义 RecentOnlyStrategy（keep_count=2）优化...")

    memory_manager.optimize_memories(
        user_id=user_id,
        strategy=custom_strategy,
        apply=True,
    )

    print("\n优化后：")
    memories_after = agent.get_user_memories(user_id=user_id)
    print(f"  记忆条数：{len(memories_after)}")

    tokens_after = custom_strategy.count_tokens(memories_after)
    print(f"  Token 数量：{tokens_after} tokens")

    if tokens_before > 0:
        reduction_pct = ((tokens_before - tokens_after) / tokens_before) * 100
        tokens_saved = tokens_before - tokens_after
        print(
            f"  缩减：{reduction_pct:.1f}%（保留最近 2 条，节省 {tokens_saved} tokens）"
        )

    print("\n保留的记忆（最近 2 条）：")
    for i, memory in enumerate(memories_after, 1):
        print(f"  {i}. {memory.memory}")
