"""
Agent 式用户输入
=============================

人机协作：允许用户在外部提供输入。
"""

from typing import Any, Dict, List

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools import Toolkit
from agno.tools.function import UserInputField
from agno.tools.user_control_flow import UserControlFlowTools
from agno.utils import pprint


class EmailTools(Toolkit):
    def __init__(self, *args, **kwargs):
        super().__init__(
            name="EmailTools", tools=[self.send_email, self.get_emails], *args, **kwargs
        )

    def send_email(self, subject: str, body: str, to_address: str) -> str:
        """向指定地址发送带有指定主题和正文的电子邮件。

        Args:
            subject (str): 电子邮件的主题。
            body (str): 电子邮件的正文。
            to_address (str): 发送电子邮件的地址。
        """
        return f"Sent email to {to_address} with subject {subject} and body {body}"

    def get_emails(self, date_from: str, date_to: str) -> list[dict[str, str]]:
        """获取指定日期之间的所有电子邮件。

        Args:
            date_from (str): 开始日期（YYYY-MM-DD 格式）。
            date_to (str): 结束日期（YYYY-MM-DD 格式）。
        """
        return [
            {
                "subject": "Hello",
                "body": "Hello, world!",
                "to_address": "test@test.com",
                "date": date_from,
            },
            {
                "subject": "Random other email",
                "body": "This is a random other email",
                "to_address": "john@doe.com",
                "date": date_to,
            },
        ]


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[EmailTools(), UserControlFlowTools()],
    markdown=True,
    db=SqliteDb(db_file="tmp/agentic_user_input.db"),
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_response = agent.run(
        "Send an email with the body 'What is the weather in Tokyo?'"
    )

    # 我们使用 while 循环继续运行，直到 agent 对用户输入满意为止
    while run_response.is_paused:
        for requirement in run_response.active_requirements:
            if requirement.needs_user_input:
                input_schema: List[UserInputField] = requirement.user_input_schema  # type: ignore

                for field in input_schema:
                    # 为 schema 中的每个字段获取用户输入
                    field_type = field.field_type  # type: ignore
                    field_description = field.description  # type: ignore

                    # 向用户显示字段信息
                    print(f"\nField: {field.name}")  # type: ignore
                    print(f"Description: {field_description}")
                    print(f"Type: {field_type}")

                    # 获取用户输入
                    if field.value is None:  # type: ignore
                        user_value = input(f"Please enter a value for {field.name}: ")  # type: ignore
                    else:
                        print(f"Value: {field.value}")  # type: ignore
                        user_value = field.value  # type: ignore

                    # 更新字段值
                    field.value = user_value  # type: ignore

        run_response = agent.continue_run(
            run_id=run_response.run_id,
            requirements=run_response.requirements,
        )
        if not run_response.is_paused:
            pprint.pprint_run_response(run_response)
            break

    run_response = agent.run("Get me all my emails")

    while run_response.is_paused:
        for requirement in run_response.active_requirements:
            if requirement.needs_user_input:
                input_schema: Dict[str, Any] = requirement.user_input_schema  # type: ignore

                for field in input_schema:
                    # 为 schema 中的每个字段获取用户输入
                    field_type = field.field_type  # type: ignore
                    field_description = field.description  # type: ignore

                    # 向用户显示字段信息
                    print(f"\nField: {field.name}")  # type: ignore
                    print(f"Description: {field_description}")
                    print(f"Type: {field_type}")

                    # 获取用户输入
                    if field.value is None:  # type: ignore
                        user_value = input(f"Please enter a value for {field.name}: ")  # type: ignore
                    else:
                        print(f"Value: {field.value}")  # type: ignore
                        user_value = field.value  # type: ignore

                    # 更新字段值
                    field.value = user_value  # type: ignore

        run_response = agent.continue_run(
            run_id=run_response.run_id,
            requirements=run_response.requirements,
        )

        if not run_response.is_paused:
            pprint.pprint_run_response(run_response)
            break
