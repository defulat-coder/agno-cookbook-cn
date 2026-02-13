"""
Agent OS - Agent 的 Web 界面
=========================================
本文件启动一个 Agent OS 服务器，为本快速入门指南中的
所有 Agent、团队和工作流提供 Web 界面。

什么是 Agent OS？
-----------------
Agent OS 是 Agno 的运行时，让你可以：
- 通过美观的 Web UI 与 Agent 对话
- 浏览会话历史
- 监控追踪信息并调试 Agent 行为
- 管理知识库和记忆
- 在 Agent、团队和工作流之间切换

使用方法
----------
1. 启动服务器：
   python cookbook/00_quickstart/run.py

2. 在浏览器中访问 https://os.agno.com

3. 添加你的本地端点：http://localhost:7777

4. 选择任意 Agent、团队或工作流并开始对话

前置条件
-------------
- 本快速入门中的所有 Agent 会自动注册
- 对于知识库 Agent，需要先加载知识库：
  python cookbook/00_quickstart/agent_search_over_knowledge.py

了解更多
----------
- Agent OS 概览：https://docs.agno.com/agent-os/overview
- Agno 文档：https://docs.agno.com
"""

from pathlib import Path

from agent_search_over_knowledge import agent_with_knowledge
from agent_with_guardrails import agent_with_guardrails
from agent_with_memory import agent_with_memory
from agent_with_state_management import agent_with_state_management
from agent_with_storage import agent_with_storage
from agent_with_structured_output import agent_with_structured_output
from agent_with_tools import agent_with_tools
from agent_with_typed_input_output import agent_with_typed_input_output
from agno.os import AgentOS
from custom_tool_for_self_learning import self_learning_agent
from human_in_the_loop import human_in_the_loop_agent
from multi_agent_team import multi_agent_team
from sequential_workflow import sequential_workflow

# ---------------------------------------------------------------------------
# AgentOS 配置
# ---------------------------------------------------------------------------
config_path = str(Path(__file__).parent.joinpath("config.yaml"))

# ---------------------------------------------------------------------------
# 创建 AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="Quick Start AgentOS",
    agents=[
        agent_with_tools,
        agent_with_storage,
        agent_with_knowledge,
        self_learning_agent,
        agent_with_structured_output,
        agent_with_typed_input_output,
        agent_with_memory,
        agent_with_state_management,
        human_in_the_loop_agent,
        agent_with_guardrails,
    ],
    teams=[multi_agent_team],
    workflows=[sequential_workflow],
    config=config_path,
    tracing=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行 AgentOS
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent_os.serve(app="run:app", reload=True)
