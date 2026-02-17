"""
多 Agent 团队 - 投资研究团队
============================================
本示例展示如何创建协同工作的 Agent 团队。
每个 Agent 都有专门的角色，由团队领导进行协调。

我们将构建一个具有对立视角的投资研究团队：
- 多头 Agent：为投资提出支持理由
- 空头 Agent：为投资提出反对理由
- 首席分析师：综合形成平衡的投资建议

这种对抗式方法比单个 Agent 能产出更好的分析。

核心概念：
- Team（团队）：由领导协调的一组 Agent
- Members（成员）：具有不同角色的专业化 Agent
- 领导负责分配任务、综合信息并输出最终结果

可尝试的示例提示：
- "我应该投资英伟达吗？"
- "分析特斯拉作为长期投资的价值"
- "苹果现在是否被高估？"
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.google import Gemini
from agno.team.team import Team
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
team_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 多头 Agent — 提出支持理由
# ---------------------------------------------------------------------------
bull_agent = Agent(
    name="Bull Analyst",
    role="Make the investment case FOR a stock",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    db=team_db,
    instructions="""\
你是一名多头分析师。你的任务是为投资某只股票提出最有力的支持理由。
找出积极因素：
- 增长驱动力和催化剂
- 竞争优势
- 强劲的财务数据和指标
- 市场机会

论述要有说服力，但必须以数据为基础。使用工具获取真实数据。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ---------------------------------------------------------------------------
# 空头 Agent — 提出反对理由
# ---------------------------------------------------------------------------
bear_agent = Agent(
    name="Bear Analyst",
    role="Make the investment case AGAINST a stock",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
    db=team_db,
    instructions="""\
你是一名空头分析师。你的任务是为反对投资某只股票提出最有力的理由。
找出风险：
- 估值担忧
- 竞争威胁
- 财务弱点
- 市场或宏观风险

保持批判但公正。使用工具获取真实数据来支撑你的论点。\
""",
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

# ---------------------------------------------------------------------------
# 创建团队
# ---------------------------------------------------------------------------
multi_agent_team = Team(
    name="Multi-Agent Team",
    model=Gemini(id="gemini-3-flash-preview"),
    members=[bull_agent, bear_agent],
    instructions="""\
你领导一个投资研究团队，包含一名多头分析师和一名空头分析师。

## 流程

1. 将股票发送给两位分析师
2. 让每位独立给出分析
3. 综合他们的论点形成平衡的建议

## 输出格式

听取两位分析师的意见后，提供：
- **多头观点摘要**：多头分析师的关键论点
- **空头观点摘要**：空头分析师的关键论点
- **综合分析**：他们在哪些方面一致？在哪些方面分歧？
- **建议**：你的平衡观点（买入/持有/卖出）及置信度
- **关键指标**：重要数据的表格

态度果断，但承认不确定性。\
""",
    db=team_db,
    show_members_responses=True,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行团队
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 第一次分析
    multi_agent_team.print_response(
        "我应该投资英伟达（NVDA）吗？",
        stream=True,
    )

    # 追问 — 团队会记住之前的分析
    multi_agent_team.print_response(
        "AMD 与它相比如何？",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
何时使用团队 vs 单个 Agent：

单个 Agent：
- 一个连贯的任务
- 不需要对立观点
- 越简单越好

团队：
- 需要多种视角
- 需要专业知识
- 复杂任务受益于分工协作
- 对抗式推理（如本示例）

其他团队模式：

1. 研究 → 分析 → 撰写的管道
   researcher = Agent(role="Gather information")
   analyst = Agent(role="Analyze data")
   writer = Agent(role="Write report")

2. 检查者模式
   worker = Agent(role="Do the task")
   checker = Agent(role="Verify the work")

3. 专家路由模式
   classifier = Agent(role="Route to specialist")
   specialists = [finance_agent, legal_agent, tech_agent]
"""
