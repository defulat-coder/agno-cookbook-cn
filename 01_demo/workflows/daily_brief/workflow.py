"""
每日简报工作流
=====================

定时早间工作流，编制个性化的每日简报。
从日历、邮件、调研和数据中提取信息，为用户呈现一天的全貌。

步骤:
1. 并行：扫描日历 + 邮件摘要 + 新闻/调研
2. 综合生成每日简报

由于没有 Google OAuth 凭据，日历和邮件数据通过模拟工具提供。

测试:
    python -m workflows.daily_brief.workflow
"""

from agno.agent import Agent
from agno.models.openai import OpenAIResponses
from agno.tools import tool
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.workflow import Step, Workflow
from agno.workflow.parallel import Parallel

# ---------------------------------------------------------------------------
# 模拟工具（无 Google OAuth 可用）
# ---------------------------------------------------------------------------


@tool(description="获取今日日历事件。为演示目的返回模拟数据。")
def get_todays_calendar() -> str:
    """返回当日模拟的日历事件。"""
    return """
Today's Calendar (Thursday, February 6, 2025):

09:00 - 09:30 | Daily Standup
  Location: Zoom
  Attendees: Engineering team (Sarah Chen, Mike Rivera, Priya Patel)
  Notes: Sprint review week - come prepared with demo updates

10:00 - 11:00 | Product Strategy Review
  Location: Conference Room A
  Attendees: CEO (James Wilson), VP Product (Lisa Zhang), You
  Notes: Q1 roadmap finalization, budget discussion

12:00 - 12:30 | 1:1 with Sarah Chen
  Location: Zoom
  Attendees: Sarah Chen (Staff Engineer)
  Notes: Career growth discussion, tech lead promotion path

14:00 - 15:00 | Investor Update Prep
  Location: Your office
  Attendees: CFO (Robert Kim), You
  Notes: Prepare slides for next week's board meeting

16:00 - 16:30 | Interview: Senior Backend Engineer
  Location: Zoom
  Attendees: Candidate (Alex Thompson), You, Mike Rivera
  Notes: System design round
"""


@tool(description="获取今日邮件摘要。为演示目的返回模拟数据。")
def get_email_digest() -> str:
    """返回当日模拟的邮件摘要。"""
    return """
Email Digest (last 24 hours):

URGENT:
- From: Robert Kim (CFO) - "Q4 Revenue Numbers Final" - Sent 11:30 PM
  Preview: Final Q4 numbers are in. Revenue up 23% YoY. Need to discuss board deck.

- From: Sarah Chen - "Production Incident - Resolved" - Sent 2:15 AM
  Preview: API latency spike at 1:45 AM. Root cause: database connection pool exhaustion. Resolved by 2:10 AM. Post-mortem scheduled.

ACTION REQUIRED:
- From: Lisa Zhang (VP Product) - "Q1 Roadmap - Your Input Needed" - Sent 8:00 AM
  Preview: Need your engineering capacity estimates by EOD for the product strategy review.

- From: HR (Maria Santos) - "Sarah Chen Promotion Packet" - Sent yesterday
  Preview: Please review and approve Sarah's tech lead promotion packet before your 1:1.

FYI:
- From: Mike Rivera - "Interview Prep: Alex Thompson" - Sent 7:30 AM
  Preview: Attached resume and system design question options for today's interview.

- From: Engineering-all - "New deployment pipeline live" - Sent yesterday
  Preview: CI/CD improvements are live. Build times reduced by 40%.

- From: investor-relations@company.com - "Board Meeting Reminder" - Sent yesterday
  Preview: Board meeting next Thursday. Deck due by Monday.
"""


# ---------------------------------------------------------------------------
# 工作流 Agent
# ---------------------------------------------------------------------------
calendar_agent = Agent(
    name="Calendar Scanner",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[get_todays_calendar],
    instructions=[
        "你负责扫描今日日历并生成简明摘要。",
        "对每个会议，记录：时间、参会人、需要准备的内容。",
        "标记任何连续会议或日程冲突。",
        "突出当日最重要的会议。",
    ],
)

email_agent = Agent(
    name="Email Digester",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[get_email_digest],
    instructions=[
        "你负责处理邮件摘要并生成按优先级排列的总结。",
        "分类：紧急/需要行动/仅供参考。",
        "对于行动项，具体说明需要做什么。",
        "在相关时将邮件与今日日历关联起来。",
    ],
)

news_agent = Agent(
    name="News Scanner",
    model=OpenAIResponses(id="gpt-5.2"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "你负责扫描相关新闻和行业动态。",
        "重点关注：AI/ML 发展、竞争对手新闻、市场趋势。",
        "保持简洁——3-5 条最相关的内容。",
        "附上来源链接。",
    ],
)

synthesizer = Agent(
    name="Brief Synthesizer",
    model=OpenAIResponses(id="gpt-5.2"),
    instructions=[
        "你负责将日历、邮件和新闻的输入汇编为连贯的每日简报。",
        "",
        "按以下结构组织简报：",
        "## 今日概览",
        "- 一句话总结今天的安排",
        "",
        "## 优先行动",
        "- 今天需要关注的 3-5 件最重要的事（来自邮件 + 日历）",
        "",
        "## 日程安排",
        "- 今日会议及准备事项",
        "",
        "## 收件箱重点",
        "- 关键邮件摘要",
        "",
        "## 行业动态",
        "- 简要新闻摘要",
        "",
        "保持内容可快速浏览。用户应能在 2 分钟内读完。",
    ],
    markdown=True,
)

# ---------------------------------------------------------------------------
# 工作流
# ---------------------------------------------------------------------------
daily_brief_workflow = Workflow(
    id="daily-brief",
    name="Daily Brief",
    steps=[
        Parallel(
            Step(name="Scan Calendar", agent=calendar_agent),
            Step(name="Process Emails", agent=email_agent),
            Step(name="Scan News", agent=news_agent),
            name="Gather Intelligence",
        ),
        Step(name="Synthesize Brief", agent=synthesizer),
    ],
)

if __name__ == "__main__":
    test_cases = [
        "Generate my daily brief for today",
        "Generate a concise daily brief and prioritize urgent action items.",
    ]
    for idx, prompt in enumerate(test_cases, start=1):
        print(f"\n--- Daily brief workflow test case {idx}/{len(test_cases)} ---")
        print(f"Prompt: {prompt}")
        daily_brief_workflow.print_response(prompt, stream=True)
