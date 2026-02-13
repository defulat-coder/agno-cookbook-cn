"""
音频情感分析
=============================

演示音频情感分析功能。
"""

import requests
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.media import Audio
from agno.models.google import Gemini

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=Gemini(id="gemini-3-flash-preview"),
    add_history_to_context=True,
    markdown=True,
    db=SqliteDb(
        session_table="audio_sentiment_analysis_sessions",
        db_file="tmp/audio_sentiment_analysis.db",
    ),
)

url = "https://agno-public.s3.amazonaws.com/demo_data/sample_conversation.wav"

response = requests.get(url)
audio_content = response.content

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 对此音频对话进行情感分析。使用说话人 A、说话人 B 来标识说话者。
    agent.print_response(
        "Give a sentiment analysis of this audio conversation. Use speaker A, speaker B to identify speakers.",
        audio=[Audio(content=audio_content)],
        stream=True,
    )

    agent.print_response(
        "What else can you tell me about this audio conversation?",
        stream=True,
    )
