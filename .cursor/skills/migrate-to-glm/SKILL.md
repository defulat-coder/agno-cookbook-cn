---
name: migrate-to-glm
description: 将 Agno 项目代码从 Gemini 模型迁移到 GLM 模型（OpenAILike）。用于用户需要切换模型、替换 Gemini 为 GLM、配置 OpenAI 兼容模型时。
---

# 迁移到 GLM 模型

将 Agno 项目中使用 Gemini 的代码迁移到 GLM 模型（通过 OpenAILike）。

## 适用场景

- 代码使用 `Gemini(id="gemini-3-flash-preview")`
- 需要切换到 GLM-4.7 或其他 OpenAI 兼容模型
- 需要统一项目的模型配置

## 迁移步骤

### 1. 检查当前代码

使用 Grep 查找所有使用 Gemini 的文件：

```bash
grep -r "from agno.models.google import Gemini" .
grep -r "Gemini(id=" .
```

### 2. 更新单个文件

对每个需要迁移的 Python 文件执行以下操作：

#### A. 替换 import 语句

```python
# 旧代码
from agno.models.google import Gemini

# 新代码
import os
from dotenv import load_dotenv
from agno.models.openai import OpenAILike

load_dotenv()
```

#### B. 替换模型配置

```python
# 旧代码
model=Gemini(id="gemini-3-flash-preview")

# 新代码
model=OpenAILike(
    id=os.getenv("MODEL_ID", "GLM-4.7"),
    base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
    api_key=os.getenv("MODEL_API_KEY"),
)
```

### 3. 配置环境变量

#### 创建或更新 .env 文件

在项目根目录创建 `.env` 文件：

```env
MODEL_ID=GLM-4.7
MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
MODEL_API_KEY=your-api-key-here
```

#### 确保 .env 在 .gitignore 中

检查 `.gitignore` 包含：

```gitignore
.env
```

### 4. 安装依赖

```bash
uv add python-dotenv openai sqlalchemy yfinance
```

## Embedder 迁移（知识库场景）

如果代码使用了知识库（Knowledge）和向量搜索，需要同时迁移 Embedder。

### 1. 替换 import

```python
# 旧代码
from agno.knowledge.embedder.google import GeminiEmbedder

# 新代码
from agno.knowledge.embedder.openai import OpenAIEmbedder
```

### 2. 替换 Embedder 配置

```python
# 旧代码
embedder=GeminiEmbedder(id="gemini-embedding-001")

# 新代码
embedder=OpenAIEmbedder(
    id=os.getenv("EMBEDDER_MODEL", "embedding-3"),
    api_key=os.getenv("EMBEDDER_API_KEY"),
    base_url=os.getenv("EMBEDDER_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
)
```

### 3. 更新 .env 文件

添加 Embedder 相关环境变量：

```env
# Agent 模型配置
MODEL_ID=GLM-4.7
MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
MODEL_API_KEY=your-api-key

# Embedder 配置（用于知识库向量化）
EMBEDDER_MODEL=embedding-3
EMBEDDER_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
EMBEDDER_API_KEY=your-embedder-api-key
```

**注意：** Embedder 的 `base_url` 使用标准端点（`paas/v4/`），不是 coding 端点。

### 4. 完整示例（Knowledge 场景）

**迁移前：**

```python
from agno.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.chroma import ChromaDb

knowledge = Knowledge(
    name="Agno Documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        embedder=GeminiEmbedder(id="gemini-embedding-001"),
    ),
)
```

**迁移后：**

```python
import os
from dotenv import load_dotenv

from agno.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.chroma import ChromaDb

load_dotenv()

knowledge = Knowledge(
    name="Agno Documentation",
    vector_db=ChromaDb(
        name="agno_docs",
        embedder=OpenAIEmbedder(
            id=os.getenv("EMBEDDER_MODEL", "embedding-3"),
            api_key=os.getenv("EMBEDDER_API_KEY"),
            base_url=os.getenv("EMBEDDER_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        ),
    ),
)
```

### 5. 智谱 AI Embedding 模型

**可用模型：**
- `embedding-3`：新一代向量模型（推荐）
- `embedding-2`：上一代模型

**API 端点：**
```
https://open.bigmodel.cn/api/paas/v4/embeddings
```

**向量维度：**
- embedding-3: 2048 维
- embedding-2: 1024 维

### 6. ChromaDB 兼容性问题

**Python 3.14 不兼容：**

当前 ChromaDB 与 Python 3.14 存在兼容性问题：

```
pydantic.v1.errors.ConfigError: unable to infer type for attribute "chroma_server_nofile"
```

**解决方案：**
1. **降级到 Python 3.12 或 3.13**（推荐）
2. **等待 ChromaDB 更新**
3. **改用其他向量数据库**（如 Qdrant、Weaviate）

**受影响文件：**
- `07_agent_search_over_knowledge.py`
- `08_custom_tool_for_self_learning.py`
- `10_human_in_the_loop.py`

## 完整示例

### 迁移前

```python
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

agent = Agent(
    name="Finance Agent",
    model=Gemini(id="gemini-3-flash-preview"),
    tools=[YFinanceTools()],
)
```

### 迁移后

```python
import os
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools

load_dotenv()

agent = Agent(
    name="Finance Agent",
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/coding/paas/v4"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    tools=[YFinanceTools()],
)
```

## 批量迁移工作流（推荐）

### 适用场景
- 目录下有多个文件需要迁移（如 00_quickstart 目录）
- 需要系统化地处理大量文件

### 完整流程

#### 1. 查找所有需要迁移的文件

使用 Grep 查找目录中所有使用 Gemini 的文件：

```bash
# 查找 import 语句
Grep pattern="from agno.models.google import Gemini" path="00_quickstart"

# 查找模型实例化
Grep pattern="model=Gemini" path="00_quickstart"
```

**输出示例：**
```
00_quickstart/03_agent_with_typed_input_output.py
00_quickstart/05_agent_with_memory.py
00_quickstart/06_agent_with_state_management.py
...
```

#### 2. 逐个文件迁移

对每个文件执行以下步骤：

**A. 替换 import 语句**

读取文件头部，找到 import 部分并替换：

```python
# 旧代码（多种变体）
from agno.models.google import Gemini

# 或
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.yfinance import YFinanceTools

# 新代码（统一格式）
import os

from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools

load_dotenv()
```

使用 StrReplace 精确替换，保持其他 import 不变。

**B. 替换所有模型配置**

一个文件可能有多个 Agent/MemoryManager 使用模型，需要全部替换：

```python
# 单个 Agent 的情况
model=Gemini(id="gemini-3-flash-preview")
# 替换为 ↓
model=OpenAILike(
    id=os.getenv("MODEL_ID", "GLM-4.7"),
    base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
    api_key=os.getenv("MODEL_API_KEY"),
)

# 多个 Agent 的情况（Team/Workflow）
# 文件中可能有 2-3 个 Agent，每个都需要替换
bull_agent = Agent(model=Gemini(...))  # 第 1 个
bear_agent = Agent(model=Gemini(...))  # 第 2 个
team = Team(model=Gemini(...))         # 第 3 个
```

**重要：** 使用 Grep 定位所有 `model=Gemini`，逐个替换。

#### 3. 处理特殊情况

**多 Agent 文件（Team/Workflow）**

文件包含多个 Agent 实例，需要替换所有：

```python
# 示例：11_multi_agent_team.py 有 3 个模型实例
bull_agent = Agent(model=Gemini(...))      # 替换 1
bear_agent = Agent(model=Gemini(...))      # 替换 2
multi_agent_team = Team(model=Gemini(...)) # 替换 3
```

**MemoryManager 模型配置**

```python
# 旧代码
memory_manager = MemoryManager(
    model=Gemini(id="gemini-3-flash-preview"),
    db=agent_db,
)

# 新代码
memory_manager = MemoryManager(
    model=OpenAILike(
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    db=agent_db,
)
```

#### 4. 批量提交策略

**推荐分批提交：**

```bash
# 第 1 批：基础文件（1-4）
git add 00_quickstart/01_agent_with_tools.py \
        00_quickstart/02_agent_with_structured_output.py \
        00_quickstart/03_agent_with_typed_input_output.py \
        00_quickstart/04_agent_with_storage.py
git commit -m "feat: 迁移基础示例文件到 GLM (01-04)"

# 第 2 批：高级特性（5-9）
git add 00_quickstart/05_agent_with_memory.py \
        00_quickstart/06_agent_with_state_management.py \
        00_quickstart/07_agent_search_over_knowledge.py \
        00_quickstart/08_custom_tool_for_self_learning.py \
        00_quickstart/09_agent_with_guardrails.py
git commit -m "feat: 迁移高级特性文件到 GLM (05-09)"

# 第 3 批：协作场景（10-12）
git add 00_quickstart/10_human_in_the_loop.py \
        00_quickstart/11_multi_agent_team.py \
        00_quickstart/12_sequential_workflow.py
git commit -m "feat: 迁移协作场景文件到 GLM (10-12)"
```

**或一次性提交：**

```bash
git add 00_quickstart/*.py
git commit -m "feat: 批量迁移 00_quickstart 所有文件到 GLM

- 迁移 01-12 所有示例文件到 OpenAILike + GLM-4.7
- 添加 dotenv 环境变量加载
- 统一模型配置方式
- 涵盖：基础、记忆、状态、知识库、工具、护栏、团队、工作流"
```

### 批量迁移实战经验

#### 00_quickstart 目录迁移总结

**文件数量：** 12 个 Python 文件  
**涉及模型实例：** 约 20+ 个（包括 Agent、Team、Workflow、MemoryManager）  
**耗时：** 约 15-20 分钟  

**关键发现：**

1. **import 替换模式一致**
   - 所有文件都遵循相同的 import 替换模式
   - 添加 `import os` 和 `load_dotenv()` 是固定操作

2. **模型配置位置不同**
   - 单 Agent 文件：1 个模型配置
   - Team 文件：2-3 个模型配置（成员 + 领导）
   - Workflow 文件：3 个模型配置（每个步骤）
   - Memory 文件：2 个模型配置（Agent + MemoryManager）

3. **容易遗漏的地方**
   - MemoryManager 的模型配置
   - Team 中 members 的模型配置
   - Workflow 中每个 Step 的 Agent 模型配置

4. **Grep 是关键工具**
   - 用于查找所有 `model=Gemini` 实例
   - 避免遗漏任何一个配置

#### 最佳实践

**迁移前：**
```bash
# 1. 查找文件列表
Grep pattern="from agno.models.google import Gemini" path="target_dir"

# 2. 统计需要替换的模型实例数量
Grep pattern="model=Gemini" path="target_dir"
```

**迁移中：**
- 按文件顺序逐个处理
- 每个文件先替换 import，再替换模型配置
- 使用 Grep 确认该文件所有 `model=Gemini` 已替换

**迁移后：**
```bash
# 验证没有遗漏
Grep pattern="Gemini\(id=" path="target_dir"
# 应该返回：无结果

# 测试运行（可选）
export MODEL_ID=GLM-4.7 \
       MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4 \
       MODEL_API_KEY=your-key
uv run target_dir/01_sample.py
```

### 处理顺序建议

按复杂度从低到高处理：

1. **简单文件**（单 Agent，1 个模型配置）
   - 01_agent_with_tools.py
   - 04_agent_with_storage.py
   - 09_agent_with_guardrails.py

2. **中等文件**（Agent + MemoryManager，2 个配置）
   - 05_agent_with_memory.py
   - 08_custom_tool_for_self_learning.py
   - 10_human_in_the_loop.py

3. **复杂文件**（多 Agent，3+ 个配置）
   - 11_multi_agent_team.py（3 个：bull + bear + team）
   - 12_sequential_workflow.py（3 个：data + analyst + report）

4. **特殊文件**（有额外注意事项）
   - 02_agent_with_structured_output.py（注意：GLM-4.7 不支持 output_schema）
   - 03_agent_with_typed_input_output.py（同上）
   - 06_agent_with_state_management.py（有自定义工具）
   - 07_agent_search_over_knowledge.py（有知识库配置）

## 注意事项

### 模型兼容性

- **GLM-4.7 不支持 `output_schema`（结构化输出）**
  - 如果代码使用了 `output_schema=SomeModel`，需要移除或改用 `glm-4-flash`
  - 错误表现：返回 Markdown 而非 JSON，导致解析失败

- **工具调用（Tool Calling）**：GLM-4.7 支持，正常工作
- **流式输出（Stream）**：支持
- **多轮对话（History）**：支持

### API 端点

GLM 模型有两个 API 端点：

```python
# 标准端点（推荐）
base_url="https://open.bigmodel.cn/api/paas/v4/"

# Coding 端点（某些场景）
base_url="https://open.bigmodel.cn/api/coding/paas/v4"
```

根据实际情况选择。

### 常见依赖

迁移时通常需要安装：

```bash
uv add python-dotenv  # 环境变量加载
uv add openai         # OpenAI SDK（OpenAILike 依赖）
uv add sqlalchemy     # 数据库支持
uv add yfinance       # 金融工具（如果使用）
```

## 验证迁移

### 检查清单

- [ ] 所有 `Gemini` import 已替换为 `OpenAILike`
- [ ] 添加了 `dotenv` 加载
- [ ] 模型配置使用环境变量
- [ ] `.env` 文件已创建并配置
- [ ] `.env` 在 `.gitignore` 中
- [ ] 依赖已安装（python-dotenv, openai）
- [ ] 测试运行成功

### 测试命令

```bash
# 方式 1：使用 .env 文件
uv run path/to/file.py

# 方式 2：直接 export（测试用）
export MODEL_ID=GLM-4.7 \
       MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4 \
       MODEL_API_KEY=your-key
uv run path/to/file.py
```

## 常见问题

### Q: 余额不足错误

```
Error code: 429 - {'error': {'code': '1113', 'message': '余额不足或无可用资源包,请充值。'}}
```

**解决**：检查 API key 余额，充值后重试。

**排查步骤：**
1. 确认 API key 正确配置在 `.env` 文件中
2. 登录智谱 AI 开放平台检查余额
3. 充值后重新运行

### Q: 结构化输出失败

```
WARNING  Failed to parse cleaned JSON: Expecting value: line 1 column 1 (char 0)
WARNING  Failed to convert response to output_schema
```

**原因**：GLM-4.7 不支持 `output_schema`，会返回 Markdown 格式而非 JSON。

**解决方案：**
1. **移除 `output_schema` 参数**（推荐）
   ```python
   agent = Agent(
       model=OpenAILike(...),
       # output_schema=StockAnalysis,  # 删除此行
   )
   ```

2. **改用文本解析**
   ```python
   response = agent.run("分析英伟达")
   # response.content 是 Markdown 文本，而非结构化对象
   print(response.content)
   ```

3. **换用支持结构化输出的模型**
   - `glm-4-flash` 可能支持（需测试）
   - 或保留 Gemini 用于结构化输出场景

**受影响文件：**
- `02_agent_with_structured_output.py`
- `03_agent_with_typed_input_output.py`

### Q: API 认证失败

```
ERROR    Model authentication error from OpenAI API: OPENAI_API_KEY not set.
```

**原因**：`.env` 文件未正确加载或环境变量未设置。

**解决方案：**

1. **检查 `.env` 文件位置**
   - 必须在项目根目录
   - 文件名为 `.env`（不是 `env.txt` 或其他）

2. **检查 `load_dotenv()` 调用**
   ```python
   from dotenv import load_dotenv
   load_dotenv()  # 必须在读取环境变量前调用
   ```

3. **手动 export 测试**
   ```bash
   export MODEL_ID=GLM-4.7
   export MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
   export MODEL_API_KEY=your-api-key
   uv run file.py
   ```

4. **检查依赖是否安装**
   ```bash
   uv add python-dotenv
   ```

### Q: 文件中有多个模型配置，如何确保全部替换？

**问题场景：**
- Team 文件有 3 个 Agent（bull + bear + team leader）
- Workflow 文件有 3 个 Step Agent
- Memory 文件有 Agent + MemoryManager

**解决方案：**

1. **使用 Grep 查找所有实例**
   ```bash
   Grep pattern="model=Gemini" path="file.py"
   ```

2. **逐个替换**
   - 不要假设只有 1 个
   - 按照 Grep 结果逐个确认

3. **验证完成**
   ```bash
   # 再次 Grep，应该无结果
   Grep pattern="Gemini\(id=" path="file.py"
   ```

**实战示例（11_multi_agent_team.py）：**
```python
# 第 1 个：bull_agent
model=Gemini(id="gemini-3-flash-preview")  # 替换

# 第 2 个：bear_agent  
model=Gemini(id="gemini-3-flash-preview")  # 替换

# 第 3 个：team
model=Gemini(id="gemini-3-flash-preview")  # 替换
```

### Q: 运行时提示找不到模块怎么办？

**常见缺失依赖：**

```bash
# ModuleNotFoundError: No module named 'sqlalchemy'
uv add sqlalchemy

# ModuleNotFoundError: No module named 'openai'
uv add openai

# ModuleNotFoundError: No module named 'yfinance'
uv add yfinance

# ModuleNotFoundError: No module named 'dotenv'
uv add python-dotenv
```

**一次性安装所有：**
```bash
uv add python-dotenv openai sqlalchemy yfinance
```

### Q: 应该使用哪个 API 端点？

**两个端点对比：**

| 端点 | URL | 适用场景 |
|------|-----|---------|
| **标准端点** | `https://open.bigmodel.cn/api/paas/v4/` | 通用场景，推荐使用 |
| **Coding 端点** | `https://open.bigmodel.cn/api/coding/paas/v4` | 代码生成、编程场景 |

**实战经验：**
- 00_quickstart 示例使用 **Coding 端点** 成功运行
- 两个端点在金融分析场景中表现相近
- 建议根据具体业务场景测试选择

**配置方式：**
```env
# 标准端点
MODEL_BASE_URL=https://open.bigmodel.cn/api/paas/v4/

# Coding 端点
MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
```

### Q: 迁移后性能有变化吗？

**实测对比（00_quickstart 示例）：**

| 指标 | Gemini 3 Flash | GLM-4.7 |
|------|----------------|---------|
| 响应速度 | 20-30s | 25-35s |
| 工具调用准确性 | 高 | 高 |
| 中文理解 | 好 | 优秀 |
| 推理质量 | 高 | 高 |
| Token 消耗 | 中等 | 中等 |

**关键发现：**
- GLM-4.7 在中文场景下表现更自然
- 工具调用（如 YFinanceTools）准确性相当
- 不支持结构化输出是主要限制

### Q: 如何处理 MemoryManager 的模型配置？

**问题：** MemoryManager 需要单独配置模型，容易遗漏。

**正确做法：**

```python
# 05_agent_with_memory.py 示例

# MemoryManager 的模型配置（容易遗漏）
memory_manager = MemoryManager(
    model=OpenAILike(  # 需要替换
        id=os.getenv("MODEL_ID", "GLM-4.7"),
        base_url=os.getenv("MODEL_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        api_key=os.getenv("MODEL_API_KEY"),
    ),
    db=agent_db,
)

# Agent 的模型配置
agent = Agent(
    model=OpenAILike(...),  # 也需要替换
    memory_manager=memory_manager,
)
```

**检查方法：**
```bash
# 查找所有 MemoryManager
Grep pattern="MemoryManager" path="file.py"

# 确认其模型配置也已替换
```

### Q: 知识库（Knowledge）场景如何迁移 Embedder？

**问题：** 使用知识库的文件需要同时迁移 Embedder 和 Agent 模型。

**完整迁移步骤：**

1. **替换 Embedder import**
   ```python
   # from agno.knowledge.embedder.google import GeminiEmbedder
   from agno.knowledge.embedder.openai import OpenAIEmbedder
   ```

2. **替换 Embedder 配置**
   ```python
   embedder=OpenAIEmbedder(
       id=os.getenv("EMBEDDER_MODEL", "embedding-3"),
       api_key=os.getenv("EMBEDDER_API_KEY"),
       base_url=os.getenv("EMBEDDER_BASE_URL"),
   )
   ```

3. **更新 .env 文件**
   ```env
   # 添加 Embedder 配置
   EMBEDDER_MODEL=embedding-3
   EMBEDDER_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
   EMBEDDER_API_KEY=your-embedder-key
   ```

4. **完整示例（07_agent_search_over_knowledge.py）：**
   ```python
   knowledge = Knowledge(
       vector_db=ChromaDb(
           embedder=OpenAIEmbedder(
               id=os.getenv("EMBEDDER_MODEL"),
               api_key=os.getenv("EMBEDDER_API_KEY"),
               base_url=os.getenv("EMBEDDER_BASE_URL"),
           ),
       ),
   )
   
   agent = Agent(
       model=OpenAILike(...),  # Agent 模型
       knowledge=knowledge,
   )
   ```

**受影响文件：**
- `07_agent_search_over_knowledge.py`
- `08_custom_tool_for_self_learning.py`
- `10_human_in_the_loop.py`

### Q: ChromaDB 在 Python 3.14 不兼容怎么办？

**错误信息：**
```
pydantic.v1.errors.ConfigError: unable to infer type for attribute "chroma_server_nofile"
```

**原因：** ChromaDB 依赖 Pydantic v1，与 Python 3.14 不兼容。

**解决方案：**

1. **降级 Python 版本**（推荐）
   ```bash
   # 使用 Python 3.12 或 3.13
   pyenv install 3.13.0
   pyenv local 3.13.0
   ```

2. **改用其他向量数据库**
   - **Qdrant**：支持 Python 3.14
   - **Weaviate**：支持 Python 3.14
   - **Milvus**：支持 Python 3.14

3. **等待 ChromaDB 更新**
   - 关注 ChromaDB GitHub 仓库
   - 等待兼容 Pydantic v2 的版本

**临时方案：**
- 跳过需要 ChromaDB 的示例文件
- 或在独立的 Python 3.12 环境中运行

### Q: Embedder 和 Agent 模型可以用不同的 API Key 吗？

**可以。** 实际上，这是推荐的做法。

**场景 1：使用相同 API Key**
```env
MODEL_API_KEY=shared-key
EMBEDDER_API_KEY=shared-key
```

**场景 2：使用不同 API Key**（推荐，便于成本跟踪）
```env
MODEL_API_KEY=agent-model-key  # 用于 GLM-4.7 推理
EMBEDDER_API_KEY=embedder-key  # 用于 embedding-3 向量化
```

**优势：**
- 分开计费和成本跟踪
- 不同场景配置不同的速率限制
- 提高安全性（最小权限原则）

### Q: Embedder 的 base_url 为什么和 Agent 不同？

**Agent 模型端点：**
```
https://open.bigmodel.cn/api/coding/paas/v4  # Coding 端点
```

**Embedder 端点：**
```
https://open.bigmodel.cn/api/paas/v4/  # 标准端点
```

**原因：**
- Agent 模型（GLM-4.7）在 Coding 端点表现更好
- Embedder 模型（embedding-3）使用标准端点
- 两个端点的 API 规范略有不同

**配置示例：**
```env
MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
EMBEDDER_BASE_URL=https://open.bigmodel.cn/api/paas/v4/
```

**注意：** Embedder 的 URL 末尾有斜杠 `/`。

## 性能对比

| 特性 | Gemini 3 Flash | GLM-4.7 |
|------|----------------|---------|
| 工具调用 | ✅ | ✅ |
| 结构化输出 | ✅ | ❌ |
| 流式输出 | ✅ | ✅ |
| 多轮对话 | ✅ | ✅ |
| 响应速度 | 快 | 快 |
| 中文支持 | 好 | 优秀 |

## 回滚方案

如果迁移后出现问题，快速回滚：

1. **还原 import**
   ```python
   from agno.models.google import Gemini
   ```

2. **还原模型配置**
   ```python
   model=Gemini(id="gemini-3-flash-preview")
   ```

3. **移除 dotenv**
   ```python
   # 删除这两行
   from dotenv import load_dotenv
   load_dotenv()
   ```

4. **安装 Gemini 依赖**
   ```bash
   uv add google-genai
   ```
