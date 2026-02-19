"""
推理模型 DeepSeek（Ollama）
========================

演示推理 Cookbook 示例。
"""

from agno.agent import Agent
from agno.models.ollama.chat import Ollama


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    agent = Agent(
        model=Ollama(id="llama3.2:latest"),
        reasoning_model=Ollama(id="deepseek-r1:14b", options={"num_predict": 4096}),
    )
    agent.print_response(
        "请解答电车难题，评估多种伦理框架，并用 ASCII 图示展示你的解答。",
        stream=True,
    )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
