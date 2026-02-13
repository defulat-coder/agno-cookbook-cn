"""
工具调用压缩
=============================

演示工具调用压缩功能。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIResponses(id="gpt-5-nano"),
    tools=[WebSearchTools()],
    description="专门跟踪竞争对手活动",
    instructions="使用搜索工具，始终使用最新的信息和数据。",
    db=SqliteDb(db_file="tmp/dbs/tool_call_compression.db"),
    compress_tool_results=True,  # 启用工具调用压缩
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        """
        使用搜索工具，始终获取最新的信息和数据。
        研究这些 AI 公司最近（过去 3 个月）的活动：

        1. OpenAI - 产品发布、合作伙伴关系、定价
        2. Anthropic - 新功能、企业交易、融资
        3. Google DeepMind - 研究突破、产品发布
        4. Meta AI - 开源发布、研究论文

        对于每个公司，查找具体行动及其日期和数字。""",
        stream=True,
    )
