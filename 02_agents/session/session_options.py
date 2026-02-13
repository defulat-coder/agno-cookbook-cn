"""
Session 选项
=============================

演示 store_history_messages 选项的简单示例。
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.utils.pprint import pprint_run_response

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=SqliteDb(db_file="tmp/example_no_history.db"),
    add_history_to_context=True,  # 在执行期间使用历史
    num_history_runs=3,
    store_history_messages=False,  # 不在数据库中存储历史消息
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== First Run: Establishing context ===")
    response1 = agent.run("My name is Alice and I love Python programming.")
    pprint_run_response(response1)

    print("\n=== Second Run: Using history (but not storing it) ===")
    response2 = agent.run("What is my name and what do I love?")
    pprint_run_response(response2)

    # 检查存储的内容
    stored_run = agent.get_last_run_output()
    if stored_run and stored_run.messages:
        history_messages = [m for m in stored_run.messages if m.from_history]
        print("\n 存储信息:")
        print(f"   存储的消息总数: {len(stored_run.messages)}")
        print(f"   历史消息: {len(history_messages)} (已清除!)")
        print("\n 执行期间使用了历史（Agent 知道答案）")
        print("   但历史消息不会存储在数据库中！")
