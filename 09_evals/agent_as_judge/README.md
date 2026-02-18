# Agent-as-Judge Eval Cookbooks（Agent 作为裁判的评估示例集）

Agent-as-judge（Agent 作为裁判）示例使用基于模型的评分来评估输出质量。

## 文件列表

- `agent_as_judge_basic.py` - 同步与异步数值评分，结果持久化存储。
- `agent_as_judge_post_hook.py` - 同步与异步后置钩子评估示例。
- `agent_as_judge_batch.py` - 批量案例评估，含汇总输出。
- `agent_as_judge_binary.py` - PASS/FAIL（通过/失败）质量评估示例。
- `agent_as_judge_custom_evaluator.py` - 使用自定义 Evaluator（评估器）Agent。
- `agent_as_judge_team.py` - 评估 Team（团队）生成响应的质量。
- `agent_as_judge_team_post_hook.py` - Team（团队）后置钩子质量检查。
- `agent_as_judge_with_guidelines.py` - 带附加指导方针的数值评分。
- `agent_as_judge_with_tools.py` - 评估使用工具的 Agent（代理）的响应。
