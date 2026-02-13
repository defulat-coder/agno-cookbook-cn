"""
Session State 工具
===================
在工厂中使用 `session_state` 作为参数名来直接接收会话状态字典
（无需 run_context）。

设置 `cache_callables=False` 以便工厂每次都重新运行，
捕获运行之间的任何 session_state 变化。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# ---------------------------------------------------------------------------
# 工具
# ---------------------------------------------------------------------------


def get_greeting(name: str) -> str:
    """用名字问候某人。"""
    return f"Hello, {name}!"


def get_farewell(name: str) -> str:
    """向某人道别。"""
    return f"Goodbye, {name}!"


def get_tools(session_state: dict):
    """根据 session_state 中的 'mode' 键选择工具。"""
    mode = session_state.get("mode", "greet")
    print(f"--> Factory resolved mode: {mode}")

    if mode == "greet":
        return [get_greeting]
    else:
        return [get_farewell]


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=get_tools,
    cache_callables=False,
    instructions=["使用可用的工具来响应。"],
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Greet mode ===")
    agent.print_response(
        "Say hi to Alice",
        session_state={"mode": "greet"},
        stream=True,
    )

    print("\n=== Farewell mode ===")
    agent.print_response(
        "Say bye to Alice",
        session_state={"mode": "farewell"},
        stream=True,
    )
