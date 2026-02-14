"""
展示如何在 AgentOS 中使用托管在 GCS 中的 JSON 文件作为数据库的示例。

GCS JSON 数据库设置：
- 使用存储在 Google Cloud Storage 中的 JSON 文件作为轻量级数据库
- 仅需要 GCS 存储桶名称 - 身份验证遵循标准 GCP 模式：
  * 本地开发：`gcloud auth application-default login`
  * 生产：将 GOOGLE_APPLICATION_CREDENTIALS 环境变量设置为服务帐户密钥路径
  * GCP 实例：自动使用实例元数据
- 可选的 prefix 参数用于组织文件（默认为空字符串）
- 根据需要在存储桶中自动创建 JSON 文件

前置条件：
1. 创建 GCS 存储桶
2. 确保适当的 GCS 权限
3. 安装 google-cloud-storage：`uv pip install google-cloud-storage`
"""

from agno.agent import Agent
from agno.db.gcs_json import GcsJsonDb
from agno.eval.accuracy import AccuracyEval
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.team.team import Team

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# 设置 GCS JSON 数据库
db = GcsJsonDb(bucket_name="agno_tests")


# 设置基本 agent 和基本团队
agent = Agent(
    name="JSON Demo Agent",
    id="basic-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    update_memory_on_run=True,
    enable_session_summaries=True,
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True,
    markdown=True,
)

team = Team(
    id="basic-team",
    name="JSON Demo Team",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    members=[agent],
    debug_mode=True,
)

# 评估示例
evaluation = AccuracyEval(
    db=db,
    name="JSON Demo Evaluation",
    model=OpenAIChat(id="gpt-4o"),
    agent=agent,
    input="What is 2 + 2?",
    expected_output="4",
    num_iterations=1,
)
# evaluation.run(print_results=True)

# 创建 AgentOS 实例
agent_os = AgentOS(
    id="json-demo-app",
    description="使用 JSON 文件数据库进行简单部署和演示的示例应用",
    agents=[agent],
    teams=[team],
)

app = agent_os.get_app()

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(app="gcs_json:app", reload=True)
