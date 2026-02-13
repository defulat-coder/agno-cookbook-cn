"""
会议准备工作流
======================

在特定会议前触发。通过调研与会者、获取相关文档、收集背景信息并生成讨论要点，
完成深度会议准备。

步骤:
1. 解析会议详情
2. 并行：调研与会者 + 获取内部资料 + 收集外部背景
3. 综合生成会议准备简报

测试:
    python -m workflows.meeting_prep.workflow
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow import Step, Workflow
from agno.workflow.parallel import Parallel

# ---------------------------------------------------------------------------
# 模拟工具
# ---------------------------------------------------------------------------


@tool(
    description="从日历中查询会议详情。为演示目的返回模拟数据。"
)
def get_meeting_details(meeting_topic: str) -> str:
    """返回模拟的会议详情。"""
    # 提供一个贴近真实的会议场景
    return """
Meeting Details:
  Title: Product Strategy Review
  Date: Thursday, February 6, 2025, 10:00 - 11:00 AM
  Location: Conference Room A
  Organizer: Lisa Zhang (VP Product)

  Attendees:
  - James Wilson (CEO) - james@company.com
  - Lisa Zhang (VP Product) - lisa@company.com
  - You (VP Engineering)

  Agenda:
  1. Q4 retrospective (10 min)
  2. Q1 roadmap review (20 min)
  3. Resource allocation & engineering capacity (15 min)
  4. Key decisions needed (15 min)

  Previous Meeting Notes (Jan 15):
  - Agreed to focus Q1 on platform reliability
  - James wanted to explore AI features for Q2
  - Lisa proposed new enterprise tier
  - Action item: You to provide engineering capacity estimates
  - Action item: Lisa to finalize customer interview results

  Related Documents:
  - Q4 Product Metrics Dashboard
  - Q1 Roadmap Draft v2
  - Engineering Capacity Planning Sheet
  - Customer Interview Summary (Lisa)
"""


@tool(
    description="获取与主题相关的内部文档。为演示目的返回模拟数据。"
)
def get_internal_docs(topic: str) -> str:
    """返回模拟的内部文档。"""
    return f"""
Related Internal Documents for: {topic}

1. Q4 Product Metrics Dashboard
   - MAU: 45,000 (up 18% QoQ)
   - Revenue: $2.3M (up 23% YoY)
   - Churn: 4.2% (down from 5.1%)
   - NPS: 62 (up from 54)
   - Key insight: Enterprise customers drive 70% of revenue

2. Q1 Roadmap Draft v2 (Lisa Zhang, Jan 28)
   - Theme: "Reliable Foundation"
   - Priority 1: Platform stability (reduce P1 incidents by 50%)
   - Priority 2: Enterprise features (SSO, audit logs, compliance)
   - Priority 3: AI-powered insights (beta)
   - Engineering ask: 3 additional backend engineers

3. Engineering Capacity Planning
   - Current team: 12 engineers (4 backend, 3 frontend, 2 infra, 2 ML, 1 mobile)
   - Q1 committed: 70% on reliability, 20% on enterprise, 10% on AI
   - Risk: ML team stretched thin if AI features accelerated
   - Hiring pipeline: 2 offers out (1 backend, 1 infra)

4. Customer Interview Summary (Lisa Zhang, Jan 30)
   - Interviewed 15 enterprise customers
   - Top requests: SSO (12/15), better API docs (10/15), audit logs (9/15)
   - Surprise finding: 8/15 want AI-powered anomaly detection
   - Quote: "We'd pay 2x for enterprise tier with SSO and compliance"
"""


# ---------------------------------------------------------------------------
# 工作流 Agent
# ---------------------------------------------------------------------------
meeting_parser = Agent(
    name="Meeting Parser",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[get_meeting_details],
    instructions=[
        "你负责解析会议详情并确定需要做哪些准备工作。",
        "提取：与会者、议程项目、上次的行动项、待解决问题。",
        "输出一份结构化的摘要，说明需要调研和准备的内容。",
    ],
)

attendee_researcher = Agent(
    name="Attendee Researcher",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "你负责调研与会者，为会议提供背景信息。",
        "对每位与会者，查找：近期公开动态、公司新闻、相关背景。",
        "重点关注与会议主题相关的信息。",
        "对于内部同事，记录其职位和近期贡献。",
    ],
)

context_gatherer = Agent(
    name="Internal Context Gatherer",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[get_internal_docs],
    instructions=[
        "你负责收集与会议相关的内部文档和数据。",
        "获取指标、历史决策、行动项和相关文档。",
        "总结每份文档中与会议议程相关的要点。",
    ],
)

external_researcher = Agent(
    name="External Context Researcher",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "你负责调研与会议主题相关的外部背景信息。",
        "关注：市场趋势、竞争对手动态、行业基准。",
        "重点收集能为会议决策提供参考的信息。",
        "保持调研结果简洁且可操作。",
    ],
)

prep_synthesizer = Agent(
    name="Prep Synthesizer",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你负责将所有调研结果汇编为会议准备简报。",
        "",
        "按以下结构组织简报：",
        "## 会议概览",
        "- 参会人、议题、时间、地点",
        "",
        "## 与会者背景",
        "- 每位与会者的简介及其可能关注的优先事项",
        "",
        "## 关键数据要点",
        "- 你应当随时掌握的指标和事实",
        "",
        "## 历史决策与行动项",
        "- 上次会议的决策及行动项的完成状态",
        "",
        "## 建议讨论要点",
        "- 5-7 个具体要点，附支撑数据",
        "",
        "## 可能被问到的问题",
        "- 其他人可能提出的问题及建议回答",
        "",
        "## 决策要点",
        "- 本次会议需要做出的决定",
        "",
        "保持内容可操作。这是一份让你有备而来的会议速查手册。",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 工作流
# ---------------------------------------------------------------------------
meeting_prep_workflow = Workflow(
    id="meeting-prep",
    name="Meeting Prep",
    steps=[
        Step(name="Parse Meeting", agent=meeting_parser),
        Parallel(
            Step(name="Research Attendees", agent=attendee_researcher),
            Step(name="Gather Internal Context", agent=context_gatherer),
            Step(name="Research External Context", agent=external_researcher),
            name="Deep Research",
        ),
        Step(name="Synthesize Prep Brief", agent=prep_synthesizer),
    ],
)

if __name__ == "__main__":
    test_cases = [
        "Prepare me for my 10 AM Product Strategy Review meeting",
        "Prepare me for the Q1 roadmap review with our CEO and VP Product.",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Meeting prep workflow test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        meeting_prep_workflow.print_response(prompt, stream=True)
