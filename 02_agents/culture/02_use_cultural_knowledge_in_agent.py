"""
02 在 Agent 中使用文化知识
=============================

在你的 Agents 中使用文化知识。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude

# ---------------------------------------------------------------------------
# 步骤 1. 初始化数据库（与 01_create_cultural_knowledge.py 中使用的相同）
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/demo.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# Agent 会自动加载共享的文化知识（例如，如何格式化响应、
# 如何编写教程，或语调/风格偏好）。
agent = Agent(
    model=Claude(id="claude-sonnet-4-5"),
    db=db,
    # 此标志将把文化知识添加到 agent 的上下文中：
    add_culture_to_context=True,
    # 此标志将在每次运行后更新文化知识：
    # update_cultural_knowledge=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # （可选）快速 A/B 切换以展示没有文化知识的差异：
    # agent_no_culture = Agent(model=Claude(id="claude-sonnet-4-5"))

    # ---------------------------------------------------------------------------
    # 步骤 3. 让 Agent 生成受益于文化知识的响应
    # ---------------------------------------------------------------------------
    # 如果 `01_create_cultural_knowledge.py` 添加了如下原则：
    #   "以代码示例开始技术解释，然后是推理"
    # Agent 将在此应用该原则，从具体的 FastAPI 示例开始。
    print("\n=== 使用文化知识 ===\n")
    agent.print_response(
        "如何使用 Docker 设置 FastAPI 服务？",
        stream=True,
        markdown=True,
    )

    # （可选）运行不带文化知识的对比：
    # print("\n=== 不使用文化知识 ===\n")
    # agent_no_culture.print_response("如何使用 Docker 设置 FastAPI 服务？", stream=True, markdown=True)
