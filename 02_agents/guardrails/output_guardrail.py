"""
输出护栏
=============================

输出护栏示例。
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.exceptions import CheckTrigger, OutputCheckError
from agno.models.openai import OpenAILike
from agno.run.agent import RunOutput

load_dotenv()


def enforce_non_empty_output(run_output: RunOutput) -> None:
    """拒绝空或过短的响应。"""
    content = (run_output.content or "").strip()
    if len(content) < 20:
        raise OutputCheckError(
            "输出过短，无法提供有效内容。",
            check_trigger=CheckTrigger.OUTPUT_NOT_ALLOWED,
        )


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="输出检查 Agent",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    post_hooks=[enforce_non_empty_output],
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("请总结整洁架构中的核心思想。", stream=True)
