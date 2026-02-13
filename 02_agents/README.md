# Agno Agents Cookbook - 开发者指南

欢迎使用 **Agno Agents Cookbook** - 这是您使用 Agno 构建智能 AI Agent 的综合指南。本 cookbook 包含实用示例、模式和最佳实践，帮助您使用 Agno 的 agent 框架创建强大的 AI 应用程序。

- [特性](#特性)
  - [Tool 集成](#tool-集成)
  - [RAG 与知识库](#rag-与知识库)
  - [Human-in-the-Loop](#human-in-the-loop)
  - [多模态能力](#多模态能力)
  - [异步与性能](#异步与性能)
  - [状态管理](#状态管理)
  - [事件处理与流式输出](#事件处理与流式输出)
  - [Parser 与 Output Models](#parser-与-output-models)
  - [高级模式](#高级模式)

### 核心 Agent 特性

| 特性 | 描述 
|---------|-------------
| **Memory** | 持久化对话历史与学习能力 
| **Tools** | 外部 API 集成与函数调用 
| **State Management** | 基于会话的上下文与数据持久化 
| **Multimodal** | 图像、音频、视频处理能力 
| **Human-in-the-Loop** | 用户确认与输入工作流 
| **Async Support** | 高性能并发操作 
| **RAG Integration** | 知识检索与增强生成


### Tool 集成
**外部 API、函数和能力**

Agent 可以使用 Agno ToolKits、自定义函数，或为复杂集成构建自定义 Toolkit 类。

**示例：**
- 查看 `cookbook/90_tools/` 了解 tool 集成模式

### RAG 与知识库
**检索增强生成与知识系统**

将 agent 连接到向量数据库和知识库，实现智能文档检索与问答。

**示例：**
- [`rag/traditional_rag_lancedb.py`](./rag/traditional_rag_lancedb.py) - 基于向量的知识检索
- [`rag/agentic_rag_pgvector.py`](./rag/agentic_rag_pgvector.py) - 使用 Pgvector 的 Agentic RAG
- [`rag/agentic_rag_with_reranking.py`](./rag/agentic_rag_with_reranking.py) - 带重排序的增强检索

查看所有示例 [这里](./rag) 

### Human-in-the-Loop
**用户确认、输入和交互式工作流**

构建可以暂停等待用户确认、收集动态输入或集成需要人工监督的外部系统的 agent。

**示例：**
- [`human_in_the_loop/confirmation_required.py`](./human_in_the_loop/confirmation_required.py) - Tool 执行确认
- [`human_in_the_loop/user_input_required.py`](./human_in_the_loop/user_input_required.py) - 动态用户输入收集
- [`human_in_the_loop/external_tool_execution.py`](./human_in_the_loop/external_tool_execution.py) - 外部系统集成

查看所有示例 [这里](./human_in_the_loop)

### 多模态能力
**图像、音频和视频处理**

处理和分析多种媒体类型，包括图像、音频文件和视频内容。

**示例：**
- [`multimodal/image_to_text.py`](./multimodal/image_to_text.py) - 图像分析与描述
- [`multimodal/audio_sentiment_analysis.py`](./multimodal/audio_sentiment_analysis.py) - 音频处理
- [`multimodal/video_caption_agent.py`](./multimodal/video_caption_agent.py) - 视频内容理解

查看所有示例 [这里](./multimodal)

### 异步与性能
**高性能和并发操作**

构建支持异步操作的高性能 agent，实现并发操作和实时流式输出。

**示例：**
- [`async/basic.py`](./async/basic.py) - 基础异步 agent 用法
- [`async/gather_agents.py`](./async/gather_agents.py) - 并发 agent 执行
- [`async/streaming.py`](./async/streaming.py) - 实时流式响应

查看所有示例 [这里](./async)

### 状态管理
**会话持久化与上下文管理**

维护跨会话的对话状态，存储用户数据，并通过持久化上下文管理多轮交互。

**示例：**
- [`state/session_state_basic.py`](./state/session_state_basic.py) - 基础会话状态用法
- [`state/session_state_in_instructions.py`](./state/session_state_in_instructions.py) - 在指令中使用状态
- [`state/session_state_multiple_users.py`](./state/session_state_multiple_users.py) - 多用户场景

查看所有示例 [这里](./state)

### 事件处理与流式输出
**实时事件监控与流式传输**

在流式输出期间捕获 agent 事件，用于监控、调试或构建具有实时更新的交互式 UI。

**示例：**
- [`events/basic_agent_events.py`](./events/basic_agent_events.py) - Tool 调用事件处理
- [`events/reasoning_agent_events.py`](./events/reasoning_agent_events.py) - 推理事件捕获

### Parser 与 Output Models
**针对不同处理阶段的专用模型**

为推理与解析结构化输出使用不同的模型，或为生成最终响应使用专用模型，优化成本和性能。

**Parser Model 优势：**
- 使用更便宜的解析模型优化成本
- 更好的结构化输出一致性
- 将推理与解析关注点分离

**Output Model 优势：**
- 最终响应的质量控制
- 不同用例的风格一致性
- 昂贵最终生成的成本管理

**示例：**
- [`other/parse_model.py`](./other/parse_model.py) - 用于结构化输出的 Parser model
- [`other/output_model.py`](./other/output_model.py) - 用于最终响应的 Output model

### 其他模式

其他一些模式包括数据库集成、会话管理以及用于生产应用的依赖注入。

**示例：**
- [`db/`](./db/) - 数据库集成模式
- [`session/`](./session/) - 高级会话管理  
- [`dependencies/`](./dependencies/) - 依赖注入模式

---