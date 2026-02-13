# Team Modes（团队模式）

Agno 团队支持四种执行模式，控制团队领导如何与成员 agent 协调工作。

## 模式概览

| 模式 | 枚举 | 描述 | 最适合 |
|------|------|-------------|----------|
| **Coordinate（协调）** | `TeamMode.coordinate` | 领导选择成员、制定任务、综合结果 | 通用编排 |
| **Route（路由）** | `TeamMode.route` | 领导路由到一个专家，直接返回其响应 | 专家选择、语言路由 |
| **Broadcast（广播）** | `TeamMode.broadcast` | 领导向所有成员发送相同任务，综合结果 | 多视角分析、共识 |
| **Tasks（任务）** | `TeamMode.tasks` | 领导将目标分解为任务列表，执行时考虑依赖关系 | 复杂多步骤工作流、并行执行 |

## 使用方法

```python
from agno.team.mode import TeamMode
from agno.team.team import Team

team = Team(
    name="My Team",
    mode=TeamMode.coordinate,  # 或 .route、.broadcast、.tasks
    members=[...],
)
```

## 目录结构

```
modes/
  coordinate/
    01_basic.py              # 与两个专家的基本协调
    02_with_tools.py         # 成员拥有工具的协调
    03_structured_output.py  # 带结构化输出模式的协调
  route/
    01_basic.py              # 基本路由到特定语言的 agent
    02_specialist_router.py  # 路由到领域专家
    03_with_fallback.py      # 带后备 agent 的路由
  broadcast/
    01_basic.py              # 多视角分析的基本广播
    02_debate.py             # 结构化辩论的广播
    03_research_sweep.py     # 跨源并行研究的广播
  tasks/
    01_basic.py              # 基本任务分解和执行
    02_parallel.py           # 并行任务执行
    03_dependencies.py       # 带依赖链的任务
```

另请参阅 `../task_mode/` 了解更多高级任务模式示例（自定义工具、异步、多运行会话）。

## 运行

```bash
.venvs/demo/bin/python cookbook/03_teams/modes/coordinate/01_basic.py
```
