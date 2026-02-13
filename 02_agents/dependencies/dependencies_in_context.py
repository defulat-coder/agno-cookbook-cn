"""
上下文中的依赖
=============================

上下文中的依赖示例。
"""

import json

import httpx
from agno.agent import Agent
from agno.models.openai import OpenAIChat


def get_top_hackernews_stories(num_stories: int = 5) -> str:
    """从 HackerNews 获取并返回热门故事。

    Args:
        num_stories: 要检索的热门故事数量（默认：5）
    Returns:
        包含故事详情（标题、URL、评分等）的 JSON 字符串
    """
    # 获取热门故事
    stories = [
        {
            k: v
            for k, v in httpx.get(
                f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
            )
            .json()
            .items()
            if k != "kids"  # 排除讨论线程
        }
        for id in httpx.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json"
        ).json()[:num_stories]
    ]
    return json.dumps(stories, indent=4)


# 创建一个可以访问实时 HackerNews 数据的上下文感知 Agent
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    # dependencies 中的每个函数在 agent 运行时被解析，
    # 可以将其视为 Agent 的依赖注入
    dependencies={"top_hackernews_stories": get_top_hackernews_stories},
    # 我们可以将整个 dependencies 字典添加到用户消息中
    add_dependencies_to_context=True,
    markdown=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # 使用示例
    agent.print_response(
        "Summarize the top stories on HackerNews and identify any interesting trends.",
        stream=True,
    )
