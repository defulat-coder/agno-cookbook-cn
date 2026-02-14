"""
带条件的工作流
=========================

演示带条件的工作流。
"""

from agno.agent.agent import Agent
from agno.db.sqlite import SqliteDb

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
# 导入工作流
from agno.os import AgentOS
from agno.tools.websearch import WebSearchTools
from agno.workflow.condition import Condition
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# === 基础 AGENTS ===
researcher = Agent(
    name="Researcher",
    instructions="研究给定主题并提供详细发现。",
    tools=[WebSearchTools()],
)

summarizer = Agent(
    name="Summarizer",
    instructions="创建研究发现的清晰摘要。",
)

fact_checker = Agent(
    name="Fact Checker",
    instructions="验证事实并检查研究的准确性。",
    tools=[WebSearchTools()],
)

writer = Agent(
    name="Writer",
    instructions="根据所有可用的研究和验证撰写全面的文章。",
)

# === 条件评估器 ===


def needs_fact_checking(step_input: StepInput) -> bool:
    """确定研究是否包含需要事实检查的声明"""
    summary = step_input.previous_step_content or ""

    # 查找表示事实声明的关键字
    fact_indicators = [
        "study shows",
        "research indicates",
        "according to",
        "statistics",
        "data shows",
        "survey",
        "report",
        "million",
        "billion",
        "percent",
        "%",
        "increase",
        "decrease",
    ]

    return any(indicator in summary.lower() for indicator in fact_indicators)


# === 工作流步骤 ===
research_step = Step(
    name="research",
    description="Research the topic",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="Summarize research findings",
    agent=summarizer,
)

# 条件事实检查步骤
fact_check_step = Step(
    name="fact_check",
    description="Verify facts and claims",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="Write final article",
    agent=writer,
)

# === 基础线性工作流 ===
basic_workflow = Workflow(
    name="basic-linear-workflow",
    description="Research -> Summarize -> Condition(Fact Check) -> Write Article",
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="Check if fact-checking is needed",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
    db=SqliteDb(
        session_table="workflow_session",
        db_file="tmp/workflow.db",
    ),
)

# 使用工作流初始化 AgentOS
agent_os = AgentOS(
    description="Example OS setup",
    workflows=[basic_workflow],
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="workflow_with_conditional:app", reload=True)
