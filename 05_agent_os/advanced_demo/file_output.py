"""
File Output
===========

演示文件输出。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.tools.file_generation import FileGenerationTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db = SqliteDb(db_file="tmp/agentos.db")

file_agent = Agent(
    name="File Output Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    send_media_to_model=False,
    tools=[FileGenerationTools(output_directory="tmp")],
    instructions="直接按原样返回文件 URL，不做任何其他操作。",
)

agent_os = AgentOS(
    id="agentos-demo",
    agents=[file_agent],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="file_output:app", reload=True)
