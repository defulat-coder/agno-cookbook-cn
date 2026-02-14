"""
Reasoning Agent
===============

演示 reasoning agent。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic.claude import Claude
from agno.os.app import AgentOS
from agno.os.interfaces.whatsapp import Whatsapp
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

agent_db = SqliteDb(db_file="tmp/persistent_memory.db")

reasoning_finance_agent = Agent(
    name="Reasoning Finance Agent",
    model=Claude(id="claude-3-7-sonnet-latest"),
    db=agent_db,
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True,
        ),
    ],
    instructions="使用表格显示数据。当你使用思考工具时，保持思考简洁。",
    add_datetime_to_context=True,
    markdown=True,
)


# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    agents=[reasoning_finance_agent],
    interfaces=[Whatsapp(agent=reasoning_finance_agent)],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:7777/config

    """
    agent_os.serve(app="reasoning_agent:app", reload=True)
