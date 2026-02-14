"""
与 Agent 共享状态
================

演示在 Agent 工具调用之间共享可变的工作流会话状态。
"""

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai.chat import OpenAIChat
from agno.run import RunContext
from agno.workflow.step import Step
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建数据库
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="tmp/workflow.db")


# ---------------------------------------------------------------------------
# 定义会话状态工具
# ---------------------------------------------------------------------------
def add_item(run_context: RunContext, item: str) -> str:
    if run_context.session_state is None:
        run_context.session_state = {}

    existing_items = [
        existing_item.lower()
        for existing_item in run_context.session_state["shopping_list"]
    ]
    if item.lower() not in existing_items:
        run_context.session_state["shopping_list"].append(item)
        return f"Added '{item}' to the shopping list."
    return f"'{item}' is already in the shopping list."


def remove_item(run_context: RunContext, item: str) -> str:
    if run_context.session_state is None:
        run_context.session_state = {}

    if len(run_context.session_state["shopping_list"]) == 0:
        return f"Shopping list is empty. Cannot remove '{item}'."

    shopping_list = run_context.session_state["shopping_list"]
    for i, existing_item in enumerate(shopping_list):
        if existing_item.lower() == item.lower():
            removed_item = shopping_list.pop(i)
            return f"Removed '{removed_item}' from the shopping list."

    return f"'{item}' not found in the shopping list."


def remove_all_items(run_context: RunContext) -> str:
    if run_context.session_state is None:
        run_context.session_state = {}

    run_context.session_state["shopping_list"] = []
    return "Removed all items from the shopping list."


def list_items(run_context: RunContext) -> str:
    if run_context.session_state is None:
        run_context.session_state = {}

    if len(run_context.session_state["shopping_list"]) == 0:
        return "Shopping list is empty."

    items = run_context.session_state["shopping_list"]
    items_str = "\n".join([f"- {item}" for item in items])
    return f"Shopping list:\n{items_str}"


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
shopping_assistant = Agent(
    name="Shopping Assistant",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[add_item, remove_item, list_items],
    instructions=[
        "你是一个乐于助人的购物助手。",
        "你可以帮助用户通过添加、删除和列出项目来管理购物清单。",
        "始终使用提供的工具与购物清单交互。",
        "在你的响应中友好且乐于助人。",
    ],
)

list_manager = Agent(
    name="List Manager",
    model=OpenAIChat(id="gpt-5.2"),
    tools=[list_items, remove_all_items],
    instructions=[
        "你是一个列表管理专家。",
        "你可以查看当前购物清单并在需要时清空它。",
        "在被问及时始终显示当前列表。",
        "向用户清楚地确认操作。",
    ],
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
manage_items_step = Step(
    name="manage_items",
    description="Help manage shopping list items (add/remove)",
    agent=shopping_assistant,
)

view_list_step = Step(
    name="view_list",
    description="View and manage the complete shopping list",
    agent=list_manager,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
shopping_workflow = Workflow(
    name="Shopping List Workflow",
    db=db,
    steps=[manage_items_step, view_list_step],
    session_state={"shopping_list": []},
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 示例 1：添加项目 ===")
    shopping_workflow.print_response(
        input="Please add milk, bread, and eggs to my shopping list."
    )
    print("工作流会话状态：", shopping_workflow.get_session_state())

    print("\n=== 示例 2：添加更多项目 ===")
    shopping_workflow.print_response(
        input="Add apples and bananas to the list, then show me the complete list."
    )
    print("工作流会话状态：", shopping_workflow.get_session_state())

    print("\n=== 示例 3：删除项目 ===")
    shopping_workflow.print_response(
        input="Remove bread from the list and show me what's left."
    )
    print("工作流会话状态：", shopping_workflow.get_session_state())

    print("\n=== 示例 4：清空列表 ===")
    shopping_workflow.print_response(
        input="Clear the entire shopping list and confirm it's empty."
    )
    print("最终工作流会话状态：", shopping_workflow.get_session_state())
