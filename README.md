# Agno Cookbook 中文版

数百个示例，复制、粘贴、运行。

## 从哪里开始

**刚接触 Agno？** 从 [00_quickstart](./00_quickstart) 开始 — 逐步介绍基础知识，每个示例递进式构建。

**想看实际案例？** 跳转到 [01_demo](./01_demo) — 高级用例。运行示例、拆解它们、从中学习。

**想探索特定主题？** 在下方找到你的使用场景。

---

## 按使用场景构建

### 构建单个 Agent
[02_agents](./02_agents) — Agno 的原子单元。从这里开始了解工具、RAG、结构化输出、多模态、护栏等。

### 多 Agent 协作
[03_teams](./03_teams) — 协调多个 Agent。异步流程、共享记忆、分布式 RAG、推理模式。

### 编排复杂流程
[04_workflows](./04_workflows) — 将 Agent、团队和函数串联为自动化管道。

### 部署和管理 Agent
[05_agent_os](./05_agent_os) — 部署到 Web API、Slack、WhatsApp 等。Agent 系统的控制平面。

---

## 深入探索

### 存储
[06_storage](./06_storage) — 为 Agent 提供持久化存储。推荐 Postgres 和 SQLite，也支持 DynamoDB、Firestore、MongoDB、Redis、SingleStore、SurrealDB 等。

### 知识库与 RAG
[07_knowledge](./07_knowledge) — 为 Agent 提供运行时可搜索的信息。涵盖分块策略（语义、递归、智能体式）、嵌入器、向量数据库、混合搜索，以及从 URL、S3、GCS、YouTube、PDF 等加载数据。

### 学习
[08_learning](./08_learning) — Agent 统一学习系统。决策日志、偏好跟踪和持续改进。

### 评估
[09_evals](./09_evals) — 衡量关键指标：准确性（LLM 作为评判者）、性能（延迟、内存）、可靠性（预期工具调用）和 Agent 作为评判者模式。

### 推理
[10_reasoning](./10_reasoning) — 让 Agent 先思考再行动。三种方式：
- **推理模型** — 使用预训练的推理模型（o1、o3 等）
- **推理工具** — 为 Agent 提供推理工具（think、analyze）
- **推理框架** — 设置 `reasoning=True` 启用带工具调用的思维链

### 记忆
[11_memory](./11_memory) — 有记忆的 Agent。跨会话存储用户相关的见解和事实，提供个性化响应。

### 模型
[90_models](./90_models) — 40+ 模型提供商。Gemini、Claude、GPT、Llama、Mistral、DeepSeek、Groq、Ollama、vLLM — 市面上有的我们基本都支持。

### 工具
[91_tools](./91_tools) — 扩展 Agent 能力。网页搜索、SQL、邮件、API、MCP、Discord、Slack、Docker，以及使用 `@tool` 装饰器的自定义工具。

### 集成
[92_integrations](./92_integrations) — 连接 Discord、可观测性工具（Langfuse、Arize Phoenix、AgentOps、LangSmith）、记忆提供商和 A2A 协议。

---

## 包管理

本项目使用 [uv](https://docs.astral.sh/uv/) 管理依赖。

```bash
# 安装所有依赖
uv sync --group all

# 仅安装特定示例组的依赖
uv sync --group quickstart
uv sync --group demo
uv sync --group learning

# 运行示例
uv run python 00_quickstart/agent_search_over_knowledge.py
```
