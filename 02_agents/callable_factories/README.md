# 可调用工厂

在运行时使用可调用工厂解析工具和团队成员。

与其传递静态列表，不如传递一个返回资源的**函数**。该函数在每次运行开始时被调用，并通过基于签名的参数注入接收上下文（`agent`、`team`、`run_context`、`session_state`）。

## 示例

- **[01_callable_tools.py](./01_callable_tools.py)** - 根据用户角色变化工具集（按 user_id 缓存）
- **[02_session_state_tools.py](./02_session_state_tools.py)** - 直接使用 `session_state` 作为参数，禁用缓存
- **[03_team_callable_members.py](./03_team_callable_members.py)** - 动态组装团队成员
