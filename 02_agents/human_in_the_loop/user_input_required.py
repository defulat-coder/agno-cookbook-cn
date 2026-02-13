"""
需要用户输入
=============================

人机协作：允许用户在外部提供输入。
"""

from typing import List

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.tools import tool
from agno.tools.function import UserInputField
from agno.utils import pprint


# 你可以指定 user_input_fields 或留空以让用户提供所有字段
@tool(requires_user_input=True, user_input_fields=["to_address"])
def send_email(subject: str, body: str, to_address: str) -> str:
    """
    发送电子邮件。

    Args:
        subject (str): 电子邮件的主题。
        body (str): 电子邮件的正文。
        to_address (str): 发送电子邮件的地址。
    """
    return f"Sent email to {to_address} with subject {subject} and body {body}"


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[send_email],
    markdown=True,
    db=SqliteDb(db_file="tmp/user_input_required.db"),
)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_response = agent.run(
        "Send an email with the subject 'Hello' and the body 'Hello, world!'"
    )

    for requirement in run_response.active_requirements:
        if requirement.needs_user_input:
            input_schema: List[UserInputField] = requirement.user_input_schema  # type: ignore

            for field in input_schema:
                # Get user input for each field in the schema
                field_type = field.field_type
                field_description = field.description

                # Display field information to the user
                print(f"\nField: {field.name}")
                print(f"Description: {field_description}")
                print(f"Type: {field_type}")

                # Get user input
                if field.value is None:
                    user_value = input(f"Please enter a value for {field.name}: ")
                else:
                    print(f"Value: {field.value}")
                    user_value = field.value

                # Update the field value
                field.value = user_value

    run_response = agent.continue_run(
        run_id=run_response.run_id,
        requirements=run_response.requirements,
    )  # or agent.continue_run(run_response=run_response)
    pprint.pprint_run_response(run_response)

    # Or for simple debug flow
    # agent.print_response("Send an email with the subject 'Hello' and the body 'Hello, world!'")
