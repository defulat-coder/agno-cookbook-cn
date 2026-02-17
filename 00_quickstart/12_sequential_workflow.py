"""
顺序工作流 - 股票研究管道
==============================================
本示例展示如何创建具有顺序步骤的工作流。
每个步骤由专门的 Agent 处理，输出传递到下一个步骤。

与团队（Agent 动态协作）不同，工作流让你
显式控制执行顺序和数据流向。

核心概念：
- Workflow（工作流）：编排一系列步骤
- Step（步骤）：将 Agent 包装为特定任务
- 步骤按顺序执行，每一步基于前一步的结果

可尝试的示例提示：
- "分析 NVDA"
- "研究特斯拉的投资价值"
- "给我一份关于苹果的报告"
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow

load_dotenv()

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
workflow_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 步骤 1：数据采集器 — 获取原始市场数据
# ---------------------------------------------------------------------------
data_agent = Agent(
    name="Data Gatherer",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    tools=[YFinanceTools()],
    instructions="""\
你是一个数据采集 Agent。你的任务是获取全面的市场数据。

对于请求的股票，采集：
- 当前价格和日涨跌幅
- 市值和成交量
- 市盈率、每股收益和其他关键比率
- 52周最高价和最低价
- 近期价格趋势

清晰地呈现原始数据。不要分析——只负责采集和整理。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

data_step = Step(
    name="Data Gathering",
    agent=data_agent,
    description="Fetch comprehensive market data for the stock",
)

# ---------------------------------------------------------------------------
# 步骤 2：分析师 — 解读数据
# ---------------------------------------------------------------------------
analyst_agent = Agent(
    name="Analyst",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    instructions="""\
你是一名金融分析师。你从数据团队获取原始市场数据。

你的任务是：
- 解读关键指标（该板块的市盈率是偏高还是偏低？）
- 识别优势和劣势
- 标注任何警示信号或积极信号
- 与典型行业基准进行对比

提供分析，不提供建议。保持客观和数据驱动。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
)

analysis_step = Step(
    name="Analysis",
    agent=analyst_agent,
    description="Analyze the market data and identify key insights",
)

# ---------------------------------------------------------------------------
# 步骤 3：报告撰写者 — 生成最终输出
# ---------------------------------------------------------------------------
report_agent = Agent(
    name="Report Writer",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    instructions="""\
你是一名报告撰写者。你从研究团队获取分析结果。

你的任务是：
- 将分析综合成清晰的投资简报
- 以一行摘要开头
- 包含建议（买入/持有/卖出）及理由
- 保持简洁——最多 200 字
- 以关键指标的小表格结尾

为忙碌的投资者写作，他们想快速看到结论。\
""",
    db=workflow_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
)

report_step = Step(
    name="Report Writing",
    agent=report_agent,
    description="Produce a concise investment brief",
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
sequential_workflow = Workflow(
    name="Sequential Workflow",
    description="Three-step research pipeline: Data → Analysis → Report",
    steps=[
        data_step,  # 步骤 1：采集数据
        analysis_step,  # 步骤 2：分析数据
        report_step,  # 步骤 3：撰写报告
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sequential_workflow.print_response(
        "分析英伟达（NVDA）的投资价值",
        stream=True,
    )

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
工作流 vs 团队：

- 工作流：显式的步骤顺序，可预测的执行，清晰的数据流
- 团队：动态协作，领导决定谁做什么

何时使用工作流：
- 步骤必须按特定顺序执行
- 每个步骤有明确的专门角色
- 需要可预测、可重复的执行
- 步骤 N 的输出流入步骤 N+1

何时使用团队：
- Agent 需要动态协作
- 领导应决定让谁参与
- 任务受益于来回讨论

高级工作流功能（本示例未展示）：
- Parallel（并行）：并发运行步骤
- Condition（条件）：仅在满足条件时运行步骤
- Loop（循环）：重复步骤直到满足条件
- Router（路由）：动态选择运行哪个步骤
"""
