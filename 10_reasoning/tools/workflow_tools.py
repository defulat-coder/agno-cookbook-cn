"""
工作流工具（Workflow Tools）
==============

演示推理 Cookbook 示例。
"""

from textwrap import dedent

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.openai import OpenAIChat
from agno.team import Team
from agno.tools.hackernews import HackerNewsTools
from agno.tools.websearch import WebSearchTools
from agno.tools.workflow import WorkflowTools
from agno.workflow.types import StepInput, StepOutput
from agno.workflow.workflow import Workflow


# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------
def run_example() -> None:
    FEW_SHOT_EXAMPLES = dedent("""\
        你可以参考以下示例作为每个工具使用方式的指导。
        ### 示例
        #### 示例：博客文章工作流
        用户：请创建一篇关于 2024 年 AI 趋势的博客文章
        思考：用户想要处理客户反馈数据。我需要了解数据的格式以及他们想要什么类型的摘要。让我从基本的工作流运行开始。
        运行：input_data="AI trends in 2024", additional_data={"topic": "AI, AI agents, AI workflows", "style": "博客文章应以通俗易懂的风格撰写。"}
        分析：工作流成功运行并生成了基本的博客文章。但格式可能不完全符合用户需求。让我检查结果是否达到他们的预期。
        最终答案：我已通过工作流创建了一篇关于 2024 年 AI 趋势的博客文章。博客文章显示...
    """)

    # 定义 Agent
    web_agent = Agent(
        name="Web Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[WebSearchTools()],
        role="Search the web for the latest news and trends",
    )
    hackernews_agent = Agent(
        name="Hackernews Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        tools=[HackerNewsTools()],
        role="Extract key insights and content from Hackernews posts",
    )

    writer_agent = Agent(
        name="Writer Agent",
        model=OpenAIChat(id="gpt-4o-mini"),
        instructions="撰写一篇关于该话题的博客文章",
    )

    def prepare_input_for_web_search(step_input: StepInput) -> StepOutput:
        title = step_input.input
        topic = step_input.additional_data.get("topic")
        return StepOutput(
            content=dedent(f"""\
    	我正在撰写标题为：{title} 的博客文章
    	<topic>
    	{topic}
    	</topic>
    	请在网络上搜索至少 10 篇相关文章\
    	""")
        )

    def prepare_input_for_writer(step_input: StepInput) -> StepOutput:
        title = step_input.additional_data.get("title")
        topic = step_input.additional_data.get("topic")
        style = step_input.additional_data.get("style")

        research_team_output = step_input.previous_step_content

        return StepOutput(
            content=dedent(f"""\
    	我正在撰写标题为：{title} 的博客文章
    	<required_style>
    	{style}
    	</required_style>
    	<topic>
    	{topic}
    	</topic>
    	以下是来自网络的信息：
    	<research_results>
    	{research_team_output}
    	<research_results>\
    	""")
        )

    # 定义用于复杂分析的研究团队
    research_team = Team(
        name="Research Team",
        members=[hackernews_agent, web_agent],
        instructions="从 Hackernews 和网络研究科技话题",
    )

    # 创建并使用工作流
    if __name__ == "__main__":
        content_creation_workflow = Workflow(
            name="Blog Post Workflow",
            description="从 Hackernews 和网络自动创建博客文章",
            db=SqliteDb(
                session_table="workflow_session",
                db_file="tmp/workflow.db",
            ),
            steps=[
                prepare_input_for_web_search,
                research_team,
                prepare_input_for_writer,
                writer_agent,
            ],
        )

        workflow_tools = WorkflowTools(
            workflow=content_creation_workflow,
            enable_think=True,
            enable_analyze=True,
            add_few_shot=True,
            few_shot_examples=FEW_SHOT_EXAMPLES,
        )

        agent = Agent(
            model=OpenAIChat(id="gpt-5-mini"),
            tools=[workflow_tools],
            markdown=True,
        )

        agent.print_response(
            "请创建一篇博客文章，标题为：2024 年 AI 趋势",
            instructions="使用 `run_workflow` 工具运行工作流时，请记得将 `additional_data` 作为键值对字典传入。",
            markdown=True,
            stream=True,
        )


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    run_example()
