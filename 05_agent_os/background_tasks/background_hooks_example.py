"""
示例：在 AgentOS 中使用后台 Post-Hook

此示例演示如何将 post-hook 作为 FastAPI 后台任务运行，
使其完全非阻塞。
"""

import asyncio

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.run.agent import RunInput

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


# 用于记录请求的 Pre-hook
def log_request(run_input: RunInput, agent):
    """
    此 pre-hook 将在 agent 处理请求之前在后台运行。
    注意：后台模式下的 Pre-hook 无法修改 run_input。
    """
    print(f"[Background Pre-Hook] Request received for agent: {agent.name}")
    print(f"[Background Pre-Hook] Input: {run_input.input_content}")


# 用于记录分析的 Post-hook
async def log_analytics(run_output, agent, session):
    """
    此 post-hook 将在响应发送给用户后在后台运行。
    它不会阻塞 API 响应。
    """
    print(f"[Background Post-Hook] Logging analytics for run: {run_output.run_id}")
    print(f"[Background Post-Hook] Agent: {agent.name}")
    print(f"[Background Post-Hook] Session: {session.session_id}")

    # 模拟 2 秒的延迟
    await asyncio.sleep(2)
    print("[Background Post-Hook] Analytics logged successfully!")


# 用于发送通知的另一个 post-hook
async def send_notification(run_output, agent):
    """
    另一个发送通知而不阻塞响应的后台任务。
    """
    print(f"[Background Post-Hook] Sending notification for agent: {agent.name}")
    # 模拟 3 秒的延迟
    await asyncio.sleep(3)
    print("[Background Post-Hook] Notification sent!")


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
    # 为钩子启用后台模式（如果禁用，钩子将在主线程中运行）
    run_hooks_in_background=True,
)

# 获取 FastAPI 应用
app = agent_os.get_app()


# 当你向 POST /agents/{agent_id}/runs 发出请求时：
# 1. agent 将处理请求
# 2. 响应将立即发送给用户
# 3. pre-hook (log_request) 和 post-hook (log_analytics, send_notification) 将在后台运行
# 4. 用户不必等待这些任务完成

# 示例请求：
# curl -X POST http://localhost:8000/agents/background-task-agent/runs \
#   -F "message=Hello, how are you?" \
#   -F "stream=false"

# 响应将立即返回，而 log_request、log_analytics 和 send_notification
# 继续在后台运行，不会阻塞 API 响应。

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="background_hooks_example:app", port=7777, reload=True)
