"""
Session State 手动更新示例
=============================

Session State 手动更新。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run import RunContext


def add_item(run_context: RunContext, item: str) -> str:
    """向购物清单添加一个商品。"""
    if run_context.session_state is None:
        run_context.session_state = {}

    run_context.session_state["shopping_list"].append(item)  # type: ignore
    return f"The shopping list is now {run_context.session_state['shopping_list']}"  # type: ignore


# 创建一个维护状态的 Agent
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    # 使用空购物清单初始化 session state（这是所有用户的默认 session state）
    session_state={"shopping_list": []},
    db=SqliteDb(db_file="tmp/agents.db"),
    tools=[add_item],
    # 你可以在 instructions 中使用 session state 的变量
    instructions="Current state (shopping list) is: {shopping_list}",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 使用示例
    agent.print_response("Add milk, eggs, and bread to the shopping list", stream=True)

    current_session_state = agent.get_session_state()
    current_session_state["shopping_list"].append("chocolate")
    agent.update_session_state(current_session_state)

    agent.print_response("What's on my list?", stream=True, debug_mode=True)

    print(f"Final session state: {agent.get_session_state()}")
