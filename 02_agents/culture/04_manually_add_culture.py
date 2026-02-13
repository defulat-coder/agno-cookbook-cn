"""
04 手动添加文化知识
=============================

手动向你的 Agents 添加文化知识。
"""

from agno.agent import Agent
from agno.culture.manager import CultureManager
from agno.db.schemas.culture import CulturalKnowledge
from agno.db.sqlite import SqliteDb
from agno.models.anthropic import Claude
from rich.pretty import pprint

# ---------------------------------------------------------------------------
# 步骤 1. 初始化用于存储文化知识的数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/demo.db")

# ---------------------------------------------------------------------------
# 步骤 2. 创建文化管理器（手动插入无需模型）
# ---------------------------------------------------------------------------
culture_manager = CultureManager(db=db)

# ---------------------------------------------------------------------------
# 步骤 3. 手动添加文化知识
# ---------------------------------------------------------------------------
# 示例：响应格式标准（简短且可操作）
response_format = CulturalKnowledge(
    name="响应格式标准（Agno）",
    summary="保持响应简洁、可扫描，并在适用时优先提供可运行的内容。",
    categories=["communication", "ux"],
    content=(
        "- 在可能的情况下，优先提供最小可运行的代码片段或示例。\n"
        "- 对于过程使用编号步骤；保持每个步骤可测试。\n"
        "- 优先使用公制单位和明确的默认值（端口、路径、版本）。\n"
        "- 以简短的验证清单结束。"
    ),
    notes=["源自重复反馈，支持可操作的答案。"],
    metadata={"source": "manual_seed", "version": 1},
)

# 持久化文化知识
culture_manager.add_cultural_knowledge(response_format)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 可选：显示存储的内容
    print("\n=== 文化知识（手动添加）===")
    pprint(culture_manager.get_all_knowledge())

    # ---------------------------------------------------------------------------
    # 步骤 4. 初始化启用文化知识的 Agent
    # ---------------------------------------------------------------------------
    # Agent 将加载共享的文化知识并将其包含在上下文中。
    agent = Agent(
        db=db,
        model=Claude(id="claude-sonnet-4-5"),
        add_culture_to_context=True,  # 将文化知识添加到提示上下文中
        # update_cultural_knowledge=True,  # 取消注释以让 agent 在运行后更新文化知识
    )

    # （可选）不带文化知识的 A/B 对比：
    # agent_no_culture = Agent(model=Claude(id="claude-sonnet-4-5"))

    # ---------------------------------------------------------------------------
    # 步骤 5. 让 Agent 生成受益于文化知识的响应
    # ---------------------------------------------------------------------------
    print("\n=== 使用文化知识 ===\n")
    agent.print_response(
        "如何使用 Docker 设置 FastAPI 服务？",
        stream=True,
        markdown=True,
    )

    # （可选）运行不带文化知识的对比：
    # print("\n=== 不使用文化知识 ===\n")
    # agent_no_culture.print_response(
    #     "如何使用 Docker 设置 FastAPI 服务？",
    #     stream=True,
    #     markdown=True,
    # )
