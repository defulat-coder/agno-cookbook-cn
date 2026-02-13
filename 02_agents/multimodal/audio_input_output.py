"""
音频输入输出
=============================

演示音频输入输出功能。
"""

import requests
from agno.agent import Agent
from agno.media import Audio
from agno.models.openai import OpenAIChat
from agno.utils.audio import write_audio_to_file
from rich.pretty import pprint

# 获取音频文件并转换为 base64 编码字符串
url = "https://openaiassets.blob.core.windows.net/$web/API/docs/audio/alloy.wav"
response = requests.get(url)
response.raise_for_status()
wav_data = response.content

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "sage", "format": "wav"},
    ),
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_response = agent.run(
        "What's in these recording?",
        audio=[Audio(content=wav_data, format="wav")],
    )

    if run_response.response_audio is not None:
        pprint(run_response.content)
        write_audio_to_file(
            audio=run_response.response_audio.content, filename="tmp/result.wav"
        )
