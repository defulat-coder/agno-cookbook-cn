"""
科学摘要评审
============================

演示内置推理和 DeepSeek 推理模型在研究方法评审中的应用。
"""

from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
task = (
    "请阅读以下科学论文摘要，并对其研究方法、结果、结论以及潜在偏差或缺陷进行批判性评估：\n\n"
    "摘要：本研究考察了一种新教学方法对学生数学成绩的影响。"
    "从一所学校抽取 30 名学生作为样本，在一个学期内使用新方法进行教学。"
    "结果显示，与上学期相比，考试成绩提高了 15%。"
    "研究得出结论：新教学方法能有效提升高中生的数学成绩。"
)

cot_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning=True,
    markdown=True,
)

deepseek_agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    reasoning_model=DeepSeek(id="deepseek-reasoner"),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 内置思维链（Chain Of Thought） ===")
    cot_agent.print_response(task, stream=True, show_full_reasoning=True)

    print("\n=== DeepSeek 推理模型 ===")
    deepseek_agent.print_response(task, stream=True, show_full_reasoning=True)
