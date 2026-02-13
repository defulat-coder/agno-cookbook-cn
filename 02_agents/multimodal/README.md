# multimodal

多模态处理模式示例，涵盖图像/音频/视频处理。

## 文件列表
- `audio_input_output.py` - 演示音频输入输出。
- `audio_sentiment_analysis.py` - 演示音频情感分析。
- `audio_streaming.py` - 演示音频流式传输。
- `audio_to_text.py` - 演示音频转文字。
- `image_to_audio.py` - 演示图像转音频。
- `image_to_image.py` - 演示图像转图像。
- `image_to_structured_output.py` - 演示图像转结构化输出。
- `image_to_text.py` - 演示图像转文字。
- `media_input_for_tool.py` - 演示工具的媒体输入。
- `video_caption.py` - 演示视频字幕生成。

## 前置要求
- 使用 `direnv allow` 加载环境变量（包括 `OPENAI_API_KEY`）。
- 使用 `./scripts/demo_setup.sh` 创建演示环境，然后用 `.venvs/demo/bin/python` 运行示例。
- 部分示例需要可选的本地服务（例如 pgvector）或特定提供商的 API 密钥。

## 运行方式
- `.venvs/demo/bin/python cookbook/02_agents/<directory>/<file>.py`
