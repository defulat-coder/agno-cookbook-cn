"""
结构化输出 Agent - 带类型化响应的金融 Agent
==================================================================
本示例展示如何从 Agent 获取结构化的类型响应。
不再是自由格式的文本，而是可信赖的 Pydantic 模型。

非常适合构建数据管道、UI 或集成场景，当你需要
可预测的数据结构时。直接解析、存储、展示——无需正则表达式。

核心概念：
- output_schema：定义响应结构的 Pydantic 模型
- Agent 的响应将始终符合此 schema
- 通过 response.content 访问结构化数据

可尝试的示例提示：
- "分析 NVDA"
- "给我一份关于特斯拉的报告"
- "苹果的投资案例是什么？"
"""

import os

from dotenv import load_dotenv
from typing import List, Optional

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools
from pydantic import BaseModel, Field

load_dotenv()

# ---------------------------------------------------------------------------
# 存储配置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")


# ---------------------------------------------------------------------------
# 结构化输出 Schema
# ---------------------------------------------------------------------------
class StockAnalysis(BaseModel):
    """股票分析的结构化输出。"""

    ticker: str = Field(..., description="Stock ticker symbol (e.g., NVDA)")
    company_name: str = Field(..., description="Full company name")
    current_price: float = Field(..., description="Current stock price in USD")
    market_cap: str = Field(..., description="Market cap (e.g., '3.2T' or '150B')")
    pe_ratio: Optional[float] = Field(None, description="P/E ratio, if available")
    week_52_high: float = Field(..., description="52-week high price")
    week_52_low: float = Field(..., description="52-week low price")
    summary: str = Field(..., description="One-line summary of the stock")
    key_drivers: List[str] = Field(..., description="2-3 key growth drivers")
    key_risks: List[str] = Field(..., description="2-3 key risks")
    recommendation: str = Field(
        ..., description="One of: Strong Buy, Buy, Hold, Sell, Strong Sell"
    )


# ---------------------------------------------------------------------------
# Agent 指令
# ---------------------------------------------------------------------------
instructions = """\
你是一个金融 Agent——一个数据驱动的分析师，负责获取市场数据、
计算关键指标，并提供简洁的、可供决策的洞察。

## 工作流程

1. 获取数据
   - 获取：价格、涨跌幅、市值、市盈率、每股收益、52周范围
   - 获取分析所需的所有字段

2. 分析
   - 识别 2-3 个关键驱动因素（哪些方面表现好）
   - 识别 2-3 个关键风险（哪些可能出问题）
   - 仅陈述事实，不做投机

3. 推荐
   - 基于数据提供明确的建议
   - 态度果断，但注明这不是个性化建议

## 规则

- 数据来源：Yahoo Finance
- 数据缺失？可选字段使用 null，必填字段进行估算
- 推荐必须是以下之一：Strong Buy、Buy、Hold、Sell、Strong Sell\
"""

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent_with_structured_output = Agent(
    name="Agent with Structured Output",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    instructions=instructions,
    tools=[YFinanceTools()],
    output_schema=StockAnalysis,
    db=agent_db,
    add_datetime_to_context=True,
    add_history_to_context=True,
    num_history_runs=5,
    markdown=True,
    debug_mode=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 获取结构化输出
    response = agent_with_structured_output.run("分析英伟达")

    # 访问类型化数据
    analysis: StockAnalysis = response.content

    # 以编程方式使用数据
    print(f"\n{'=' * 60}")
    print(f"股票分析: {analysis.company_name} ({analysis.ticker})")
    print(f"{'=' * 60}")
    print(f"价格: ${analysis.current_price:.2f}")
    print(f"市值: {analysis.market_cap}")
    print(f"市盈率: {analysis.pe_ratio or 'N/A'}")
    print(f"52周范围: ${analysis.week_52_low:.2f} - ${analysis.week_52_high:.2f}")
    print(f"\n摘要: {analysis.summary}")
    print("\n关键驱动因素:")
    for driver in analysis.key_drivers:
        print(f"  • {driver}")
    print("\n关键风险:")
    for risk in analysis.key_risks:
        print(f"  • {risk}")
    print(f"\n推荐: {analysis.recommendation}")
    print(f"{'=' * 60}\n")

# ---------------------------------------------------------------------------
# 更多示例
# ---------------------------------------------------------------------------
"""
结构化输出非常适合以下场景：

1. 构建 UI
   analysis = agent.run("Analyze TSLA").content
   render_stock_card(analysis)

2. 存入数据库
   db.insert("analyses", analysis.model_dump())

3. 比较股票
   nvda = agent.run("Analyze NVDA").content
   amd = agent.run("Analyze AMD").content
   if nvda.pe_ratio < amd.pe_ratio:
       print(f"{nvda.ticker} is cheaper by P/E")

4. 构建数据管道
   tickers = ["AAPL", "GOOGL", "MSFT"]
   analyses = [agent.run(f"Analyze {t}").content for t in tickers]

Schema 保证你始终获得预期的字段。
无需解析，没有意外。
"""
