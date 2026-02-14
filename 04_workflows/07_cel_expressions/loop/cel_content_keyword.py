"""使用 CEL 结束条件的循环：当 Agent 发出完成信号时停止。
================================================================

使用 last_step_content.contains() 检测输出中的关键字
以表示循环应该停止。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import CEL_AVAILABLE, Loop, Step, Workflow

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
if not CEL_AVAILABLE:
    print("CEL is not available. Install with: pip install cel-python")
    exit(1)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
editor = Agent(
    name="Editor",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions=(
        "编辑和改进文本。当文本经过润色并准备就绪时，"
        "在响应末尾包含单词 DONE。"
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Content Keyword Loop",
    steps=[
        Loop(
            name="Editing Loop",
            max_iterations=5,
            end_condition='last_step_content.contains("DONE")',
            steps=[
                Step(name="Edit", agent=editor),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print('使用 CEL 结束条件的循环：last_step_content.contains("DONE")')
    print("=" * 60)
    workflow.print_response(
        input="Refine this draft: AI is changing the world in many ways.",
        stream=True,
    )
