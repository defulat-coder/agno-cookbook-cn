"""
缓存模型响应
=============================

展示如何缓存模型响应以避免冗余 API 调用的示例。
"""

import time

from agno.agent import Agent
from agno.models.openai import OpenAIChat


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(model=OpenAIChat(id="gpt-4o", cache_response=True))

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 运行相同的查询两次以演示缓存
    for i in range(1, 3):
        print(f"\n{'=' * 60}")
        print(
            f"运行 {i}: {'缓存未命中（首次请求）' if i == 1 else '缓存命中（缓存响应）'}"
        )
        print(f"{'=' * 60}\n")

        response = agent.run(
            "Write me a short story about a cat that can talk and solve problems."
        )
        print(response.content)
        print(f"\n 耗时: {response.metrics.duration:.3f}s")

        # 为了清晰起见，在迭代之间稍作延迟
        if i == 1:
            time.sleep(0.5)
