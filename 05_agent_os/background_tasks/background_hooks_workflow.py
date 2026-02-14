"""
示例：AgentOS 中工作流的后台钩子

此示例演示如何在工作流中使用后台钩子。
后台钩子在 API 响应发送后执行，使其非阻塞。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.run.agent import RunOutput
from agno.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def log_step_completion(run_output: RunOutput, agent: Agent) -> None:
    """
    agent 上的后台 post-hook，在每个步骤完成后运行。
    """
    print(f"[Background Hook] Agent '{agent.name}' completed step")
    print(f"[Background Hook] Run ID: {run_output.run_id}")

    # 模拟异步工作
    await asyncio.sleep(1)
    print(f"[Background Hook] Logged metrics for {agent.name}")


# 为工作流步骤创建 agent
analyzer = Agent(
    name="Analyzer",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="分析输入并识别关键点。",
    post_hooks=[log_step_completion],
)

summarizer = Agent(
    name="Summarizer",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="将分析总结为简短的响应。",
    post_hooks=[log_step_completion],
)

# 创建工作流
analysis_workflow = Workflow(
    id="analysis-workflow",
    name="AnalysisWorkflow",
    description="分析输入并提供摘要",
    steps=[analyzer, summarizer],
    db=AsyncSqliteDb(db_file="tmp/workflow.db"),
)

# 创建启用后台钩子的 AgentOS
agent_os = AgentOS(
    workflows=[analysis_workflow],
    run_hooks_in_background=True,
)

app = agent_os.get_app()

# 示例请求：
# curl -X POST http://localhost:7777/workflows/analysis-workflow/runs \
#   -F "message=Explain the benefits of exercise" \
#   -F "stream=false"

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="background_hooks_workflow:app", port=7777, reload=True)
