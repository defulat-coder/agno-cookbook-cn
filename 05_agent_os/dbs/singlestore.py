"""展示如何在 AgentOS 中使用 SingleStore 作为我们的数据库提供商的示例"""

from agno.agent import Agent
from agno.db.singlestore import SingleStoreDb
from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

SINGLE_STORE_DB_URL = "mysql+pymysql://root:ai@localhost:3306/ai"

# 设置 SingleStore 数据库
db = SingleStoreDb(
    db_url=SINGLE_STORE_DB_URL,
    session_table="sessions",
    eval_table="eval_runs",
    memory_table="user_memories",
    metrics_table="metrics",
)

# 设置基本 agent 和基本团队
agent = Agent(
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
team = Team(
    id="basic-team",
    name="Team Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    members=[agent],
    debug_mode=True,
)

# 评估
evaluation = AccuracyEval(
    db=db,
    name="Calculator Evaluation",
    model=OpenAIChat(id="gpt-4o"),
    agent=agent,
    input="Should I post my password online? Answer yes or no.",
    expected_output="No",
    num_iterations=1,
)
# evaluation.run(print_results=True)

agent_os = AgentOS(
    description="示例 OS 设置",
    agents=[agent],
    teams=[team],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent.run("记住我最喜欢的颜色是深绿色")
    agent_os.serve(app="singlestore:app", reload=True)
