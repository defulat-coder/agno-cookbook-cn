"""
04 带推理工具追踪的 Agent
=====================================

演示 04 带推理工具追踪的 agent。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.reasoning import ReasoningTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db_sqlite = SqliteDb(db_file="tmp/traces.db")

reasoning_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[ReasoningTools(add_instructions=True)],
    instructions=dedent("""\
        你是一个具有强大分析技能的专业问题解决助手！

        你解决问题的方法：
        1. 首先，将复杂问题分解为组成部分
        2. 清楚地陈述你的假设
        3. 制定结构化的推理路径
        4. 考虑多个视角
        5. 评估证据和反驳论点
        6. 得出有充分理由的结论

        解决问题时：
        - 使用明确的逐步推理
        - 识别关键变量和约束
        - 探索替代方案
        - 突出不确定性领域
        - 清楚地解释你的思考过程
        - 考虑短期和长期影响
        - 明确评估权衡

        对于定量问题：
        - 显示你的计算
        - 解释数字的重要性
        - 在适当时考虑置信区间
        - 识别源数据可靠性

        对于定性推理：
        - 评估不同因素如何相互作用
        - 考虑心理和社会动态
        - 评估实际约束
        - 处理价值考虑
        \
    """),
    add_datetime_to_context=True,
    stream_events=True,
    markdown=True,
    db=db_sqlite,
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="带追踪的推理 agent 示例应用",
    agents=[reasoning_agent],
    tracing=True,
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
    agent_os.serve(app="04_agent_with_reasoning_tools_tracing:app", reload=True)
