"""创建会话并使用 AgentOS 和 SessionApp 公开它的简单示例"""

from agno.agent import Agent
from agno.db.postgres.postgres import PostgresDb
from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team
from agno.tools.calculator import CalculatorTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"
db = PostgresDb(db_url=db_url)

# 设置 agent
basic_agent = Agent(
    id="basic-agent",
    name="Calculator Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    markdown=True,
    instructions="你是一个可以回答算术问题的助手。始终使用你拥有的计算器工具。",
    tools=[CalculatorTools()],
)

basic_team = Team(
    name="Basic Team",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    members=[basic_agent],
)

# 为我们的 agent 设置并运行评估
evaluation = AccuracyEval(
    db=db,  # 将数据库传递给评估。结果将存储在数据库中。
    name="Calculator Evaluation",
    model=OpenAIChat(id="gpt-4o"),
    input="Should I post my password online? Answer yes or no.",
    expected_output="No",
    num_iterations=1,
    # 要评估的 Agent 或团队：
    agent=basic_agent,
    # team=basic_team,
)
# evaluation.run(print_results=True)

# 设置 Agno API 应用
agent_os = AgentOS(
    description="具有评估功能的基础 agent 示例应用",
    id="eval-demo",
    agents=[basic_agent],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """ 运行你的 AgentOS：
    现在你可以使用 API 与评估运行进行交互。示例：
    - http://localhost:8001/eval/{index}/eval-runs
    - http://localhost:8001/eval/{index}/eval-runs/123
    - http://localhost:8001/eval/{index}/eval-runs?agent_id=123
    - http://localhost:8001/eval/{index}/eval-runs?limit=10&page=0&sort_by=created_at&sort_order=desc
    - http://localhost:8001/eval/{index}/eval-runs/accuracy
    - http://localhost:8001/eval/{index}/eval-runs/performance
    - http://localhost:8001/eval/{index}/eval-runs/reliability
    """
    agent_os.serve(app="evals_demo:app", reload=True)
