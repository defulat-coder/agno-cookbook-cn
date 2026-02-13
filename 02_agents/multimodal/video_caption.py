"""
视频字幕生成
=============================

请使用以下命令安装依赖:
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.moviepy_video import MoviePyVideoTools
from agno.tools.openai import OpenAITools

video_tools = MoviePyVideoTools(
    process_video=True, generate_captions=True, embed_captions=True
)

openai_tools = OpenAITools()

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
video_caption_agent = Agent(
    name="Video Caption Generator Agent",
    model=OpenAIChat(
        id="gpt-4o",
    ),
    tools=[video_tools, openai_tools],
    description="你是一个可以为视频生成和嵌入字幕的 AI agent。",
    instructions=[
        "当用户提供视频时，处理它以生成字幕。",
        "按以下顺序使用视频处理工具:",
        "1. 使用 extract_audio 从视频中提取音频",
        "2. 使用 transcribe_audio 转录音频",
        "3. 使用 create_srt 生成 SRT 字幕",
        "4. 使用 embed_captions 将字幕嵌入到视频中",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    video_caption_agent.print_response(
        "Generate captions for {video with location} and embed them in the video"
    )
