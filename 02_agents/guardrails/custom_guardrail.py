"""
自定义护栏
=============================

自定义护栏示例。
"""

import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.exceptions import CheckTrigger, InputCheckError
from agno.guardrails.base import BaseGuardrail
from agno.models.openai import OpenAILike

load_dotenv()


class TopicGuardrail(BaseGuardrail):
    """拦截请求危险指令的请求。"""

    def check(self, run_input) -> None:
        content = (run_input.input_content or "").lower()
        blocked_terms = ["build malware", "phishing template", "exploit"]
        if any(term in content for term in blocked_terms):
            raise InputCheckError(
                "Input contains blocked security-abuse content.",
                check_trigger=CheckTrigger.INPUT_NOT_ALLOWED,
            )

    async def async_check(self, run_input) -> None:
        self.check(run_input)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    name="Guarded Agent",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    pre_hooks=[TopicGuardrail()],
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        "Explain secure password management best practices.", stream=True
    )
