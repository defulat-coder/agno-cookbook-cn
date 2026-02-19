# Reasoning（推理）

Reasoning（推理）赋予 Agent 在响应前"思考"、在行动（即工具调用）后"分析"结果的能力，大幅提升 Agent 解决需要连续工具调用问题的能力。

推理 Agent 在响应前会经历一个内部思维链（Chain of Thought）过程，逐步推演不同思路，并在必要时进行验证和修正。Agno 支持 3 种推理方式：

1. Reasoning Models（推理模型）
2. Reasoning Tools（推理工具）
3. Reasoning Agents and Teams（推理 Agent 与团队）

## Reasoning Models（推理模型）

Reasoning Models 是经过预训练、用于推理的模型。你可以尝试任意 Agno 支持的模型，若该模型具备推理能力，则会自动用于推理。

查看[示例](./models/)。

### 独立推理模型

Agno 的一个强大特性是支持使用独立于主模型的推理模型。当你希望使用比主模型更强的推理模型时，这一功能非常实用。

查看[示例](./models/openai/reasoning_gpt_4_1.py)。

## Reasoning Tools（推理工具）

通过为模型提供"think"（思考）工具，可以为非推理模型提供专属的结构化思考空间，从而大幅提升其推理能力。这是一种简单却有效的为非推理模型添加推理能力的方法。

查看[示例](./tools/)。

## Reasoning Agents and Teams（推理 Agent 与团队）

Reasoning Agent 是 Agno 开发的一种新型多 Agent 系统，将思维链推理（Chain of Thought Reasoning）与工具使用相结合。

你可以通过设置 `reasoning=True` 为任意 Agent 启用推理功能。

当一个设置了 `reasoning=True` 的 Agent 接收到任务时，一个独立的"推理 Agent"会首先通过思维链解决问题。在每个步骤中，它会调用工具收集信息、验证结果并持续迭代，直到得出最终答案。推理 Agent 得出最终答案后，会将结果交还给原始 Agent 进行验证并生成响应。

查看[示例](./agents/)。
