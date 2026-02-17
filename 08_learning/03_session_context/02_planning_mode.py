"""
Session Context：计划模式（深入探讨）
==========================================
面向任务的 Session 的目标、计划和进度跟踪。

计划模式添加：
- 目标：用户试图实现的目标
- 计划：达到目标的步骤
- 进度：已完成的步骤

用于需要跟踪进度的任务导向 Agent。

对比：01_summary_mode.py 仅摘要（更快）。
另见：01_basics/3b_session_context_planning.py 了解基础知识。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, SessionContextConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    learning=LearningMachine(
        session_context=SessionContextConfig(
            enable_planning=True,  # 跟踪目标、计划、进度
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行：任务规划
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "deploy@example.com"
    session_id = "deploy_session"

    # Step 1: 陈述目标
    print("\n" + "=" * 60)
    print("STEP 1: 陈述目标")
    print("=" * 60 + "\n")

    agent.print_response(
        "I need to deploy a new Python web app to AWS. Help me plan this.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Step 2: 完成第一个任务
    print("\n" + "=" * 60)
    print("STEP 2: 第一个任务完成")
    print("=" * 60 + "\n")

    agent.print_response(
        "Done! I've created the Dockerfile and it builds successfully.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Step 3: 更多进度
    print("\n" + "=" * 60)
    print("STEP 3: 更多进度")
    print("=" * 60 + "\n")

    agent.print_response(
        "ECR repository is set up and I've pushed the image.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Step 4: 下一步是什么？
    print("\n" + "=" * 60)
    print("STEP 4: 下一步是什么？")
    print("=" * 60 + "\n")

    agent.print_response(
        "What should I do next?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)
