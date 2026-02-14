"""
使用嵌套步骤的工作流
===========================

演示使用 `Steps`、`Condition` 和 `Parallel` 进行嵌套工作流组合。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.workflow.condition import Condition
from agno.workflow.parallel import Parallel
from agno.workflow.step import Step
from agno.workflow.steps import Steps
from agno.workflow.workflow import Workflow

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
researcher = Agent(
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    instructions="研究给定主题并提供关键事实和见解。",
)

tech_researcher = Agent(
    name="Tech Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[HackerNewsTools()],
    instructions="从 Hacker News 研究技术相关主题并提供最新进展。",
)

news_researcher = Agent(
    name="News Research Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[ExaTools()],
    instructions="使用 Exa 搜索研究当前新闻和趋势。",
)

writer = Agent(
    name="Writing Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions="根据提供的研究撰写一篇全面的文章。使其引人入胜且结构清晰。",
)

editor = Agent(
    name="Editor Agent",
    model=OpenAIChat(id="gpt-4o"),
    instructions="审查和编辑文章的清晰度、语法和流畅性。提供精修的最终版本。",
)

content_agent = Agent(
    name="Content Agent",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="根据研究输入准备和格式化用于写作的内容。",
)

# ---------------------------------------------------------------------------
# 定义步骤
# ---------------------------------------------------------------------------
initial_research_step = Step(
    name="InitialResearch",
    agent=researcher,
    description="对主题进行初步研究",
)

tech_research_step = Step(
    name="TechResearch",
    agent=tech_researcher,
    description="从 Hacker News 研究技术发展",
)

news_research_step = Step(
    name="NewsResearch",
    agent=news_researcher,
    description="研究当前新闻和趋势",
)

content_prep_step = Step(
    name="ContentPreparation",
    agent=content_agent,
    description="准备和组织所有用于写作的研究",
)

writing_step = Step(
    name="Writing",
    agent=writer,
    description="根据研究撰写文章",
)

editing_step = Step(
    name="Editing",
    agent=editor,
    description="编辑和润色文章",
)


# ---------------------------------------------------------------------------
# 定义条件评估器
# ---------------------------------------------------------------------------
def is_tech_topic(step_input) -> bool:
    message = step_input.input.lower() if step_input.input else ""
    tech_keywords = [
        "ai",
        "machine learning",
        "technology",
        "software",
        "programming",
        "tech",
        "startup",
        "blockchain",
    ]
    return any(keyword in message for keyword in tech_keywords)


# ---------------------------------------------------------------------------
# 创建工作流
# ---------------------------------------------------------------------------
article_creation_sequence = Steps(
    name="ArticleCreation",
    description="从研究到最终编辑的完整文章创作工作流",
    steps=[
        initial_research_step,
        Condition(
            name="TechResearchCondition",
            description="如果主题与技术相关，则进行专业的并行研究",
            evaluator=is_tech_topic,
            steps=[
                Parallel(
                    tech_research_step,
                    news_research_step,
                    name="SpecializedResearch",
                    description="并行进行技术和新闻研究",
                ),
                content_prep_step,
            ],
        ),
        writing_step,
        editing_step,
    ],
)

article_workflow = Workflow(
    name="Enhanced Article Creation Workflow",
    description="带条件并行研究的自动化文章创作",
    steps=[article_creation_sequence],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    article_workflow.print_response(
        input="Write an article about the latest AI developments in machine learning",
        markdown=True,
        stream=True,
    )
