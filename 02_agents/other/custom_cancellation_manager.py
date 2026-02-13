"""
演示自定义取消管理器的示例。

展示如何扩展 BaseRunCancellationManager 来实现你自己的
取消后端（例如，数据库、消息队列、API 等）。

此示例创建一个基于文件的取消管理器，将取消状态
持久化到 JSON 文件，可以通过网络文件系统在进程间共享。

使用方法：
    .venvs/demo/bin/python cookbook/02_agents/other/custom_cancellation_manager.py
"""

import json
import tempfile
import threading
import time
from pathlib import Path
from typing import Dict

from agno.agent import Agent
from agno.exceptions import RunCancelledException
from agno.models.openai import OpenAIChat
from agno.run.agent import RunEvent
from agno.run.cancel import set_cancellation_manager
from agno.run.cancellation_management.base import BaseRunCancellationManager

# ---------------------------------------------------------------------------
# 创建自定义取消管理器
# ---------------------------------------------------------------------------


class FileBasedCancellationManager(BaseRunCancellationManager):
    """将状态持久化到 JSON 文件的取消管理器。

    这是一个展示如何构建自定义后端的简单示例。
    在生产环境中，你可能会使用数据库、Redis 或 API。
    """

    def __init__(self, file_path: str):
        self._file_path = Path(file_path)
        self._lock = threading.Lock()
        # 如果文件不存在则初始化
        if not self._file_path.exists():
            self._write_state({})

    def _read_state(self) -> Dict[str, bool]:
        """从文件读取取消状态。"""
        try:
            return json.loads(self._file_path.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _write_state(self, state: Dict[str, bool]) -> None:
        """将取消状态写入文件。"""
        self._file_path.write_text(json.dumps(state, indent=2))

    def register_run(self, run_id: str) -> None:
        with self._lock:
            state = self._read_state()
            # 使用 setdefault 保留启动前取消意图
            state.setdefault(run_id, False)
            self._write_state(state)

    async def aregister_run(self, run_id: str) -> None:
        self.register_run(run_id)

    def cancel_run(self, run_id: str) -> bool:
        with self._lock:
            state = self._read_state()
            was_registered = run_id in state
            state[run_id] = True
            self._write_state(state)
            return was_registered

    async def acancel_run(self, run_id: str) -> bool:
        return self.cancel_run(run_id)

    def is_cancelled(self, run_id: str) -> bool:
        state = self._read_state()
        return state.get(run_id, False)

    async def ais_cancelled(self, run_id: str) -> bool:
        return self.is_cancelled(run_id)

    def cleanup_run(self, run_id: str) -> None:
        with self._lock:
            state = self._read_state()
            state.pop(run_id, None)
            self._write_state(state)

    async def acleanup_run(self, run_id: str) -> None:
        self.cleanup_run(run_id)

    def raise_if_cancelled(self, run_id: str) -> None:
        if self.is_cancelled(run_id):
            raise RunCancelledException(f"Run {run_id} was cancelled")

    async def araise_if_cancelled(self, run_id: str) -> None:
        self.raise_if_cancelled(run_id)

    def get_active_runs(self) -> Dict[str, bool]:
        return self._read_state()

    async def aget_active_runs(self) -> Dict[str, bool]:
        return self.get_active_runs()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------


def main():
    """演示自定义的基于文件的取消管理器。"""

    # 创建一个临时文件用于取消状态
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        state_file = f.name
        f.write("{}")

    print(f"取消状态文件: {state_file}")
    print("=" * 50)

    # 设置自定义取消管理器
    manager = FileBasedCancellationManager(file_path=state_file)
    set_cancellation_manager(manager)
    print("已配置自定义的基于文件的取消管理器\n")

    # 创建一个 agent
    agent = Agent(
        name="StoryAgent",
        model=OpenAIChat(id="gpt-4o-mini"),
        description="编写故事的 agent",
    )

    # 用于在线程间共享状态的容器
    run_id_container: dict = {}

    def run_agent():
        content_pieces = []
        for chunk in agent.run(
            "写一个关于巫师学习 Python 编程的长故事。"
            "要详细并包含大量对话。",
            stream=True,
        ):
            if "run_id" not in run_id_container and chunk.run_id:
                run_id_container["run_id"] = chunk.run_id

            if chunk.event == RunEvent.run_content:
                print(chunk.content, end="", flush=True)
                content_pieces.append(chunk.content)
            elif chunk.event == RunEvent.run_cancelled:
                print(f"\n\n[CANCELLED] Run was cancelled: {chunk.run_id}")
                run_id_container["cancelled"] = True
                return

        run_id_container["cancelled"] = False

    def cancel_after_delay():
        time.sleep(5)
        run_id = run_id_container.get("run_id")
        if run_id:
            print(f"\n\n[CANCEL] Cancelling run {run_id} via file-based manager...")

            # 显示取消前的状态文件
            state = manager.get_active_runs()
            print(f"[STATE] Before cancel: {state}")

            agent.cancel_run(run_id)

            # 显示取消后的状态文件
            state = manager.get_active_runs()
            print(f"[STATE] After cancel: {state}")

    # 启动两个线程
    agent_thread = threading.Thread(target=run_agent)
    cancel_thread = threading.Thread(target=cancel_after_delay)

    agent_thread.start()
    cancel_thread.start()

    agent_thread.join()
    cancel_thread.join()

    # 最终状态
    print("\n" + "=" * 50)
    print("RESULTS:")
    print(f"  Was cancelled: {run_id_container.get('cancelled', 'unknown')}")
    print(f"  Final state file contents: {manager.get_active_runs()}")

    # 清理
    Path(state_file).unlink(missing_ok=True)
    print("\nExample completed!")


if __name__ == "__main__":
    main()
