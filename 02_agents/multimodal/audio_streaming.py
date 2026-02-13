"""
音频流式传输
=============================

演示音频流式传输功能。
"""

import base64
import wave
from typing import Iterator

from agno.agent import Agent, RunOutputEvent
from agno.models.openai import OpenAIChat

# 音频配置
SAMPLE_RATE = 24000  # Hz (24kHz)
CHANNELS = 1  # 单声道（如果是立体声改为 2）
SAMPLE_WIDTH = 2  # 字节（16 位）

# 向 agent 提供音频文件和音频配置，获取文本 + 音频结果
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o-audio-preview",
        modalities=["text", "audio"],
        audio={
            "voice": "alloy",
            "format": "pcm16",
        },  # 流式传输仅支持 pcm16
    ),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    output_stream: Iterator[RunOutputEvent] = agent.run(
        "Tell me a 10 second story", stream=True
    )

    filename = "tmp/response_stream.wav"

    # 以追加二进制模式打开文件一次
    with wave.open(str(filename), "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)

        # 迭代生成的音频
        for response in output_stream:
            response_audio = response.response_audio  # type: ignore
            if response_audio:
                if response_audio.transcript:
                    print(response_audio.transcript, end="", flush=True)
                if response_audio.content:
                    try:
                        pcm_bytes = base64.b64decode(response_audio.content)
                        wav_file.writeframes(pcm_bytes)
                    except Exception as e:
                        print(f"Error decoding audio: {e}")
    print()
