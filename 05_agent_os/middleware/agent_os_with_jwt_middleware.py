"""
此示例演示如何在 AgentOS 中使用我们的 JWT 中间件。

中间件提取 JWT 声明并将其存储在 request.state 中以便轻松访问。
此示例使用默认的 Authorization 标头方法。

对于基于 cookie 的身份验证，请参阅 agent_os_with_jwt_cookies.py
对于标头和 cookie 支持，使用 token_source=TokenSource.BOTH
"""

from datetime import UTC, datetime, timedelta

import jwt
from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.openai import OpenAIChat
from agno.os import AgentOS
from agno.os.middleware import JWTMiddleware

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# JWT 密钥（生产环境中使用环境变量）
JWT_SECRET = "a-string-secret-at-least-256-bits-long"

# 设置数据库
db = PostgresDb(db_url="postgresql+psycopg://ai:ai@localhost:5532/ai")


# 定义一个使用依赖声明的工具
def get_user_details(dependencies: dict):
    """
    获取当前用户的详细信息。
    """
    return {
        "name": dependencies.get("name"),
        "email": dependencies.get("email"),
        "roles": dependencies.get("roles"),
    }


# 创建 agent
research_agent = Agent(
    id="user-agent",
    model=OpenAIChat(id="gpt-4o"),
    db=db,
    tools=[get_user_details],
    instructions="你是一个用户 agent，如果用户要求，可以获取用户详细信息。",
)


agent_os = AgentOS(
    description="JWT 保护的 AgentOS",
    agents=[research_agent],
)

# 获取最终应用
app = agent_os.get_app()

# 将 JWT 中间件添加到应用
# 此中间件将自动将 JWT 值提取到 request.state
app.add_middleware(
    JWTMiddleware,
    verification_keys=[JWT_SECRET],
    algorithm="HS256",
    user_id_claim="sub",  # 从 'sub' 声明中提取 user_id
    session_id_claim="session_id",  # 从 'session_id' 声明中提取 session_id
    dependencies_claims=["name", "email", "roles"],
    # 在此示例中，我们希望此中间件演示参数注入，而不是令牌验证。
    # 在生产场景中，你可能还需要令牌验证。将此设置为 False 时要小心。
    validate=False,
)

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """
    运行带有 JWT 参数注入的 AgentOS。

    通过调用 /agents/user-agent/runs 并发送消息进行测试："你知道关于我的什么信息？"
    """
    # 带有 user_id 和 session_id 的测试令牌：
    payload = {
        "sub": "user_123",  # 这将作为 user_id 参数注入
        "session_id": "demo_session_456",  # 这将作为 session_id 参数注入
        "exp": datetime.now(UTC) + timedelta(hours=24),
        "iat": datetime.now(UTC),
        # 依赖声明
        "name": "John Doe",
        "email": "john.doe@example.com",
        "roles": ["admin", "user"],
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    print("测试令牌:")
    print(token)
    agent_os.serve(app="agent_os_with_jwt_middleware:app", port=7777, reload=True)
