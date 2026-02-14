"""
提前停止 - 基础
================

演示使用 `StepOutput(stop=True)` 进行提前终止，跨直接步骤、`Steps` 容器和 Agent/函数工作流。
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.websearch import WebSearchTools
from agno.workflow import Step, Workflow
from agno.workflow.steps import Steps
from agno.workflow.types import StepInput, StepOutput

# ---------------------------------------------------------------------------
# 创建 Agent（安全部署）
# ---------------------------------------------------------------------------
security_scanner = Agent(
    name="Security Scanner",
    model=OpenAIChat(id="gpt-5.2"),
    instructions=[
        "你是一个安全扫描器。分析提供的代码或系统是否存在安全漏洞。",
        "如果未发现严重漏洞，返回 'SECURE'。",
        "如果检测到严重安全问题，返回 'VULNERABLE'。",
        "简要说明你的发现。",
    ],
)

code_deployer = Agent(
    name="Code Deployer",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="将通过安全审查的代码部署到生产环境。",
)

monitoring_agent = Agent(
    name="Monitoring Agent",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="为部署的应用程序设置监控和警报。",
)


# ---------------------------------------------------------------------------
# 定义安全门
# ---------------------------------------------------------------------------
def security_gate(step_input: StepInput) -> StepOutput:
    security_result = step_input.previous_step_content or ""
    print(f"安全扫描结果：{security_result}")

    if "VULNERABLE" in security_result.upper():
        return StepOutput(
            content="[警报] 安全警报：检测到严重漏洞。出于安全原因阻止部署。",
            stop=True,
        )
    return StepOutput(
        content="[通过] 安全检查通过。继续部署...",
        stop=False,
    )


# ---------------------------------------------------------------------------
# 创建安全工作流
# ---------------------------------------------------------------------------
security_workflow = Workflow(
    name="Secure Deployment Pipeline",
    description="Deploy code only if security checks pass",
    steps=[
        Step(name="Security Scan", agent=security_scanner),
        Step(name="Security Gate", executor=security_gate),
        Step(name="Deploy Code", agent=code_deployer),
        Step(name="Setup Monitoring", agent=monitoring_agent),
    ],
)

# ---------------------------------------------------------------------------
# 创建 Agent（内容质量管道）
# ---------------------------------------------------------------------------
content_creator = Agent(
    name="Content Creator",
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[WebSearchTools()],
    instructions="创建关于给定主题的吸引人内容。研究并撰写全面的文章。",
)

fact_checker = Agent(
    name="Fact Checker",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="验证事实并检查内容的准确性。标记任何错误信息。",
)

editor = Agent(
    name="Editor",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="编辑和润色内容以供发布。确保清晰度和流畅性。",
)

publisher = Agent(
    name="Publisher",
    model=OpenAIChat(id="gpt-4o-mini"),
    instructions="准备内容以供发布并处理最终格式化。",
)


# ---------------------------------------------------------------------------
# 定义质量门
# ---------------------------------------------------------------------------
def content_quality_gate(step_input: StepInput) -> StepOutput:
    content = step_input.previous_step_content or ""

    if len(content) < 100:
        return StepOutput(
            step_name="content_quality_gate",
            content="[失败] 质量检查失败：内容太短。停止工作流。",
            stop=True,
        )

    problematic_keywords = ["fake", "misinformation", "unverified", "conspiracy"]
    if any(keyword in content.lower() for keyword in problematic_keywords):
        return StepOutput(
            step_name="content_quality_gate",
            content="[失败] 质量检查失败：检测到问题内容。停止工作流。",
            stop=True,
        )

    return StepOutput(
        step_name="content_quality_gate",
        content="[通过] 质量检查通过：内容符合质量标准。",
        stop=False,
    )


# ---------------------------------------------------------------------------
# 创建内容工作流
# ---------------------------------------------------------------------------
content_pipeline = Steps(
    name="content_pipeline",
    description="Content creation pipeline with quality gates",
    steps=[
        Step(name="create_content", agent=content_creator),
        Step(name="quality_gate", executor=content_quality_gate),
        Step(name="fact_check", agent=fact_checker),
        Step(name="edit_content", agent=editor),
        Step(name="publish", agent=publisher),
    ],
)

content_workflow = Workflow(
    name="Content Creation with Quality Gate",
    description="Content creation workflow with early termination on quality issues",
    steps=[
        content_pipeline,
        Step(name="final_review", agent=editor),
    ],
)

# ---------------------------------------------------------------------------
# 创建 Agent（数据验证工作流）
# ---------------------------------------------------------------------------
data_validator = Agent(
    name="Data Validator",
    model=OpenAIChat(id="gpt-5.2"),
    instructions=[
        "你是一个数据验证器。分析提供的数据并确定其是否有效。",
        "要使数据有效，必须满足以下标准：",
        "- user_count：必须是正数（> 0）",
        "- revenue：必须是正数（> 0）",
        "- date：必须是合理的日期格式（YYYY-MM-DD）",
        "如果满足所有标准，返回确切的 'VALID'。",
        "如果任何标准失败，返回确切的 'INVALID'。",
        "同时简要解释你的推理。",
    ],
)

data_processor = Agent(
    name="Data Processor",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="处理和转换经过验证的数据。",
)

report_generator = Agent(
    name="Report Generator",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="从处理过的数据生成最终报告。",
)


# ---------------------------------------------------------------------------
# 定义验证门
# ---------------------------------------------------------------------------
def early_exit_validator(step_input: StepInput) -> StepOutput:
    validation_result = step_input.previous_step_content or ""

    if "INVALID" in validation_result.upper():
        return StepOutput(
            content="[失败] 数据验证失败。工作流提前停止以防止处理无效数据。",
            stop=True,
        )
    return StepOutput(
        content="[通过] 数据验证通过。继续处理...",
        stop=False,
    )


# ---------------------------------------------------------------------------
# 创建数据工作流
# ---------------------------------------------------------------------------
data_workflow = Workflow(
    name="Data Processing with Early Exit",
    description="Process data but stop early if validation fails",
    steps=[
        data_validator,
        early_exit_validator,
        data_processor,
        report_generator,
    ],
)

# ---------------------------------------------------------------------------
# 运行工作流
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== 测试有漏洞的代码部署 ===")
    security_workflow.print_response(
        input="Scan this code: exec(input('Enter command: '))"
    )

    print("=== 测试安全的代码部署 ===")
    security_workflow.print_response(
        input="Scan this code: def hello(): return 'Hello World'"
    )

    print("\n=== 测试：短内容（应提前停止）===")
    content_workflow.print_response(
        input="Write a short note about conspiracy theories",
        markdown=True,
        stream=True,
    )

    print("\n=== 测试无效数据 ===")
    data_workflow.print_response(
        input="Process this data: {'user_count': -50, 'revenue': 'invalid_amount', 'date': 'bad_date'}"
    )

    print("=== 测试有效数据 ===")
    data_workflow.print_response(
        input="Process this data: {'user_count': 1000, 'revenue': 50000, 'date': '2024-01-15'}"
    )
