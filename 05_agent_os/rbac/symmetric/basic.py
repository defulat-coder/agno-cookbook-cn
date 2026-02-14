"""
AgentOS 的基础 RBAC 示例

此示例演示如何在 AgentOS 中使用中间件启用 RBAC（基于角色的访问控制）和 JWT 令牌身份验证。

前置条件：
- 设置 JWT_VERIFICATION_KEY 环境变量或将其传递给中间件
- 端点自动使用默认作用域映射进行保护
"""

import os
from datetime import UTC, datetime, timedelta

import jwt
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.config import AuthorizationConfig
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# JWT 密钥（生产环境中使用环境变量）
JWT_SECRET = os.getenv("JWT_VERIFICATION_KEY", "your-secret-key-at-least-256-bits-long")

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")

# 创建 agent
research_agent = Agent(
    id="research-agent",
    name="Research Agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
    markdown=True,
)

# 创建 AgentOS
agent_os = AgentOS(
    id="my-agent-os",
    description="RBAC 保护的 AgentOS",
    agents=[research_agent],
    authorization=True,
    authorization_config=AuthorizationConfig(
        verification_keys=[JWT_SECRET],
        algorithm="HS256",
    ),
)

# 获取应用并添加 RBAC 中间件
app = agent_os.get_app()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    运行启用了 RBAC 的 AgentOS。
    
    受众验证：
    - 令牌必须包含与 AgentOS ID 匹配的 `aud` 声明
    - 具有错误受众的令牌将被拒绝
    
    默认作用域映射保护所有端点：
    - GET /agents/{agent_id}: 需要 "agents:read"
    - POST /agents/{agent_id}/runs: 需要 "agents:run"
    - GET /sessions: 需要 "sessions:read"
    - GET /memory: 需要 "memory:read"
    - 等等
    
    作用域格式：
    - "agents:read" - 列出所有 agent
    - "agents:research-agent:run" - 运行特定 agent
    - "agents:*:run" - 运行任何 agent
    - "agent_os:admin" - 完全访问所有内容
    
    使用包含作用域的 JWT 令牌进行测试：
    """
    # 创建具有不同作用域的测试令牌
    # 注意：包含带有 AgentOS ID 的 `aud` 声明
    user_token_payload = {
        "sub": "user_123",
        "session_id": "session_456",
        "scopes": ["agents:read", "agents:run"],
        "exp": datetime.now(UTC) + timedelta(hours=24),
        "iat": datetime.now(UTC),
    }
    user_token = jwt.encode(user_token_payload, JWT_SECRET, algorithm="HS256")

    admin_token_payload = {
        "sub": "admin_789",
        "session_id": "admin_session_123",
        "scopes": ["agent_os:admin"],  # 管理员可以访问所有内容
        "exp": datetime.now(UTC) + timedelta(hours=24),
        "iat": datetime.now(UTC),
    }
    admin_token = jwt.encode(admin_token_payload, JWT_SECRET, algorithm="HS256")

    print("\n" + "=" * 60)
    print("RBAC 测试令牌")
    print("=" * 60)
    print("\n用户令牌（agents:read, agents:run）:")
    print(user_token)
    print("\n管理员令牌（agent_os:admin - 完全访问）:")
    print(admin_token)
    print("\n" + "=" * 60)
    print("\n测试命令:")
    print(
        '\ncurl -H "Authorization: Bearer '
        + user_token
        + '" http://localhost:7777/agents'
    )
    print(
        '\ncurl -H "Authorization: Bearer '
        + admin_token
        + '" http://localhost:7777/sessions'
    )
    print("\n" + "=" * 60 + "\n")

    agent_os.serve(app="basic:app", port=7777, reload=True)
