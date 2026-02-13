"""
图像转图像
=============================

演示图像转图像功能。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.fal import FalTools

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    id="image-to-image",
    name="Image to Image Agent",
    tools=[FalTools()],
    markdown=True,
    instructions=[
        "你必须使用 `image_to_image` 工具来生成图像。",
        "你是一个可以使用 Fal AI API 生成图像的 AI agent。",
        "你将获得一个提示词和一个图像 URL。",
        "你必须按原样返回图像 URL，不要将其转换为 markdown 或其他格式。",
    ],
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "a cat dressed as a wizard with a background of a mystic forest. Make it look like 'https://fal.media/files/koala/Chls9L2ZnvuipUTEwlnJC.png'",
        stream=True,
    )
