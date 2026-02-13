"""
高级压缩
=============================

此示例展示如何为工具调用压缩设置基于上下文 token 的限制。
"""

from agno.agent import Agent
from agno.compression.manager import CompressionManager
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools

compression_prompt = """
    你是一名压缩专家。你的目标是为竞争情报分析师压缩网络搜索结果。
    
    你的目标：提取可操作的竞争洞察，同时极度简洁。
    
    必须保留：
    - 竞争对手名称和具体行动（产品发布、合作伙伴关系、收购、定价变化）
    - 精确数字（收入、市场份额、增长率、定价、员工人数）
    - 准确日期（公告日期、发布日期、交易日期）
    - 高管或官方声明的直接引用
    - 融资轮次和估值
    
    必须删除：
    - 公司历史和背景信息
    - 一般行业趋势（除非针对竞争对手）
    - 分析师观点和猜测（仅保留事实）
    - 详细的产品描述（仅保留关键差异点和定价）
    - 营销宣传和促销语言
    
    输出格式：
    返回一个项目符号列表，每行遵循此格式：
    "[公司名称] - [日期]: [行动/事件] ([关键数字/详情])"
    
    总字数保持在 200 字以内。务必极度简洁。仅陈述事实。
    
    示例：
    - Acme Corp - Mar 15, 2024: 以 $99/用户/月推出 AcmeGPT，目标企业市场
    - TechCo - Feb 10, 2024: 以 $150M 收购 DataStart，获得 500 个企业客户
"""

compression_manager = CompressionManager(
    model=OpenAIChat(id="gpt-5-mini"),
    compress_token_limit=5000,
    compress_tool_call_instructions=compression_prompt,
)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    description="专门跟踪竞争对手活动",
    instructions="使用搜索工具，始终使用最新的信息和数据。",
    db=SqliteDb(db_file="tmp/token_based_tool_call_compression.db"),
    compression_manager=compression_manager,
    add_history_to_context=True,  # 将历史添加到上下文
    num_history_runs=3,
    session_id="token_based_tool_call_compression",
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        """
        使用搜索工具，始终使用最新的信息和数据。
        研究这些 AI 公司最近（过去 3 个月）的活动：
        
        1. OpenAI - 产品发布、合作伙伴关系、定价
        2. Anthropic - 新功能、企业交易、融资
        3. Google DeepMind - 研究突破、产品发布
        4. Meta AI - 开源发布、研究论文
       
        对于每个公司，查找具体行动及其日期和数字。""",
        stream=True,
    )
