"""
带记忆的 Agent - 能记住你的金融 Agent
=====================================================
本示例展示如何为 Agent 添加用户偏好记忆。
Agent 可以跨所有对话记住关于你的信息。

与存储（保存对话历史）不同，记忆保存的是
用户级别的信息：偏好、事实、上下文。

核心概念：
- MemoryManager：从对话中提取并存储用户记忆
- enable_agentic_memory：Agent 通过工具调用决定何时存储/检索（高效）
- update_memory_on_run：记忆管理器在每次响应后运行（保证捕获）
- user_id：将记忆关联到特定用户

可尝试的示例提示：
- "我对科技股感兴趣，尤其是 AI 公司"
- "我的风险承受能力是中等"
- "你会为我推荐什么股票？"
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools
from rich.pretty import pprint

load_dotenv()

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 记忆管理器配置
# ---------------------------------------------------------------------------
memory_manager = MemoryManager(
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    db=agent_db,
    additional_instructions="""
    捕获用户喜爱的股票、风险承受能力和投资目标。
    """,
)

# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent——一个数据驱动的分析师，负责获取市场数据、
计算关键指标，并提供简洁的、可供决策的洞察。

## 记忆

你拥有用户偏好的记忆（自动在上下文中提供）。用它来：
- 根据用户兴趣定制推荐
- 考虑用户的风险承受能力
- 参考用户的投资目标

## 工作流程

1. 获取数据
   - 获取：价格、涨跌幅、市值、市盈率、每股收益、52周范围
   - 对比分析时，为每只股票获取相同字段

2. 分析
   - 在未提供时计算比率（市盈率、市销率、利润率）
   - 关键驱动因素和风险——最多 2-3 条
   - 仅陈述事实，不做投机

3. 呈现
   - 以一行摘要开头
   - 多股对比使用表格
   - 保持精炼

## 规则

- 数据来源：Yahoo Finance。始终标注时间戳。
- 数据缺失？标注"N/A"，继续。
- 不提供个性化建议——相关时添加免责声明。
- 不使用 emoji。\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
user_id = "investor@example.com"

agent_with_memory = Agent(
    name="Agent with Memory",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    instructions=instructions,
    tools=[YFinanceTools()],
    db=agent_db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 告诉 Agent 你的偏好
    agent_with_memory.print_response(
        "我对 AI 和半导体股票感兴趣。我的风险承受能力是中等。",
        user_id=user_id,
        stream=True,
    )

    # Agent 现在知道了你的偏好
    agent_with_memory.print_response(
        "你会为我推荐什么股票？",
        user_id=user_id,
        stream=True,
    )

    # 查看已存储的记忆
    memories = agent_with_memory.get_user_memories(user_id=user_id)
    print("\n" + "=" * 60)
    print("已存储的记忆:")
    print("=" * 60)
    pprint(memories)

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
记忆 vs 存储：

- 存储（Storage）："我们讨论了什么？"（对话历史）
- 记忆（Memory）："你了解我哪些信息？"（用户偏好）

记忆跨会话持久化：

1. 运行此脚本——Agent 学习你的偏好
2. 使用相同 user_id 开始一个新会话
3. Agent 仍然记得你喜欢 AI 股票

适用场景：
- 个性化推荐
- 记住用户上下文（职业、目标、约束条件）
- 跨对话建立默契

启用记忆的两种方式：

1. enable_agentic_memory=True（本示例使用的方式）
   - Agent 通过工具调用决定何时存储/检索
   - 更高效——仅在需要时运行

2. update_memory_on_run=True
   - 记忆管理器在每次 Agent 响应后运行
   - 保证捕获——不会遗漏用户信息
   - 更高的延迟和成本
"""
