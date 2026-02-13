"""
Session State 高级示例
=============================

Session State 高级用法。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run import RunContext


# 定义管理购物清单的工具函数
def add_item(run_context: RunContext, item: str) -> str:
    """向购物清单添加一个商品并返回确认信息。"""
    # 如果商品不在清单中则添加
    if run_context.session_state is None:
        run_context.session_state = {}

    if item.lower() not in [
        i.lower() for i in run_context.session_state["shopping_list"]
    ]:
        run_context.session_state["shopping_list"].append(item)  # type: ignore
        return f"Added '{item}' to the shopping list"
    else:
        return f"'{item}' is already in the shopping list"


def remove_item(run_context: RunContext, item: str) -> str:
    """从购物清单中按名称删除一个商品。"""
    if run_context.session_state is None:
        run_context.session_state = {}

    # 不区分大小写的搜索
    for i, list_item in enumerate(run_context.session_state["shopping_list"]):
        if list_item.lower() == item.lower():
            run_context.session_state["shopping_list"].pop(i)
            return f"Removed '{list_item}' from the shopping list"

    return f"'{item}' was not found in the shopping list"


def list_items(run_context: RunContext) -> str:
    """列出购物清单中的所有商品。"""
    if run_context.session_state is None:
        run_context.session_state = {}

    shopping_list = run_context.session_state["shopping_list"]

    if not shopping_list:
        return "The shopping list is empty."

    items_text = "\n".join([f"- {item}" for item in shopping_list])
    return f"Current shopping list:\n{items_text}"


# 创建一个维护状态的购物清单管理 Agent
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="o3-mini"),
    # 使用空购物清单初始化 session state（所有会话的默认 session state）
    session_state={"shopping_list": []},
    db=SqliteDb(db_file="tmp/example.db"),
    tools=[add_item, remove_item, list_items],
    # 你可以在 instructions 中使用 session state 的变量
    instructions=dedent("""\
        Your job is to manage a shopping list.

        The shopping list starts empty. You can add items, remove items by name, and list all items.

        Current shopping list: {shopping_list}
    """),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 使用示例
    agent.print_response("Add milk, eggs, and bread to the shopping list", stream=True)
    print(f"Session state: {agent.get_session_state()}")

    agent.print_response("I got bread", stream=True)
    print(f"Session state: {agent.get_session_state()}")

    agent.print_response("I need apples and oranges", stream=True)
    print(f"Session state: {agent.get_session_state()}")

    agent.print_response("whats on my list?", stream=True)
    print(f"Session state: {agent.get_session_state()}")

    agent.print_response(
        "Clear everything from my list and start over with just bananas and yogurt",
        stream=True,
    )
    print(f"Session state: {agent.get_session_state()}")
