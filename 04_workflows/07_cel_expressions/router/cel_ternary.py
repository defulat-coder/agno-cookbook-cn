"""使用 CEL 表达式的路由器：对输入内容使用三元运算符。
==============================================================

使用 CEL 三元运算符根据输入是否提及"video"
在两个步骤之间进行选择。

要求：
    pip install cel-python
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.workflow import CEL_AVAILABLE, Step, Workflow
from agno.workflow.router import Router

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
if not CEL_AVAILABLE:
    print("CEL is not available. Install with: pip install cel-python")
    exit(1)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
video_agent = Agent(
    name="Video Specialist",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你专门从事视频内容创作和编辑建议。",
    markdown=True,
)

image_agent = Agent(
    name="Image Specialist",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="你专门从事图像设计、摄影和视觉内容。",
    markdown=True,
)

# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
workflow = Workflow(
    name="CEL Ternary Router",
    steps=[
        Router(
            name="Media Router",
            selector='input.contains("video") ? "Video Handler" : "Image Handler"',
            choices=[
                Step(name="Video Handler", agent=video_agent),
                Step(name="Image Handler", agent=image_agent),
            ],
        ),
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("--- 视频请求 ---")
    workflow.print_response(input="How do I edit a video for YouTube?")
    print()

    print("--- 图像请求 ---")
    workflow.print_response(input="Help me design a logo for my startup.")
