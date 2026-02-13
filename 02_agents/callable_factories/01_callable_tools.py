"""
可调用工具工厂
======================
将函数作为 `tools` 传递而不是列表。该函数在每次运行开始时被调用，
因此工具集可以根据用户或会话而变化。

工厂通过签名检查接收命名参数：
- agent: Agent 实例
- run_context: 当前 RunContext（包含 user_id、session_id 等）
- session_state: 当前会话状态字典

结果默认按 user_id（或 session_id）缓存。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run import RunContext

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------


def search_web(query: str) -> str:
    """在网络上搜索信息。"""
    return f"Search results for: {query}"


def search_internal_docs(query: str) -> str:
    """搜索内部文档（仅管理员）。"""
    return f"Internal doc results for: {query}"


def get_account_balance(account_id: str) -> str:
    """获取账户余额（仅财务）。"""
    return f"Balance for {account_id}: $42,000"


# ---------------------------------------------------------------------------
# 可调用工厂
# ---------------------------------------------------------------------------


def tools_for_user(run_context: RunContext):
    """根据存储在 session_state 中的用户角色返回不同的工具。"""
    role = (run_context.session_state or {}).get("role", "viewer")
    print(f"--> Resolving tools for role: {role}")

    base_tools = [search_web]
    if role == "admin":
        base_tools.append(search_internal_docs)
    if role in ("admin", "finance"):
        base_tools.append(get_account_balance)

    return base_tools


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=tools_for_user,
    instructions=[
        "你是一个乐于助人的助手。",
        "使用可用的工具来回答用户的问题。",
    ],
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 运行 1: viewer 角色 - 仅 search_web 可用
    # 每个 user_id 获取自己的缓存工具集
    print("=== Run as viewer ===")
    agent.print_response(
        "Search for recent news about AI agents",
        user_id="viewer_user",
        session_state={"role": "viewer"},
        stream=True,
    )

    # 运行 2: admin 角色 - 所有工具可用
    # 不同的 user_id 意味着工厂将使用新上下文再次调用
    print("\n=== Run as admin ===")
    agent.print_response(
        "Search internal docs for the deployment guide and check account balance for ACC-001",
        user_id="admin_user",
        session_state={"role": "admin"},
        stream=True,
    )
