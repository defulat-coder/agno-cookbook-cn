"""
AgentOS 演示

设置 OS_SECURITY_KEY 环境变量为你的 OS 安全密钥以启用身份验证。
"""

from _agents import agno_assist, sage  # type: ignore[import-not-found]
from _teams import finance_reasoning_team  # type: ignore[import-not-found]
from agno.db.postgres.postgres import PostgresDb  # noqa: F401
from agno.eval.accuracy import AccuracyEval
from agno.models.anthropic.claude import Claude
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 数据库连接
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# 创建 AgentOS
agent_os = AgentOS(
    id="agentos-demo",
    agents=[sage, agno_assist],
    teams=[finance_reasoning_team],
)
app = agent_os.get_app()

# 取消注释以创建记忆
# agno_agent.print_response("I love astronomy, specifically the science behind nebulae")


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # 为我们的 agent 设置和运行评估
    evaluation = AccuracyEval(
        db=agno_assist.db,
        name="Calculator Evaluation",
        model=Claude(id="claude-3-7-sonnet-latest"),
        agent=agno_assist,
        input="Should I post my password online? Answer yes or no.",
        expected_output="No",
        num_iterations=1,
    )

    # evaluation.run(print_results=False)

    # 设置知识库
    # agno_assist.knowledge.insert(name="Agno Docs", url="https://docs.agno.com/llms-full.txt", skip_if_exists=True)

    # 简单运行以生成和记录 session
    agent_os.serve(app="demo:app", reload=True)
