# 01 quickstart（快速入门）

01_quickstart 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- 01_basic_coordination.py - 演示基本协调。
- 02_respond_directly_router_team.py - 演示响应直接路由器团队。
- 03_delegate_to_all_members.py - 演示委派给所有成员。
- 04_respond_directly_with_history.py - 演示带历史记录的直接响应。
- 05_team_history.py - 演示团队历史记录。
- 06_history_of_members.py - 演示成员历史记录。
- 07_share_member_interactions.py - 演示共享成员交互。
- 08_concurrent_member_agents.py - 演示并发成员 agent。
- broadcast_mode.py - 演示广播模式。
- caching/cache_team_response.py - 演示缓存团队响应。
- nested_teams.py - 演示嵌套团队。
- task_mode.py - 演示任务模式。
