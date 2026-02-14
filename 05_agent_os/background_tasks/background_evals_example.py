"""
示例：AgentOS 中使用 AgentAsJudgeEval 的每个钩子后台控制

此示例演示对哪些钩子在后台运行的细粒度控制：
- 为评估实例设置 eval.run_in_background = True
- AgentAsJudgeEval 基于自定义标准评估输出质量
"""

from agno.agent import Agent
from agno.db.sqlite import AsyncSqliteDb
from agno.eval.agent_as_judge import AgentAsJudgeEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置数据库
db = AsyncSqliteDb(db_file="tmp/agent_as_judge_evals.db")

# 用于完整性的 AgentAsJudgeEval - 同步运行（阻塞响应）
completeness_eval = AgentAsJudgeEval(
    db=db,
    name="Completeness Check",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="响应应该彻底、完整，并解决问题的所有方面",
    print_results=True,
    print_summary=True,
    telemetry=True,
)
# completeness_eval.run_in_background = False（默认 - 阻塞）

# 用于质量的 AgentAsJudgeEval - 在后台运行（非阻塞）
quality_eval = AgentAsJudgeEval(
    db=db,
    name="Quality Assessment",
    model=OpenAIChat(id="gpt-5.2"),
    criteria="响应应该结构良好、简洁且专业",
    scoring_strategy="numeric",
    threshold=8,
    additional_guidelines=[
        "检查响应是否易于理解",
        "验证响应是否不过于冗长",
    ],
    print_results=True,
    print_summary=True,
    run_in_background=True,  # 将此评估作为后台任务运行
)

agent = Agent(
    id="geography-agent",
    name="GeographyAgent",
    model=OpenAIChat(id="gpt-5.2"),
    instructions="你是一个有用的地理助手。提供准确且简洁的答案。",
    db=db,
    post_hooks=[
        completeness_eval,  # run_in_background=False - 首先运行，阻塞
        quality_eval,  # run_in_background=True - 在响应后运行
    ],
    markdown=True,
    telemetry=False,
)

# 创建 AgentOS
agent_os = AgentOS(agents=[agent])
app = agent_os.get_app()

# 流程：
# 1. Agent 处理请求
# 2. 同步钩子运行（completeness_eval）
# 3. 响应发送给用户
# 4. 后台钩子运行（quality_eval）

# 测试方式：
# curl -X POST http://localhost:7777/agents/geography-agent/runs \
#   -F "message=What is the capital of France?" -F "stream=false"

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="background_evals_example:app", port=7777, reload=True)
