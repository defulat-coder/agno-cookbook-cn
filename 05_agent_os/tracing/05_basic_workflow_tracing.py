"""
AgentOS 追踪
要求：
    uv pip install agno opentelemetry-api opentelemetry-sdk openinference-instrumentation-agno
"""

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from agno.tools.websearch import WebSearchTools
from agno.workflow.condition import Condition
from agno.workflow.step import Step
from agno.workflow.types import StepInput
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = SqliteDb(db_file="tmp/traces.db")

# === 基础 AGENT ===
researcher = Agent(
    name="Researcher",
    instructions="研究给定的主题并提供详细发现。",
    tools=[WebSearchTools()],
)

summarizer = Agent(
    name="Summarizer",
    instructions="创建研究发现的清晰摘要。",
)

fact_checker = Agent(
    name="Fact Checker",
    instructions="验证研究中的事实并检查准确性。",
    tools=[WebSearchTools()],
)

writer = Agent(
    name="Writer",
    instructions="基于所有可用的研究和验证撰写全面的文章。",
)

# === 条件评估器 ===


def needs_fact_checking(step_input: StepInput) -> bool:
    """确定研究是否包含需要事实检查的声明"""
    return True


# === 工作流步骤 ===
research_step = Step(
    name="research",
    description="研究主题",
    agent=researcher,
)

summarize_step = Step(
    name="summarize",
    description="总结研究发现",
    agent=summarizer,
)

# 条件事实检查步骤
fact_check_step = Step(
    name="fact_check",
    description="验证事实和声明",
    agent=fact_checker,
)

write_article = Step(
    name="write_article",
    description="撰写最终文章",
    agent=writer,
)

# === 基础线性工作流 ===
basic_workflow = Workflow(
    name="Basic Linear Workflow",
    description="研究 -> 总结 -> 条件（事实检查）-> 撰写文章",
    db=db,
    steps=[
        research_step,
        summarize_step,
        Condition(
            name="fact_check_condition",
            description="检查是否需要事实检查",
            evaluator=needs_fact_checking,
            steps=[fact_check_step],
        ),
        write_article,
    ],
)

# 设置我们的 AgentOS 应用
agent_os = AgentOS(
    description="用于追踪基础工作流的示例应用",
    workflows=[basic_workflow],
    tracing=True,
)
app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="05_basic_workflow_tracing:app", reload=True)
