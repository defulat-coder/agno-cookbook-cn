"""
在 AgentOS 中展示推理 Agent 的示例。

你可以像平常一样与 Agent 交互。它会在提供最终答案之前进行推理。
你将看到它的思维链在生成时实时显示。
"""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.os import AgentOS
from agno.run.agent import RunEvent  # noqa

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 创建启用推理的 agent
agent = Agent(
    reasoning_model=Claude(
        id="claude-sonnet-4-5",
        thinking={"type": "enabled", "budget_tokens": 1024},
    ),
    reasoning=True,
    instructions="逐步思考问题。",
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="Reasoning model streaming",
    agents=[agent],
)
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """运行你的 AgentOS。

    你可以在以下地址查看配置和可用应用：
    http://localhost:7777/config

    """
    agent_os.serve(app="reasoning_model:app", reload=True)
