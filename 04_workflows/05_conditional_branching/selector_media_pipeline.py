"""
选择器媒体管道
=======================

演示使用路由器选择器在图像和视频生成管道之间进行路由。
"""

import asyncio
from typing import List, Optional

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.models.gemini import GeminiTools
from agno.tools.openai import OpenAITools
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.steps import Steps
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow
from pydantic import BaseModel


# ---------------------------------------------------------------------------
# 定义输入模型
# ---------------------------------------------------------------------------
class MediaRequest(BaseModel):
    topic: str
    content_type: str
    prompt: str
    style: Optional[str] = "realistic"
    duration: Optional[int] = None
    resolution: Optional[str] = "1024x1024"


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
image_generator = Agent(
    name="Image Generator",
    model=OpenAIChat(id="gpt-4o"),
    tools=[OpenAITools(image_model="gpt-image-1")],
    instructions="""你是一位专业的图像生成专家。
    当用户请求创建图像时，你应该使用可用的图像生成工具实际生成图像。

    始终使用 generate_image 工具根据用户的规格创建请求的图像。
    包括详细、有创意的提示，融入风格、构图、光线和氛围细节。

    生成图像后，简要描述你创建的内容。""",
)

image_describer = Agent(
    name="Image Describer",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""你是一位专业的图像分析和描述专家。
    当你收到图像（作为输入或来自前一步骤）时，详细分析和描述它，包括：
    - 视觉元素和构图
    - 颜色、光线和氛围
    - 艺术风格和技术
    - 情感影响和叙事

    如果未提供图像，请使用前一步骤的图像描述或提示。
    提供丰富、引人入胜的描述，捕捉视觉内容的本质。""",
)

video_generator = Agent(
    name="Video Generator",
    model=OpenAIChat(id="gpt-4o"),
    tools=[GeminiTools(vertexai=True)],
    instructions="""你是一位专业的视频制作专家。
    根据用户请求创建详细的视频生成提示和故事板。
    包括场景描述、摄像机移动、过渡和时间安排。
    考虑节奏、视觉叙事以及分辨率和持续时间等技术方面。
    将你的响应格式化为全面的视频制作计划。""",
)

video_describer = Agent(
    name="Video Describer",
    model=OpenAIChat(id="gpt-4o"),
    instructions="""你是一位专业的视频分析和评论家。
    全面分析和描述视频，包括：
    - 场景构图和摄影
    - 叙事流和节奏
    - 视觉效果和制作质量
    - 视听和谐和氛围
    - 技术执行和艺术价值
    提供详细、专业的视频分析。""",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
generate_image_step = Step(
    name="generate_image",
    agent=image_generator,
    description="根据用户请求生成详细的图像创建提示",
)

describe_image_step = Step(
    name="describe_image",
    agent=image_describer,
    description="详细分析和描述生成的图像概念",
)

generate_video_step = Step(
    name="generate_video",
    agent=video_generator,
    description="创建全面的视频制作计划和故事板",
)

describe_video_step = Step(
    name="describe_video",
    agent=video_describer,
    description="用专业见解分析和评论视频制作计划",
)

image_sequence = Steps(
    name="image_generation",
    description="完整的图像生成和分析工作流",
    steps=[generate_image_step, describe_image_step],
)

video_sequence = Steps(
    name="video_generation",
    description="完整的视频制作和分析工作流",
    steps=[generate_video_step, describe_video_step],
)


# ---------------------------------------------------------------------------
# 定义路由器选择器
# ---------------------------------------------------------------------------
def media_sequence_selector(step_input: StepInput) -> List[Step]:
    if not step_input.input or not isinstance(step_input.input, str):
        return [image_sequence]

    message_lower = step_input.input.lower()
    if "video" in message_lower:
        return [video_sequence]
    if "image" in message_lower:
        return [image_sequence]
    return [image_sequence]


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
media_workflow = Workflow(
    name="AI Media Generation Workflow",
    description="使用 AI Agent 生成和分析图像或视频",
    steps=[
        Router(
            name="Media Type Router",
            description="根据内容类型路由到适当的媒体生成管道",
            selector=media_sequence_selector,
            choices=[image_sequence, video_sequence],
        )
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=== 示例 1：图像生成（使用 message_data）===")
    image_request = MediaRequest(
        topic="Create an image of magical forest for a movie scene",
        content_type="image",
        prompt="A mystical forest with glowing mushrooms",
        style="fantasy art",
        resolution="1920x1080",
    )
    _ = image_request

    media_workflow.print_response(
        input="Create an image of magical forest for a movie scene",
        markdown=True,
    )

    asyncio.run(
        media_workflow.aprint_response(
            input="Create an image of magical forest for a movie scene",
            markdown=True,
        )
    )
