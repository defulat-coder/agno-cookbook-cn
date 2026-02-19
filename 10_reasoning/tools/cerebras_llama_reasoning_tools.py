"""
Cerebras Llama 推理工具
==============================

演示推理 Cookbook 示例。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.models.cerebras import Cerebras
from agno.tools.reasoning import ReasoningTools


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    reasoning_agent = Agent(
        model=Cerebras(id="llama-3.3-70b"),
        tools=[ReasoningTools(add_instructions=True)],
        instructions=dedent("""\
            你是一位拥有强大分析能力的专业问题解决助手！

            解决问题的方式：
            1. 首先，将复杂问题分解为各个组成部分
            2. 清晰陈述你的假设
            3. 制定结构化的推理路径
            4. 考虑多种视角
            5. 评估证据和反驳论点
            6. 得出有充分依据的结论

            解决问题时：
            - 使用明确的逐步推理
            - 识别关键变量和约束条件
            - 探索替代方案
            - 突出不确定性领域
            - 清晰解释你的思考过程
            - 同时考虑短期和长期影响
            - 明确评估权衡取舍

            对于定量问题：
            - 展示你的计算过程
            - 解释数字的重要性
            - 在适当情况下考虑置信区间
            - 识别数据来源的可靠性

            对于定性推理：
            - 评估不同因素的相互作用
            - 考虑心理和社会动态
            - 评估实际约束条件
            - 考虑价值因素
            \
        """),
        add_datetime_to_context=True,
        stream_events=True,
        markdown=True,
    )

    # 使用复杂推理问题的示例
    reasoning_agent.print_response(
        "请解决这道逻辑谜题：一个人需要将一只狐狸、一只鸡和一袋谷物运过河。"
        "船只能容纳这个人和一样东西。如果无人看管，狐狸会吃鸡，鸡会吃谷物。"
        "这个人怎样才能将所有东西安全运过河？",
        stream=True,
    )

    # # 经济分析示例
    # reasoning_agent.print_response(
    #     "在当前利率、通货膨胀和市场趋势下，租房还是买房更合适？"
    #     "请在分析中同时考虑财务和生活方式因素。",
    #     stream=True
    # )

    # # 战略决策示例
    # reasoning_agent.print_response(
    #     "一家初创公司有 50 万美元资金，需要决定将其用于市场营销还是产品开发。"
    #     "他们希望在 12 个月内最大化增长和用户获取。"
    #     "他们应该考虑哪些因素，如何分析这个决策？",
    #     stream=True
    # )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
