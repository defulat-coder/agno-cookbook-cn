# Agent 快速入门指南

本指南介绍使用 Agno 构建 Agent 的基础知识。跟随本教程学习如何构建具有记忆、知识库、状态管理、护栏和人机协作功能的 Agent。我们还将构建多 Agent 团队和基于步骤的 Agent 工作流。

每个示例都可以独立运行，并包含详细注释帮助你理解底层原理。我们将使用 **Gemini 3 Flash** — 快速、经济且擅长工具调用的模型，当然你也可以通过一行代码切换到任何其他模型。

## 文件列表

| # | 文件 | 学习内容 | 核心特性 |
|:--|:---------|:------------------|:-------------|
| 01 | `01_agent_with_tools.py` | 为 Agent 提供工具以获取实时数据 | 工具调用、数据获取 |
| 02 | `02_agent_with_structured_output.py` | 返回类型化的 Pydantic 对象 | 结构化输出、类型安全 |
| 03 | `03_agent_with_typed_input_output.py` | 输入和输出的完整类型安全 | 输入 Schema、输出 Schema |
| 04 | `04_agent_with_storage.py` | 跨运行持久化对话 | 持久化存储、Session 管理 |
| 05 | `05_agent_with_memory.py` | 跨 Session 记住用户偏好 | Memory Manager、个性化 |
| 06 | `06_agent_with_state_management.py` | 跟踪、修改和持久化结构化 State | Session State、State 管理 |
| 07 | `07_agent_search_over_knowledge.py` | 将文档加载到知识库并使用混合搜索 | 分块、嵌入、混合搜索、Agentic 检索 |
| 08 | `08_custom_tool_for_self_learning.py` | 如何编写自定义工具并添加自学习能力 | 自定义工具、自学习 |
| 09 | `09_agent_with_guardrails.py` | 添加输入验证和安全检查 | 护栏、PII 检测、Prompt 注入检测 |
| 10 | `10_human_in_the_loop.py` | 执行工具前需要用户确认 | 人机协作、工具确认 |
| 11 | `11_multi_agent_team.py` | 通过组织多个 Agent 为团队来协调它们 | 多 Agent 团队、动态协作 |
| 12 | `12_sequential_workflow.py` | 按顺序执行 Agent/团队/函数 | Agentic 工作流、管道 |

## 核心概念

| 概念 | 作用 | 使用场景 |
|:--------|:-------------|:------------|
| **Tools（工具）** | 让 Agent 执行操作 | 获取数据、调用 API、运行代码 |
| **Storage（存储）** | 持久化对话历史 | 多轮对话和状态管理 |
| **Knowledge（知识库）** | 可搜索的文档存储 | RAG、文档问答 |
| **Memory（记忆）** | 记住用户偏好 | 个性化 |
| **State（状态）** | Agent 管理的结构化数据 | 跟踪进度、管理列表 |
| **Teams（团队）** | 多个 Agent 协作 | 专业 Agent 的动态协作 |
| **Workflows（工作流）** | 顺序执行的 Agent 管道 | 可预测的多步骤流程和数据流 |
| **Guardrails（护栏）** | 验证和过滤输入 | 阻止 PII、防止 Prompt 注入 |
| **Human in the Loop（人机协作）** | 操作前需要确认 | 敏感操作、安全关键工具 |

## 为什么选择 Gemini 3 Flash？

- **速度** — 亚秒级响应让 Agent 循环感觉更流畅
- **工具调用** — 开箱即用的可靠函数调用
- **经济实惠** — 足够便宜可以自由实验

Agno 是**模型无关的**，你可以通过一行代码切换到 OpenAI、Anthropic 或任何其他提供商。

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

### 2. 创建并激活虚拟环境
```bash
uv venv .quickstart --python 3.12
source .quickstart/bin/activate
```

### 3. 安装依赖
```bash
uv pip install -r cookbook/00_quickstart/requirements.txt
```

### 4. 设置 API key
```bash
export GOOGLE_API_KEY=your-google-api-key
```

### 5. 运行任意 cookbook
```bash
python cookbook/00_quickstart/01_agent_with_tools.py
```

**就这么简单。** 无需 Docker，无需 Postgres — 只需 Python 和一个 API key。

## 通过 Agent OS 运行

Agent OS 提供了一个 Web 界面来与你的 Agent 交互。启动服务器：

```bash
python cookbook/00_quickstart/run.py
```

然后访问 [os.agno.com](https://os.agno.com) 并添加 `http://localhost:7777` 作为端点。

以下是实际运行效果 — 与你的 Agent 聊天、探索 Session、监控跟踪、管理知识和记忆，所有这些都通过一个美观的可视化 UI 完成。

https://github.com/user-attachments/assets/aae0086b-86f6-4939-a0ce-e1ec9b87ba1f

> [!TIP]
> 要运行 agent-with-knowledge，请记得先使用以下命令加载知识库：
> ```bash
> python cookbook/00_quickstart/07_agent_search_over_knowledge.py
> ```

## 随时切换模型

Agno 是模型无关的。相同的代码，不同的提供商：

```python
# Gemini（这些示例中的默认选择）
from agno.models.google import Gemini
model = Gemini(id="gemini-3-flash-preview")

# OpenAI
from agno.models.openai import OpenAIResponses
model = OpenAIResponses(id="gpt-5.2")

# Anthropic
from agno.models.anthropic import Claude
model = Claude(id="claude-sonnet-4-5")
```

## 单独运行 Cookbook

```bash
# 01 - 工具：获取实时市场数据
python cookbook/00_quickstart/01_agent_with_tools.py

# 02 - 结构化输出：获取类型化响应
python cookbook/00_quickstart/02_agent_with_structured_output.py

# 03 - 类型化输入输出：完整类型安全
python cookbook/00_quickstart/03_agent_with_typed_input_output.py

# 04 - 存储：记住对话
python cookbook/00_quickstart/04_agent_with_storage.py

# 05 - 记忆：记住用户偏好
python cookbook/00_quickstart/05_agent_with_memory.py

# 06 - 状态：管理观察列表
python cookbook/00_quickstart/06_agent_with_state_management.py

# 07 - 知识库：搜索你的文档
python cookbook/00_quickstart/07_agent_search_over_knowledge.py

# 08 - 自定义工具：编写你自己的工具
python cookbook/00_quickstart/08_custom_tool_for_self_learning.py

# 09 - 护栏：输入验证和安全检查
python cookbook/00_quickstart/09_agent_with_guardrails.py

# 10 - 人机协作：执行前确认
python cookbook/00_quickstart/10_human_in_the_loop.py

# 11 - 团队：多头 vs 空头分析
python cookbook/00_quickstart/11_multi_agent_team.py

# 12 - 工作流：研究管道
python cookbook/00_quickstart/12_sequential_workflow.py
```

## 异步模式

本快速入门中的所有示例为简单起见都使用同步代码。对于 async/await 模式（推荐用于生产环境），请查看 `cookbook/02_agents/`，其中包含大多数功能的异步变体。

## 了解更多

- [Agno 文档](https://docs.agno.com)
- [Agent OS 概览](https://docs.agno.com/agent-os/introduction)
