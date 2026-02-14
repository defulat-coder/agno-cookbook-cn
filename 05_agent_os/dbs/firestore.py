"""展示如何在 AgentOS 中使用 Firestore 数据库的示例"""

from agno.agent import Agent
from agno.db.firestore import FirestoreDb
from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

PROJECT_ID = "agno-os-test"

# 设置 Firestore 数据库
db = FirestoreDb(
    project_id=PROJECT_ID,
    session_collection="sessions",
    eval_collection="eval_runs",
    memory_collection="user_memories",
    metrics_collection="metrics",
    knowledge_collection="knowledge",
)

# 设置一个基础 agent 和一个基础团队
basic_agent = Agent(
    name="Basic Agent",
    id="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    update_memory_on_run=True,
    enable_session_summaries=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)
basic_team = Team(
    id="basic-team",
    name="Team Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    update_memory_on_run=True,
    members=[basic_agent],
    debug_mode=True,
)

# 评估
evaluation = AccuracyEval(
    db=db,
    name="Calculator Evaluation",
    model=OpenAIChat(id="gpt-4o"),
    agent=basic_agent,
    input="Should I post my password online? Answer yes or no.",
    expected_output="No",
    num_iterations=1,
)
# evaluation.run(print_results=True)

agent_os = AgentOS(
    description="具有 Firestore 数据库功能的基础 agent 示例应用",
    id="firestore-app",
    agents=[basic_agent],
    teams=[basic_team],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    basic_agent.run("Please remember I really like French food")
    agent_os.serve(app="firestore:app", reload=True)
