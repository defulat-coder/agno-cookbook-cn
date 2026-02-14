"""演示如何使用 WorkflowAgent 将工作流添加到 AgentOS 的示例"""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.workflow import WorkflowAgent
from agno.workflow.condition import Condition
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"


# === AGENTS ===
story_writer = Agent(
    name="Story Writer",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="你的任务是根据给定主题撰写一个100字的故事",
)

story_editor = Agent(
    name="Story Editor",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="审查并改进故事的语法、流畅性和清晰度",
)

story_formatter = Agent(
    name="Story Formatter",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="将故事分解为序言、正文和结尾部分",
)


# === 条件评估器 ===
def needs_editing(step_input: StepInput) -> bool:
    """根据长度和复杂性确定故事是否需要编辑"""
    story = step_input.previous_step_content or ""

    # 检查故事是否足够长以受益于编辑
    word_count = len(story.split())

    # 如果故事超过50个单词或包含复杂标点，则进行编辑
    return word_count > 50 or any(punct in story for punct in ["!", "?", ";", ":"])


def add_references(step_input: StepInput):
    """为故事添加参考资料"""
    previous_output = step_input.previous_step_content

    if isinstance(previous_output, str):
        return previous_output + "\n\nReferences: https://www.agno.com"


# === 工作流步骤 ===
write_step = Step(
    name="write_story",
    description="Write initial story",
    agent=story_writer,
)

edit_step = Step(
    name="edit_story",
    description="Edit and improve the story",
    agent=story_editor,
)

format_step = Step(
    name="format_story",
    description="Format the story into sections",
    agent=story_formatter,
)

# 创建一个 WorkflowAgent，它将决定何时运行工作流
workflow_agent = WorkflowAgent(model=OpenAIChat(id="gpt-5.2"), num_history_runs=4)

# === 带条件的工作流 ===
workflow = Workflow(
    name="Story Generation with Conditional Editing",
    description="A workflow that generates stories, conditionally edits them, formats them, and adds references",
    agent=workflow_agent,
    steps=[
        write_step,
        Condition(
            name="editing_condition",
            description="Check if story needs editing",
            evaluator=needs_editing,
            steps=[edit_step],
        ),
        format_step,
        add_references,
    ],
    db=PostgresDb(db_url),
    # debug_mode=True,
)


# 使用工作流初始化 AgentOS
agent_os = AgentOS(
    description="Example OS setup",
    workflows=[workflow],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="basic_chat_workflow_agent:app", reload=True)
