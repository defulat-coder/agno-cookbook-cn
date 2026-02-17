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

## 批量迁移工作流

对于多个文件的迁移：

1. **查找所有文件**
   ```bash
   grep -l "from agno.models.google import Gemini" **/*.py
   ```

2. **逐个文件迁移**
   - 使用 StrReplace 替换 import 部分
   - 使用 StrReplace 替换 model 配置部分

3. **测试迁移后的文件**
   ```bash
   export MODEL_ID=GLM-4.7
   export MODEL_BASE_URL=https://open.bigmodel.cn/api/coding/paas/v4
   export MODEL_API_KEY=your-key
   uv run path/to/file.py
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 迁移到 GLM 模型并添加环境变量配置"
   ```

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

### Q: 结构化输出失败

```
WARNING  Failed to parse cleaned JSON: Expecting value: line 1 column 1 (char 0)
WARNING  Failed to convert response to output_schema
```

**解决**：GLM-4.7 不支持 `output_schema`，移除该参数或换用支持的模型。

### Q: API 认证失败

```
ERROR    Model authentication error from OpenAI API: OPENAI_API_KEY not set.
```

**解决**：检查 `.env` 文件是否正确加载，或使用 export 手动设置。

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
