# Performance Eval Cookbooks（性能评估示例集）

性能示例对 Agent（代理）和 Team（团队）的运行时与内存影响进行基准测试。

## 文件列表

- `async_function.py` - 异步函数性能基准测试。
- `db_logging.py` - 带 PostgreSQL 日志记录的性能基准测试。
- `instantiate_agent.py` - Agent（代理）实例化基准测试。
- `instantiate_agent_with_tool.py` - 配置工具的 Agent（代理）实例化基准测试。
- `instantiate_team.py` - Team（团队）实例化基准测试。
- `response_with_memory_updates.py` - 启用内存更新的响应性能测试。
- `response_with_storage.py` - 带存储历史记录的响应性能测试。
- `simple_response.py` - 单次响应基线性能基准测试。
- `team_response_with_memory_simple.py` - 单 Team（团队）内存影响基准测试。
- `team_response_with_memory_multi_user.py` - 多用户并发 Team（团队）内存基准测试。
- `team_response_with_memory_and_reasoning.py` - 带推理工具和大型工具输出的 Team（团队）内存基准测试。
- `comparison/` - 框架对比基准测试。
