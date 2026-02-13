"""
Agno 演示注册表。

为 AgentOS 提供共享的工具、模型和数据库连接。
"""

from agno.models.openai import OpenAIResponses
from agno.registry import Registry
from agno.tools.calculator import CalculatorTools
from db import get_postgres_db

demo_db = get_postgres_db()

registry = Registry(
    tools=[CalculatorTools()],
    models=[
        OpenAIResponses(id="gpt-5.2"),
        OpenAIResponses(id="gpt-5.2-mini"),
    ],
    dbs=[demo_db],
)
