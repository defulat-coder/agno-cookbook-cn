"""
结构化输出
=================

演示结构化输出。
"""

from typing import List

from agno.agent.agent import Agent
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


class MovieScript(BaseModel):
    setting: str = Field(
        ..., description="Provide a nice setting for a blockbuster movie."
    )
    ending: str = Field(
        ...,
        description="Ending of the movie. If not available, provide a happy ending.",
    )
    genre: str = Field(
        ...,
        description="Genre of the movie. If not available, select action, thriller or romantic comedy.",
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(
        ..., description="3 sentence storyline for the movie. Make it exciting!"
    )


structured_agent = Agent(
    name="structured-output-agent",
    id="structured_output_agent",
    model=OpenAIChat(id="gpt-4o"),
    description="一个创意AI编剧，生成详细、结构良好的电影剧本，包含引人入胜的场景、角色、故事线和完整的情节弧线，以标准化格式呈现",
    markdown=True,
    output_schema=MovieScript,
)


# 设置你的 AgentOS 应用
agent_os = AgentOS(
    agents=[structured_agent],
    a2a_interface=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """使用 A2A 接口运行你的 AgentOS。
    你可以通过 A2A 协议运行 Agent：
    POST http://localhost:7777/agents/{id}/v1/message:send
    对于流式响应：
    POST http://localhost:7777/agents/{id}/v1/message:stream
    在以下地址检索 agent 卡片：
    GET  http://localhost:7777/agents/{id}/.well-known/agent-card.json
    """
    agent_os.serve(app="structured_output:app", port=7777, reload=True)
