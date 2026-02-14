"""
示例：在 AgentOS 中使用后台 Post-Hook

此示例演示如何将 post-hook 作为 FastAPI 后台任务运行，
使其完全非阻塞。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.hooks.decorator import hook
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.run.agent import RunInput

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


@hook(run_in_background=True)
def log_request(run_input: RunInput, agent):
    """
    此 pre-hook 将在 agent 处理请求之前在后台运行。
    注意：后台模式下的 Pre-hook 无法修改 run_input。
    """
    print(f"[Background Pre-Hook] Request received for agent: {agent.name}")
    print(f"[Background Pre-Hook] Input: {run_input.input_content}")


async def log_analytics(run_output, agent, session):
    """
    用于记录分析的 Post hook
    """
    print(f"[Post-Hook] Logging analytics for run: {run_output.run_id}")
    print(f"[Post-Hook] Agent: {agent.name}")
    print(f"[Post-Hook] Session: {session.session_id}")
    print("[Post-Hook] Analytics logged successfully!")


@hook(run_in_background=True)
async def send_notification(run_output, agent):
    """
    用于发送通知的 Post hook
    """
    print(f"[Post-Hook] Sending notification for agent: {agent.name}")
    await asyncio.sleep(3)
    print("[Post-Hook] Notification sent!")


# 创建启用后台 post-hook 的 agent
agent = Agent(
    id="background-task-agent",
    name="BackgroundTaskAgent",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="你是一个有用的助手",
    db=AsyncSqliteDb(db_file="tmp/agent.db"),
    # 定义钩子
    pre_hooks=[log_request],
    post_hooks=[log_analytics, send_notification],
    markdown=True,
)

# 创建 AgentOS
agent_os = AgentOS(
    agents=[agent],
)

# 获取 FastAPI 应用
app = agent_os.get_app()


# 当你向 POST /agents/{agent_id}/runs 发出请求时：
# 1. agent 将处理请求
# 2. 响应将立即发送给用户，log_analytics 在正常执行流程中执行
# 3. pre-hook (log_request) 和 post-hook (send_notification) 将在后台运行，不会阻塞 API 响应
# 4. 用户不必等待这些任务完成

# 示例请求：
# curl -X POST http://localhost:8000/agents/background-task-agent/runs \
#   -F "message=Hello, how are you?" \
#   -F "stream=false"

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="background_hooks_decorator:app", port=7777, reload=True)
