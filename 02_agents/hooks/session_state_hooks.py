"""
Session State Hooks 示例
=============================

演示如何使用 pre_hook 更新 session_state 的示例。
"""

from typing import List

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.run import RunContext
from agno.run.agent import RunInput
from pydantic import BaseModel, Field


class ConversationTopics(BaseModel):
    topics: List[str] = Field(description="Topics present in the user messages")


# 这将是我们的 pre-hook 函数
def track_conversation_topics(run_context: RunContext, run_input: RunInput) -> None:
    """简单的 pre-hook 函数，用于在 session state 中跟踪对话主题"""

    # 如果 session state 还不存在，则初始化它
    if run_context.session_state is None:
        run_context.session_state = {"topics": []}
    elif run_context.session_state.get("topics") is None:
        run_context.session_state["topics"] = []

    # 设置一个 Agent 来获取对话中讨论的主题
    # ---------------------------------------------------------------------------
    # 创建 Agent
    # ---------------------------------------------------------------------------

    topics_analyzer_agent = Agent(
        name="Topics Analyzer",
        model=OpenAIChat(id="gpt-5-mini"),
        instructions=[
            "Your task is to analyze a user query and extract the topics."
            "You will be presented with a user message sent to an agent."
            "You need to extract the topics present in the user message."
            "Be concise and brief. Topics should be one or two words, and only want the one or two main topics."
            "Respond just with the list of topics, no other text or explanation."
        ],
        output_schema=ConversationTopics,
    )

    # 运行 Agent 获取对话中讨论的主题
    response = topics_analyzer_agent.run(
        input=f"Extract the topics present in the following user message: {run_input.input_content}"
    )

    # 更新 session state 以跟踪对话中讨论的主题
    run_context.session_state["topics"].extend(response.content.topics)  # type: ignore


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
# 创建一个简单的 Agent 并配备我们的 pre-hook
agent = Agent(
    name="Simple Agent",
    model=OpenAIChat(id="gpt-5-mini"),
    pre_hooks=[track_conversation_topics],
    db=SqliteDb(db_file="test.db"),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response(
        input="I want to know more about AI Agents.",
        session_id="topics_analyzer_session",
    )
    print(
        f"Current session state, after the first run: {agent.get_session_state(session_id='topics_analyzer_session')}"
    )

    agent.print_response(
        input="I also want to know more about Agno, the framework to build AI Agents.",
        session_id="topics_analyzer_session",
    )
    print(
        f"Current session state, after the second run: {agent.get_session_state(session_id='topics_analyzer_session')}"
    )
