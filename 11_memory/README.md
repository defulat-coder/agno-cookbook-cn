# Agent 记忆

本节演示 Agno Agent 如何在多次 Run、多个 Session 和多个 Agent 之间持久化和使用用户记忆。

## 目录结构

- `01_agent_with_memory.py` 到 `08_memory_tools.py`：Agent 核心记忆模式。
- `memory_manager/`：使用 PostgreSQL 直接调用 `MemoryManager` API 的示例。
- `optimize_memories/`：记忆优化策略示例。

> SurrealDB 记忆管理器示例已移至 `cookbook/92_integrations/surrealdb/`。

## 环境配置

### 1. 创建虚拟环境

```shell
python3 -m venv ~/.venvs/aienv
source ~/.venvs/aienv/bin/activate
```

### 2. 安装依赖

```shell
pip install -U psycopg sqlalchemy openai agno
```

### 3. 运行示例

```shell
python cookbook/11_memory/01_agent_with_memory.py
```
