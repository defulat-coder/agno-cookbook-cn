"""
取消运行
=============================

演示如何取消正在运行的 agent 执行的示例。
"""

import threading
import time

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.run.agent import RunEvent
from agno.run.base import RunStatus


def long_running_task(agent: Agent, run_id_container: dict):
    """
    模拟一个可以被取消的长时间运行的 agent 任务。

    Args:
        agent: 要运行的 agent
        run_id_container: 用于存储 run_id 以便取消的字典

    Returns:
        包含运行结果和状态的字典
    """
    try:
        # 启动 agent 运行 - 这模拟了一个长任务
        final_response = None
        content_pieces = []

        for chunk in agent.run(
            "Write a very long story about a dragon who learns to code. "
            "Make it at least 2000 words with detailed descriptions and dialogue. "
            "Take your time and be very thorough.",
            stream=True,
        ):
            if "run_id" not in run_id_container and chunk.run_id:
                run_id_container["run_id"] = chunk.run_id

            if chunk.event == RunEvent.run_content:
                print(chunk.content, end="", flush=True)
                content_pieces.append(chunk.content)
            # 当运行被取消时，会触发 `RunEvent.run_cancelled` 事件
            elif chunk.event == RunEvent.run_cancelled:
                print(f"\n[CANCELLED] Run was cancelled: {chunk.run_id}")
                run_id_container["result"] = {
                    "status": "cancelled",
                    "run_id": chunk.run_id,
                    "cancelled": True,
                    "content": "".join(content_pieces)[:200] + "..."
                    if content_pieces
                    else "No content before cancellation",
                }
                return
            elif hasattr(chunk, "status") and chunk.status == RunStatus.completed:
                final_response = chunk

        # 如果执行到这里，说明运行成功完成
        if final_response:
            run_id_container["result"] = {
                "status": final_response.status.value
                if final_response.status
                else "completed",
                "run_id": final_response.run_id,
                "cancelled": final_response.status == RunStatus.cancelled,
                "content": ("".join(content_pieces)[:200] + "...")
                if content_pieces
                else "No content",
            }
        else:
            run_id_container["result"] = {
                "status": "unknown",
                "run_id": run_id_container.get("run_id"),
                "cancelled": False,
                "content": ("".join(content_pieces)[:200] + "...")
                if content_pieces
                else "No content",
            }

    except Exception as e:
        print(f"\n[ERROR] Exception in run: {str(e)}")
        run_id_container["result"] = {
            "status": "error",
            "error": str(e),
            "run_id": run_id_container.get("run_id"),
            "cancelled": True,
            "content": "Error occurred",
        }


def cancel_after_delay(agent: Agent, run_id_container: dict, delay_seconds: int = 3):
    """
    在指定延迟后取消 agent 运行。

    Args:
        agent: 需要取消运行的 agent
        run_id_container: 包含要取消的 run_id 的字典
        delay_seconds: 取消前等待的秒数
    """
    print(f"[TIMER] Will cancel run in {delay_seconds} seconds...")
    time.sleep(delay_seconds)

    run_id = run_id_container.get("run_id")
    if run_id:
        print(f"[CANCEL] Cancelling run: {run_id}")
        success = agent.cancel_run(run_id)
        if success:
            print(f"[OK] Run {run_id} marked for cancellation")
        else:
            print(
                f"[ERROR] Failed to cancel run {run_id} (may not exist or already completed)"
            )
    else:
        print("[WARNING] No run_id found to cancel")


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
def main():
    """演示运行取消的主函数。"""

    # 使用模型初始化 agent

    # ---------------------------------------------------------------------------
    # 创建 Agent
    # ---------------------------------------------------------------------------

    agent = Agent(
        name="StorytellerAgent",
        model=OpenAIChat(id="o3-mini"),  # 使用能够生成长响应的模型
        description="An agent that writes detailed stories",
    )

    print("Starting agent run cancellation example...")
    print("=" * 50)

    # 用于在线程间共享 run_id 的容器
    run_id_container = {}

    # 在独立线程中启动 agent 运行
    agent_thread = threading.Thread(
        target=lambda: long_running_task(agent, run_id_container), name="AgentRunThread"
    )

    # 启动取消线程
    cancel_thread = threading.Thread(
        target=cancel_after_delay,
        args=(agent, run_id_container, 8),  # 8 秒后取消
        name="CancelThread",
    )

    # 启动两个线程
    print("[START] Starting agent run thread...")
    agent_thread.start()

    print("[START] Starting cancellation thread...")
    cancel_thread.start()

    # 等待两个线程完成
    print("[WAIT] Waiting for threads to complete...")
    agent_thread.join()
    cancel_thread.join()

    # 打印结果
    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)

    result = run_id_container.get("result")
    if result:
        print(f"Status: {result['status']}")
        print(f"Run ID: {result['run_id']}")
        print(f"Was Cancelled: {result['cancelled']}")

        if result.get("error"):
            print(f"Error: {result['error']}")
        else:
            print(f"Content Preview: {result['content']}")

        if result["cancelled"]:
            print("\n[SUCCESS] Run was successfully cancelled!")
        else:
            print("\n[WARNING] Run completed before cancellation")
    else:
        print(
            "[ERROR] No result obtained - check if cancellation happened during streaming"
        )

    print("\nExample completed!")


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 运行主示例
    main()
