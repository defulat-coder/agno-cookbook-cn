"""
Session Context：计划模式
==============================
Session Context 跟踪当前对话的状态：
- 已讨论的内容
- 当前目标及其状态
- 活动计划和进度

计划模式（enable_planning=True）添加结构化目标跟踪 -
摘要加上目标、计划步骤和进度标记。

对比：3a_session_context_summary.py 了解轻量级跟踪。
"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.learn import LearningMachine, SessionContextConfig
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 计划模式：除摘要外还跟踪目标、计划和进度。
# 适合需要结构化进度的任务导向对话。
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    db=db,
    instructions="Be very concise. Give brief, actionable answers.",
    learning=LearningMachine(
        session_context=SessionContextConfig(
            enable_planning=True,
        ),
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "planner@example.com"
    session_id = "deploy_app"

    # Turn 1: 设置明确步骤的目标
    print("\n" + "=" * 60)
    print("TURN 1: 设置目标")
    print("=" * 60 + "\n")

    agent.print_response(
        "Help me deploy a Python app to production. Give me 3 steps.",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 2: 完成第一步
    print("\n" + "=" * 60)
    print("TURN 2: 完成步骤 1")
    print("=" * 60 + "\n")

    agent.print_response(
        "Done with step 1. What's the command for step 2?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)

    # Turn 3: 完成第二步
    print("\n" + "=" * 60)
    print("TURN 3: 完成步骤 2")
    print("=" * 60 + "\n")

    agent.print_response(
        "Step 2 done. What's left?",
        user_id=user_id,
        session_id=session_id,
        stream=True,
    )
    agent.learning_machine.session_context_store.print(session_id=session_id)
