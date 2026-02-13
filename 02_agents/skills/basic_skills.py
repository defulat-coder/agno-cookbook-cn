"""
基础 Skills
=============================

基础 Skills 示例。
"""

from pathlib import Path

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.skills import LocalSkills, Skills

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 获取相对于此文件的 skills 目录
skills_dir = Path(__file__).parent / "sample_skills"

# 创建一个从目录加载 skills 的 agent
agent = Agent(
    name="Code Review Agent",
    model=OpenAIChat(id="gpt-4o"),
    skills=Skills(loaders=[LocalSkills(str(skills_dir))]),
    instructions=[
        "你是一个有帮助的助手，可以访问专业的 skills。",
    ],
    markdown=True,
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 要求 agent 审查一些代码
    agent.print_response(
        "Review this Python code and provide feedback:\n\n"
        "```python\n"
        "def calculate_total(items):\n"
        "    total = 0\n"
        "    for i in range(len(items)):\n"
        "        total = total + items[i]['price'] * items[i]['quantity']\n"
        "    return total\n"
        "```"
    )
