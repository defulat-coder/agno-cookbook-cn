"""SurrealDB + AgentOS 演示

步骤：
    1. 在容器中运行 SurrealDB：`./cookbook/scripts/run_surrealdb.sh`
    2. 运行演示：`python cookbook/agent_os/dbs/surreal_db/run.py`
"""

from agents import agno_assist
from agno.os import AgentOS
from teams import reasoning_finance_team
from workflows import research_workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# ************* 创建 AgentOS *************
agent_os = AgentOS(
    description="SurrealDB AgentOS",
    agents=[agno_assist],
    teams=[reasoning_finance_team],
    workflows=[research_workflow],
)
# 获取 AgentOS 的 FastAPI 应用
app = agent_os.get_app()
# *******************************

# ************* 运行 AgentOS *************
# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="run:app", reload=True)
# *******************************
