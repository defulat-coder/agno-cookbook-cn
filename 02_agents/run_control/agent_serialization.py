"""
Agent 序列化
=============================

Agent 序列化。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
agent_db = SqliteDb(db_file="tmp/agents.db")

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    id="serialization-demo-agent",
    name="Serialization Demo Agent",
    model=OpenAIResponses(id="gpt-5.2"),
    db=agent_db,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    config = agent.to_dict()
    recreated = Agent.from_dict(config)

    version = agent.save()
    loaded = Agent.load(id=agent.id, db=agent_db, version=version)

    recreated.print_response("Say hello from a recreated agent.", stream=True)
    loaded.print_response("Say hello from a loaded agent.", stream=True)
