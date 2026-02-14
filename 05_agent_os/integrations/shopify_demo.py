"""
AgentOS 与 Shopify 工具的示例。

前置条件：
- 设置以下环境变量：
    - SHOPIFY_SHOP_NAME -> 你的 Shopify 商店名称，例如 "my-store" 来自 my-store.myshopify.com
    - SHOPIFY_ACCESS_TOKEN -> 你的 Shopify 访问令牌

你可以从 Shopify Admin > Settings > Apps and sales channels > Develop apps 获取你的 Shopify 访问令牌

所需范围：
- read_orders（用于订单和销售数据）
- read_products（用于产品信息）
- read_customers（用于客户洞察）
- read_analytics（用于分析数据）
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.config import AgentOSConfig, ChatConfig
from agno.tools.shopify import ShopifyTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = PostgresDb(id="basic-db", db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

sales_agent = Agent(
    name="Sales Analyst",
    model=OpenAIChat(id="gpt-5.2"),
    db=db,
    tools=[ShopifyTools()],
    instructions=[
        "你是一个使用 Shopify 的电子商务商店的销售分析师。",
        "帮助用户了解他们的销售业绩、产品趋势和客户行为。",
        "分析数据时：",
        "1. 首先使用可用工具获取相关数据",
        "2. 以清晰、可操作的格式总结关键见解",
        "3. 突出显示值得注意的模式或问题",
        "4. 在适当时建议后续步骤",
        "始终清晰地呈现数字并使用比较来增加上下文。",
        "如果需要获取有关商店的信息，如货币，调用 `get_shop_info` 工具。",
    ],
    markdown=True,
    add_datetime_to_context=True,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Example app for Shopify agent",
    agents=[sales_agent],
    config=AgentOSConfig(
        chat=ChatConfig(
            quick_prompts={
                "sales_agent": [
                    "What are my top 5 selling products in the last 30 days? Show me quantity sold and revenue for each.",
                    "Which products are frequently bought together? I want to create product bundles for my store.",
                    "How are my sales trending compared to last month? Are we up or down in terms of revenue and order count?",
                ],
            },
        ),
    ),
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
    agent_os.serve(app="shopify_demo:app", reload=True)
