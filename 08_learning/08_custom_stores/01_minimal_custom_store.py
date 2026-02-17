"""
自定义存储：最小示例
=============================
展示如何通过实现 LearningStore 协议创建自定义学习存储。

此最小示例使用内存存储并演示：
- 必须实现的 LearningStore 协议方法
- 如何通过存储的构造函数传递自定义上下文（如 project_id）
- 如何将自定义存储插入 LearningMachine

有关数据库支持的示例，请参见 02_custom_store_with_db.py
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from agno.agent import Agent
from agno.learn import LearningMachine
from agno.learn.stores.protocol import LearningStore
from agno.models.openai import OpenAIResponses

# ---------------------------------------------------------------------------
# 自定义存储实现
# ---------------------------------------------------------------------------

# 内存存储（生产环境中应该是数据库）
_project_data: Dict[str, Dict[str, Any]] = {}


@dataclass
class ProjectContextStore(LearningStore):
    """项目特定上下文的自定义存储。

    存储用户正在处理的项目信息。
    演示如何创建自定义学习存储。

    注意：`context` 字段是此示例的模式选择，不是
    协议要求。你也可以使用类型化的配置类（如内置存储）
    或特定参数的直接字段。
    """

    # 在构造时传递的自定义上下文（模式选择，非必需）
    context: Dict[str, Any] = field(default_factory=dict)

    # 内部状态
    _updated: bool = field(default=False, init=False)

    # =========================================================================
    # LearningStore 协议实现（必需）
    # =========================================================================

    @property
    def learning_type(self) -> str:
        """此学习类型的唯一标识符。"""
        return "project_context"

    @property
    def schema(self) -> Any:
        """此学习类型使用的 schema 类。"""
        # 对于简单存储，可以只返回 dict 或 dataclass
        return dict

    def recall(self, **kwargs) -> Optional[Dict[str, Any]]:
        """从存储中检索项目上下文。

        使用 self.context 中的 project_id（在构造时设置）。
        """
        project_id = self.context.get("project_id")
        if not project_id:
            return None
        return _project_data.get(project_id)

    async def arecall(self, **kwargs) -> Optional[Dict[str, Any]]:
        """recall 的异步版本。"""
        return self.recall(**kwargs)

    def process(self, messages: List[Any], **kwargs) -> None:
        """从消息中提取并保存项目上下文。

        在真实实现中，你可能会使用模型从对话中提取
        相关信息。
        """
        project_id = self.context.get("project_id")
        if not project_id or not messages:
            return

        # 简单提取：查找项目相关关键词
        # 在生产环境中，使用模型进行智能提取
        current = _project_data.get(project_id, {})

        for msg in messages:
            content = getattr(msg, "content", str(msg))
            if isinstance(content, str):
                # 简单的关键词提取（仅演示）
                if "goal" in content.lower() or "objective" in content.lower():
                    current["last_discussed_topic"] = "goals"
                    self._updated = True
                elif "blocker" in content.lower() or "stuck" in content.lower():
                    current["last_discussed_topic"] = "blockers"
                    self._updated = True

        if current:
            _project_data[project_id] = current

    async def aprocess(self, messages: List[Any], **kwargs) -> None:
        """process 的异步版本。"""
        self.process(messages, **kwargs)

    def build_context(self, data: Any) -> str:
        """为 Agent prompt 构建上下文字符串。

        将召回的数据格式化为 XML，注入到
        Agent 的系统 prompt 中。
        """
        if not data:
            project_id = self.context.get("project_id", "unknown")
            return f"<project_context>\nProject: {project_id}\nNo context saved yet.\n</project_context>"

        project_id = self.context.get("project_id", "unknown")
        lines = ["<project_context>", f"Project: {project_id}"]

        for key, value in data.items():
            lines.append(f"{key}: {value}")

        lines.append("</project_context>")
        return "\n".join(lines)

    def get_tools(self, **kwargs) -> List[Callable]:
        """获取暴露给 Agent 的工具。

        如果不需要工具则返回空列表，或返回
        Agent 可以使用的可调用函数。
        """
        return []

    async def aget_tools(self, **kwargs) -> List[Callable]:
        """get_tools 的异步版本。"""
        return self.get_tools(**kwargs)

    @property
    def was_updated(self) -> bool:
        """检查存储在上次操作中是否已更新。"""
        return self._updated

    # =========================================================================
    # 自定义方法（可选）
    # =========================================================================

    def set_context(self, key: str, value: Any) -> None:
        """手动设置项目上下文。"""
        project_id = self.context.get("project_id")
        if not project_id:
            return

        if project_id not in _project_data:
            _project_data[project_id] = {}

        _project_data[project_id][key] = value
        self._updated = True

    def print(self) -> None:
        """打印当前项目上下文。"""
        project_id = self.context.get("project_id", "unknown")
        data = _project_data.get(project_id, {})
        print(f"\n--- Project Context: {project_id} ---")
        if data:
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print("  (empty)")
        print()


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------

# 使用项目上下文创建自定义存储
project_store = ProjectContextStore(
    context={
        "project_id": "learning-machine",
        "team": "platform",
    },
)

# 通过 custom_stores 插入 LearningMachine
agent = Agent(
    model=OpenAIResponses(id="gpt-5.2"),
    learning=LearningMachine(
        custom_stores={
            "project": project_store,
        },
    ),
    markdown=True,
)


# ---------------------------------------------------------------------------
# 运行演示
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    user_id = "developer@example.com"

    # 手动设置一些项目上下文
    project_store.set_context("current_sprint", "Sprint 23")
    project_store.set_context("tech_stack", "Python, PostgreSQL")

    print("\n" + "=" * 60)
    print("自定义存储演示：项目上下文")
    print("=" * 60 + "\n")

    # 项目上下文将出现在 Agent 的系统 prompt 中
    agent.print_response(
        "What project am I working on?",
        user_id=user_id,
        stream=True,
    )

    project_store.print()

    # 讨论触发提取的内容
    print("\n" + "=" * 60)
    print("讨论阻碍（触发提取）")
    print("=" * 60 + "\n")

    agent.print_response(
        "I'm stuck on the database migration. It's a blocker for the release.",
        user_id=user_id,
        stream=True,
    )

    project_store.print()
