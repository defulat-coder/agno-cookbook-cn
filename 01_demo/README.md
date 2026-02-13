# Agno 演示

6 个自学习 Agent、2 个团队和 2 个工作流，通过 AgentOS 提供服务。每个 Agent 从交互中学习，并在每次使用中不断改进。

## 架构

所有 Agent 共享共同的基础设施：

- **模型**：`OpenAIResponses(id="gpt-5.2")`
- **存储**：PostgreSQL + PgVector，用于知识库、学习记录和聊天历史
- **知识库**：双知识库系统 —— 静态精选知识 + 运行时发现的动态学习内容
- **搜索**：混合搜索（语义 + 关键词），使用 OpenAI 嵌入（`text-embedding-3-small`）
- **学习**：`LearningMachine` 处于 `AGENTIC` 模式 —— Agent 自主决定何时保存学习内容

## Agents

### Dash - 自学习数据 Agent

通过 SQL 分析 F1 赛车数据集。提供洞察和上下文，而不仅仅是原始查询结果。跨会话记住列特性、日期格式和成功的查询。

### Scout - 自学习上下文 Agent

使用类 grep 搜索和完整文档阅读，在公司 S3 存储中查找信息（上下文）。了解存在哪些数据源，并将查询路由到正确的存储桶。从重复使用中学习用户意图。

### Pal - 会学习的个人 Agent

捕获和检索个人知识：笔记、书签、联系人、会议、项目。使用 DuckDB 存储结构化内容，使用学习系统存储模式和研究发现。

### Seek - 深度研究 Agent

进行详尽的多源研究，产出结构清晰、来源可靠的报告。遵循 4 阶段方法论：界定范围、收集、分析、综合。

### Dex - 关系智能 Agent

为你互动的人建立动态档案。跟踪互动、梳理人脉关系，并准备包含完整上下文的会议简报。

### Ace - 回复 Agent

起草邮件、消息和问题的回复。学习你的语气、沟通风格以及不同场景（客户 vs 团队 vs 高管）的偏好。

## 团队

| 团队 | 成员 | 模式 | 用途 |
|------|------|------|------|
| **研究团队** | Seek + Scout + Dex | 协调 | 将研究拆分为维度（外部、内部、人员），委托给专家。将发现综合为全面报告。 |
| **支持团队** | Ace + Scout + Dash | 路由 | 将问题路由到合适的专家：数据/指标给 Dash，内部文档给 Scout，起草给 Ace。 |

## 工作流

| 工作流 | 步骤 | 用途 |
|--------|------|------|
| **Daily Brief** | 3 个并行收集器（日历、邮件、新闻）+ 1 个综合器 | 晨间简报，包含优先级、日程要点、收件箱摘要和行业新闻。使用模拟日历/邮件数据和实时 DuckDuckGo 新闻。 |
| **Meeting Prep** | 解析会议 → 3 个并行研究员（参会者、内部文档、外部上下文）→ 1 个综合器 | 深度准备，包含参会者背景、关键数据点、讨论要点和预期问题。使用模拟会议数据和实时 DuckDuckGo。 |

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/agno-agi/agno.git
cd agno
```

### 2. 创建并激活 demo 虚拟环境
```bash
./scripts/demo_setup.sh
source .venvs/demo/bin/activate
```

### 3. 运行 PgVector
```bash
./cookbook/scripts/run_pgvector.sh
```

### 4. 为 Dash 加载数据（F1 数据集）
```bash
python -m cookbook.01_demo.agents.dash.scripts.load_data
python -m cookbook.01_demo.agents.dash.scripts.load_knowledge
```

### 5. 为 Scout 加载知识库（企业文档）
```bash
python -m cookbook.01_demo.agents.scout.scripts.load_knowledge
```

### 6. 导出环境变量
```bash
export OPENAI_API_KEY="..."      # 所有 Agent 必需
export EXA_API_KEY="..."         # 可选，因为 Exa MCP 目前免费
```

### 7. 运行 demo
```bash
python -m cookbook.01_demo.run
```

### 8. 通过 AgentOS 连接

- 在浏览器中打开 [os.agno.com](https://os.agno.com)
- 点击「添加 AgentOS」
- 添加 `http://localhost:7777` 作为端点
- 点击「连接」
- 你应该能看到 demo 的 Agent 和工作流
- 通过 Web 界面与 Agent 和工作流交互

### 评测

16 个测试用例，覆盖所有 Agent、两个团队和两个工作流。使用字符串匹配验证，支持 `all` 或 `any` 匹配模式。

```bash
# 运行所有 evals
python -m cookbook.01_demo.evals.run_evals

# 按 Agent 筛选
python -m cookbook.01_demo.evals.run_evals --agent dash

# 按类别筛选
python -m cookbook.01_demo.evals.run_evals --category dash_basic

# 详细模式（失败时显示完整响应）
python -m cookbook.01_demo.evals.run_evals --verbose
```
