# AgentOS RBAC - 基于角色的访问控制

此目录包含展示 AgentOS 的 RBAC（基于角色的访问控制）系统和 JWT 身份验证的示例。

## 概述

AgentOS RBAC 使用带有作用域的 JWT 令牌提供细粒度的访问控制。

**重要：** RBAC 是可选的。路由级授权检查（作用域验证、资源过滤）仅在 JWT 中间件上设置 `authorization=True` 时运行。如果没有此标志，JWT 令牌会被验证，但所有资源都可访问。

系统支持：

1. **全局资源作用域** - 某类型所有资源的权限
2. **每个资源的作用域** - 细粒度的 Agent/团队/工作流权限
3. **通配符支持** - 灵活的权限模式
4. **受众验证** - JWT `aud` 声明必须与 AgentOS ID 匹配

## AgentOS Control Plane

AgentOS 上的 RBAC 与 AgentOS Control Plane 兼容。连接 AgentOS 时，需要为来自 Control Plane 的流量启用"授权"，以获得具有正确作用域的所需 JWT 令牌。

有关 AgentOS 安全的更多信息，请参阅[文档](https://docs.agno.com/agent-os/security/overview)。

注意：AgentOS Control Plane 流量仅支持非对称密钥。连接 AgentOS 时，Control Plane 将提供公钥。

## JWT 签名算法

AgentOS 支持对称和非对称 JWT 签名：

| 算法 | 类型 | 用例 |
|-----------|------|----------|
| **RS256**（默认） | 非对称 | 生产环境 - 使用公钥/私钥对 |
| **HS256** | 对称 | 开发/测试 - 使用共享密钥 |

**此目录中的大多数示例使用 HS256（对称）以简化操作。** 这允许在不设置密钥对的情况下运行示例。对于生产部署，我们建议使用 RS256 非对称密钥。

有关非对称密钥示例，请参阅 `asymmetric/basic.py`，它演示了：
- RSA 密钥对生成
- 使用私钥签名令牌（认证服务器）
- 使用公钥验证令牌（AgentOS）

## 受众验证

JWT 令牌中的 `aud`（受众）声明用于验证令牌是否用于此 AgentOS 实例：

```python
# 令牌负载必须包含与 AgentOS ID 匹配的 aud 声明
payload = {
    "sub": "user_123",
    "aud": "my-agent-os",  # 必须与 AgentOS ID 匹配
    "scopes": ["agents:read", "agents:run"],
    "exp": datetime.now(UTC) + timedelta(hours=24),
}
```

当 `verify_audience=True` 时，具有不匹配 `aud` 声明的令牌将被拒绝并返回 401 错误。

## 作用域格式

### 1. 管理员作用域（最高权限）
```
agent_os:admin
```
授予对所有端点和资源的完全访问权限。

### 2. 全局资源作用域
格式：`resource:action`

示例：
```
system:read       # 读取系统配置
agents:read       # 列出所有 Agent
agents:run        # 运行任何 Agent
teams:read        # 列出所有团队
workflows:read    # 列出所有工作流
```

### 3. 每个资源的作用域  
格式：`resource:<resource-id>:action`

示例：
```
agents:my-agent:read              # 读取特定 Agent
agents:my-agent:run               # 运行特定 Agent
agents:*:run                      # 运行任何 Agent（通配符）
teams:my-team:read                # 读取特定团队
teams:*:run                       # 运行任何团队（通配符）
```

## 作用域层次结构

系统按以下顺序检查作用域：

1. **管理员作用域** - 授予所有权限
2. **通配符作用域** - 匹配如 `agents:*:run` 的模式
3. **特定作用域** - 资源和操作的精确匹配

## 端点过滤

### GET 端点（自动过滤）

列表端点根据用户作用域自动过滤结果：

- **GET /agents** - 仅返回用户有权访问的 Agent
- **GET /teams** - 仅返回用户有权访问的团队
- **GET /workflows** - 仅返回用户有权访问的工作流

**示例：**
```python
# 具有特定 Agent 作用域的用户：
# ["agents:agent-1:read", "agents:agent-2:read"]
GET /agents -> 仅返回 agent-1 和 agent-2

# 具有通配符资源作用域的用户：
# ["agents:*:read"]
GET /agents -> 返回所有 Agent

# 具有全局资源作用域的用户：
# ["agents:read"]
GET /agents -> 返回所有 Agent

# 具有管理员权限的用户：
# ["agent_os:admin"]
GET /agents -> 返回所有 Agent
```

### POST 端点（访问检查）

运行端点检查具有资源上下文的匹配作用域：

- **POST /agents/{agent_id}/runs** - 需要具有运行操作的 Agent 作用域
- **POST /teams/{team_id}/runs** - 需要具有运行操作的团队作用域
- **POST /workflows/{workflow_id}/runs** - 需要具有运行操作的工作流作用域

**运行 Agent "web-agent" 的有效作用域模式：**
- `agents:web-agent:run`（特定 Agent）
- `agents:*:run`（任何 Agent - 通配符）
- `agents:run`（全局作用域）
- `agent_os:admin`（完全访问）

## 示例

### 基本 RBAC（对称）
有关使用 HS256 对称密钥的简单示例，请参阅 `symmetric/basic.py`。

### 基本 RBAC（非对称） 
有关 RS256 非对称密钥示例（建议用于生产），请参阅 `asymmetric/basic.py`。

### 每个 Agent 的权限
有关每个 Agent 的自定义作用域映射，请参阅 `symmetric/agent_permissions.py`。

### 高级作用域
有关以下内容的综合示例，请参阅 `symmetric/advanced_scopes.py`：
- 全局和每个资源的作用域
- 通配符模式
- 多个权限级别
- 受众验证

## 快速开始

### 1. 启用 RBAC

有两种方式启用 RBAC：

**选项 A：通过 AgentOS 参数（推荐）**
```python
from agno.os import AgentOS

agent_os = AgentOS(
    id="my-agent-os",
    agents=[agent1, agent2],
    authorization=True,  # 启用 RBAC
    authorization_config=AuthorizationConfig(
        verification_keys=["your-public-key-or-secret"],  # 或设置 JWT_VERIFICATION_KEY 环境变量
        algorithm="RS256",  # 默认；对称密钥使用 "HS256"
    ),
)

app = agent_os.get_app()
```

**选项 B：直接通过 JWTMiddleware**
```python
from agno.os import AgentOS
from agno.os.middleware import JWTMiddleware

agent_os = AgentOS(
    id="my-agent-os",
    agents=[agent1, agent2],
)

app = agent_os.get_app()

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-public-key-or-secret"],
    algorithm="RS256",
    authorization=True,  # 启用 RBAC - 没有此项，作用域不会被强制执行
)
```

**注意：** 当 `authorization=False`（或未设置）时，JWT 令牌仍会被验证，但基于作用域的访问控制被禁用 - 所有经过身份验证的用户都可以访问所有资源。

### 2. 创建带有作用域和受众的 JWT 令牌

```python
import jwt
from datetime import datetime, timedelta, UTC

# 管理员用户
admin_token = jwt.encode({
    "sub": "admin_user",
    "aud": "my-agent-os",
    "scopes": ["agent_os:admin"],
    "exp": datetime.now(UTC) + timedelta(hours=24),
}, "your-secret", algorithm="HS256")

# 高级用户（对所有 Agent 的全局访问）
power_user_token = jwt.encode({
    "sub": "power_user",
    "aud": "my-agent-os",
    "scopes": [
        "agents:read",     # 列出所有 Agent
        "agents:*:run",    # 运行任何 Agent
    ],
    "exp": datetime.now(UTC) + timedelta(hours=24),
}, "your-secret", algorithm="HS256")

# 受限用户（仅特定 Agent）
limited_token = jwt.encode({
    "sub": "limited_user",
    "aud": "my-agent-os",
    "scopes": [
        "agents:agent-1:read",
        "agents:agent-1:run",
    ],
    "exp": datetime.now(UTC) + timedelta(hours=24),
}, "your-secret", algorithm="HS256")
```

### 3. 发起经过身份验证的请求

```bash
# 列出 Agent（按作用域过滤）
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:7777/agents

# 运行特定 Agent
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "message=Hello" \
  http://localhost:7777/agents/agent-1/runs
```

## 默认作用域映射

所有 AgentOS 端点都有默认的作用域要求：

```python
{
    # 系统
    "GET /config": ["system:read"],
    "GET /models": ["system:read"],
    
    # Agent
    "GET /agents": ["agents:read"],
    "GET /agents/*": ["agents:read"],
    "POST /agents/*/runs": ["agents:run"],
    
    # 团队
    "GET /teams": ["teams:read"],
    "POST /teams/*/runs": ["teams:run"],
    
    # 工作流
    "GET /workflows": ["workflows:read"],
    "POST /workflows/*/runs": ["workflows:run"],
    
    # Session
    "GET /sessions": ["sessions:read"],
    "POST /sessions": ["sessions:write"],
    "DELETE /sessions/*": ["sessions:delete"],
    
    # 更多...
}
```

有关默认作用域映射，请参阅 `/libs/agno/agno/os/scopes.py`。

## 自定义作用域映射

你可以覆盖或扩展默认映射：

```python
from agno.os.middleware import JWTMiddleware

app.add_middleware(
    JWTMiddleware,
    verification_keys=["your-public-key-or-secret"],
    algorithm="RS256",  # 默认；对称密钥使用 "HS256"
    authorization=True,
    verify_audience=True,  # 验证 aud 声明是否与 AgentOS ID 匹配
    scope_mappings={
        # 覆盖默认
        "GET /agents": ["custom:scope"],
        
        # 添加新端点
        "POST /custom/endpoint": ["custom:action"],
        
        # 允许无作用域
        "GET /public": [],
    }
)
```

## 安全最佳实践

1. **在生产环境中使用 RS256 非对称密钥** - 仅与 AgentOS 共享公钥。这是 AgentOS Control Plane 与 AgentOS 实例通信的方式。
2. **使用环境变量**存储密钥和密码
3. **设置适当的令牌过期时间**（exp 声明）
4. **在生产环境中使用 HTTPS**
5. **遵循最小权限原则** - 授予所需的最小作用域
6. **监控访问日志**以发现可疑活动

## 故障排除

### 401 未授权
- 令牌缺失或已过期
- JWT 密钥/密码无效
- 令牌格式不正确

### 403 禁止访问
- 用户缺少所需的作用域
- 资源无法使用用户的作用域访问

### GET /agents 中未显示 Agent
- 用户缺少这些 Agent 的读取作用域
- 检查 `agents:read` 和 `agents:<id>:read` 作用域

### 作用域未被强制执行
- 确保在 JWTMiddleware 或 AgentOS 上设置 `authorization=True`
- 如果没有此标志，会进行 JWT 验证，但会跳过作用域检查
- 所有经过身份验证的用户都可以访问所有资源

## 其他资源

- [AgentOS 文档](https://docs.agno.com/agent-os/security/overview)
- [JWT.io](https://jwt.io) - JWT 调试工具
