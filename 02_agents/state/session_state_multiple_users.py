"""
Session State 多用户示例
=============================

此示例演示如何在多用户环境中为每个用户维护状态。
"""

import json

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run import RunContext

# 内存数据库用于存储用户购物清单
# 按用户 ID 和会话 ID 组织
shopping_list = {}


def add_item(run_context: RunContext, item: str) -> str:
    """向当前用户的购物清单添加一个商品。"""

    current_user_id = run_context.session_state["current_user_id"]
    current_session_id = run_context.session_state["current_session_id"]
    shopping_list.setdefault(current_user_id, {}).setdefault(
        current_session_id, []
    ).append(item)

    return f"Item {item} added to the shopping list"


def remove_item(run_context: RunContext, item: str) -> str:
    """从当前用户的购物清单中删除一个商品。"""

    current_user_id = run_context.session_state["current_user_id"]
    current_session_id = run_context.session_state["current_session_id"]

    if (
        current_user_id not in shopping_list
        or current_session_id not in shopping_list[current_user_id]
    ):
        return f"No shopping list found for user {current_user_id} and session {current_session_id}"

    if item not in shopping_list[current_user_id][current_session_id]:
        return f"Item '{item}' not found in the shopping list for user {current_user_id} and session {current_session_id}"

    shopping_list[current_user_id][current_session_id].remove(item)
    return f"Item {item} removed from the shopping list"


def get_shopping_list(run_context: RunContext) -> str:
    """获取当前用户的购物清单。"""

    if run_context.session_state is None:
        run_context.session_state = {}

    current_user_id = run_context.session_state["current_user_id"]
    current_session_id = run_context.session_state["current_session_id"]
    return f"Shopping list for user {current_user_id} and session {current_session_id}: \n{json.dumps(shopping_list[current_user_id][current_session_id], indent=2)}"


# 创建一个维护状态的 Agent
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=SqliteDb(db_file="tmp/data.db"),
    tools=[add_item, remove_item, get_shopping_list],
    # 引用内存数据库
    instructions=[
        "Current User ID: {current_user_id}",
        "Current Session ID: {current_session_id}",
    ],
    markdown=True,
)

user_id_1 = "john_doe"
user_id_2 = "mark_smith"
user_id_3 = "carmen_sandiago"

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 使用示例
    agent.print_response(
        "Add milk, eggs, and bread to the shopping list",
        stream=True,
        user_id=user_id_1,
        session_id="user_1_session_1",
    )
    agent.print_response(
        "Add tacos to the shopping list",
        stream=True,
        user_id=user_id_2,
        session_id="user_2_session_1",
    )
    agent.print_response(
        "Add apples and grapes to the shopping list",
        stream=True,
        user_id=user_id_3,
        session_id="user_3_session_1",
    )
    agent.print_response(
        "Remove milk from the shopping list",
        stream=True,
        user_id=user_id_1,
        session_id="user_1_session_1",
    )
    agent.print_response(
        "Add minced beef to the shopping list",
        stream=True,
        user_id=user_id_2,
        session_id="user_2_session_1",
    )

    # Mark Smith 的购物清单上有什么？
    agent.print_response(
        "What is on Mark Smith's shopping list?",
        stream=True,
        user_id=user_id_2,
        session_id="user_2_session_1",
    )

    # 新会话，所以是新购物清单
    agent.print_response(
        "Add chicken and soup to my list.",
        stream=True,
        user_id=user_id_2,
        session_id="user_3_session_2",
    )

    print(f"Final shopping lists: \n{json.dumps(shopping_list, indent=2)}")
