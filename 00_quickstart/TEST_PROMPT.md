# 提示词：改进 Agno 测试套件

你正在改进 **Agno** AI Agent 框架的测试套件。你的主要目标是**消除不稳定的测试**（大多由集成测试中的 API 速率限制引起）并**为覆盖率空白添加新的单元测试**。

---

## 环境设置

在每个会话开始时按顺序运行以下命令：

```bash
# 1. 加载环境变量（API 密钥等）
direnv allow
eval "$(direnv export bash 2>/dev/null)"

# 2. 激活测试虚拟环境
source .venv/bin/activate

# 3. 如果 .venv 不存在，先创建它：
#    ./scripts/test_setup.sh

# 4. 按需安装缺失的库：
#    uv pip install <package>
```

---

## 运行测试

```bash
# 完整单元测试套件（带覆盖率）
./scripts/test.sh

# 单个子目录
pytest libs/agno/tests/unit/<subdir> -v

# 单个文件
pytest libs/agno/tests/unit/<path>/test_file.py -v

# 单个测试
pytest libs/agno/tests/unit/<path>/test_file.py::TestClass::test_name -v

# 显示输出
pytest ... -s

# 首次失败即停止
pytest ... -x

# 集成测试（需要通过 direnv 提供 API 密钥）
pytest libs/agno/tests/integration/<subdir> -v

# 特定模块的覆盖率
pytest libs/agno/tests/unit/<subdir> --cov=libs/agno/agno/<module> --cov-report=term-missing -v
```

---

## 测试套件结构

```
libs/agno/tests/
├── unit/           # 约 240 个文件，完全 mock，不进行真实 API 调用
├── integration/    # 约 360 个文件，真实 API 调用，真实数据库
└── system/         # 约 24 个文件，端到端测试，需要运行中的服务
```

**Pytest 配置** 在 `libs/agno/pyproject.toml` 中：
```toml
[tool.pytest.ini_options]
log_cli = true
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
```

**关键 fixtures** 位于：
- `libs/agno/tests/integration/conftest.py` — 共享的数据库 fixtures、异步客户端重置
- `libs/agno/tests/unit/*/conftest.py` — 按模块的 fixtures

---

## 不稳定问题

**根本原因：** 集成测试向 35+ 个 LLM 提供商发起真实 API 调用。速率限制（HTTP 429）导致间歇性失败，这并非代码 bug。

### 速率限制保护的现状

**35 个模型提供商中只有 4 个有速率限制保护：**
- `libs/agno/tests/integration/models/google/conftest.py`
- `libs/agno/tests/integration/models/groq/conftest.py`
- `libs/agno/tests/integration/models/cerebras/conftest.py`
- `libs/agno/tests/integration/models/sambanova/conftest.py`

**31 个提供商完全没有保护**，包括最常用的：OpenAI、Anthropic、Azure、AWS、Meta、Deepseek、Mistral、Cohere、xAI 等。

保护模式是一个 `conftest.py` pytest 钩子，将速率限制失败转换为跳过：

```python
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """将触发 <提供商> 速率限制（429）的测试跳过而非失败。"""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if call.excinfo is not None:
            error_msg = str(call.excinfo.value)
            full_repr = str(report.longrepr) if report.longrepr else ""
            sections_text = " ".join(content for _, content in report.sections)
            combined = (error_msg + full_repr + sections_text).lower()
            if any(p in combined for p in ["429", "rate limit", "rate_limit", "quota", "resource_exhausted"]):
                report.outcome = "skipped"
                report.longrepr = ("", -1, "Skipped: <提供商> rate limit (429)")
```

### 额外问题：大多数测试没有重试/退避机制

Google 集成测试在 Agent 上配置了重试/退避：
```python
agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    exponential_backoff=True,
    delay_between_retries=5,
)
```

但 OpenAI、Anthropic 和大多数其他提供商的测试没有：
```python
# 没有退避——单次 429 = 测试失败
agent = Agent(model=OpenAIChat(id="gpt-4o-mini"), telemetry=False)
```

---

## 任务 1：为所有集成模型测试添加速率限制保护

**对 `libs/agno/tests/integration/models/` 下每个还没有带速率限制钩子的 `conftest.py` 的提供商目录**，创建一个。

需要检查的完整提供商目录列表：
```
aimlapi, anthropic, aws, azure, cerebras*, cohere, cometapi, dashscope,
deepinfra, deepseek, fireworks, google*, groq*, huggingface, ibm, langdb,
litellm, litellm_openai, lmstudio, meta, mistral, nebius, nvidia, ollama,
openai, openrouter, perplexity, portkey, sambanova*, together, vercel,
vertexai, vllm, xai

(* = 已有保护)
```

**对每个未受保护的目录：**

1. 检查该目录中是否已存在 `conftest.py`
2. 如果存在，将 `pytest_runtest_makereport` 钩子添加进去（不要覆盖已有的 fixtures）
3. 如果不存在，创建一个仅包含该钩子的新 `conftest.py`
4. 在跳过消息中使用提供商名称（例如 `"Skipped: OpenAI rate limit (429)"`）

**同时为以下发起真实 API 调用的非模型集成测试目录添加钩子：**
- `libs/agno/tests/integration/agent/`（使用 OpenAI）
- `libs/agno/tests/integration/teams/`（使用 OpenAI）
- `libs/agno/tests/integration/workflows/`（使用 OpenAI）
- `libs/agno/tests/integration/embedder/`（使用 OpenAI）
- `libs/agno/tests/integration/reranker/`

对于这些，使用通用消息：`"Skipped: rate limit (429)"`。

---

## 任务 2：为缺少重试/退避的集成测试添加

对于创建了真实 Agent 实例但没有重试配置的集成测试，添加 `retries` 和 `exponential_backoff`：

**修改前：**
```python
agent = Agent(model=OpenAIChat(id="gpt-4o-mini"), telemetry=False)
```

**修改后：**
```python
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    retries=3,
    delay_between_retries=2,
    exponential_backoff=True,
    telemetry=False,
)
```

**范围：** 应用到以下目录的测试：
- `libs/agno/tests/integration/models/openai/`
- `libs/agno/tests/integration/models/anthropic/`
- `libs/agno/tests/integration/models/azure/`
- `libs/agno/tests/integration/models/aws/`
- `libs/agno/tests/integration/models/deepseek/`
- `libs/agno/tests/integration/models/mistral/`
- `libs/agno/tests/integration/models/cohere/`
- `libs/agno/tests/integration/models/xai/`
- `libs/agno/tests/integration/models/together/`
- `libs/agno/tests/integration/models/meta/`
- 其他所有实例化 Agent 但没有重试配置的提供商测试
- `libs/agno/tests/integration/agent/`（所有 Agent 集成测试）
- `libs/agno/tests/integration/teams/`（所有团队集成测试）
- `libs/agno/tests/integration/workflows/`（所有工作流集成测试）

**尽可能使用 fixtures。** 如果文件已有模型 fixture 如：
```python
@pytest.fixture(scope="module")
def openai_model():
    return OpenAIChat(id="gpt-4o-mini")
```

则将重试配置添加到 Agent 创建处，而非模型 fixture。优先使用 Agent 级别的配置。

**对于内联创建 Agent 的测试**（不通过 fixture），直接添加重试参数。

**不要为以下添加重试：**
- 专门测试错误处理的测试（例如 `test_exception_handling`）
- 明确测试重试行为的测试（例如 `test_retries.py`）
- 单元测试（它们都是 mock 的）

---

## 任务 3：修复或移除真正不稳定的单元测试

运行完整的单元测试套件并修复所有失败：

```bash
pytest libs/agno/tests/unit/ -v 2>&1
```

**重要：只修改测试文件，不要修改 `libs/agno/agno/` 中的生产代码。**

### 已知失败模式（优先修复这些）

**1. 环境变量泄漏到默认参数**

工具类在 `__init__` 中使用 `getenv("SOME_KEY")` 作为默认参数值。默认参数在导入时求值，因此 direnv 设置的任何值都会被永久固定。运行时操作 `os.environ` 的测试无法覆盖它。

示例：`libs/agno/agno/tools/jina.py`：
```python
def __init__(self, api_key: Optional[str] = getenv("JINA_API_KEY"), ...):
```

修复方式：在测试中显式传值，不依赖默认值。或使用 `monkeypatch.setattr` 在构造前 patch 模块级别的默认值。或使用 `monkeypatch.delenv` / `monkeypatch.setenv` 结合重新导入。

已知文件：`libs/agno/tests/unit/tools/test_jina.py`

**2. `time.time` mock 耗尽（StopIteration）**

测试使用 `side_effect=[值列表]` mock `time.time`，但 Python 的 `logging` 模块在 `LogRecord.__init__` 中内部调用 `time.time()`。这些隐藏调用消耗了 mock 中的值，导致 `StopIteration`。

修复方式：使用永不耗尽的可调用对象替代有限列表：
```python
# 不要用：mock_time.side_effect = [0, 0, 1, 2, 3, 4, 5, 6]
# 改用：
call_count = 0
def fake_time():
    nonlocal call_count
    call_count += 1
    return call_count * 0.5

mock_time.side_effect = fake_time
```

或使用 `itertools.count()` 或永不耗尽的生成器。

已知文件：`libs/agno/tests/unit/tools/test_opencv.py`

**3. Patch 被测类本身（无效 patch）**

测试执行 `with patch("agno.tools.jina.JinaReaderTools"):`，但随后使用已导入的引用调用 `JinaReaderTools()`。这个 patch 没有实际作用。

修复方式：完全移除这些无效的 patch。

已知文件：`libs/agno/tests/unit/tools/test_jina.py`

**4. 单元测试中的速率限制/网络问题**

发起真实 HTTP 调用的测试可能因速率限制或网络问题而失败。

修复方式：确保所有外部调用都被正确 mock。单元测试绝不应该访问网络。

### 通用不稳定模式

| 模式 | 修复方式 |
|------|----------|
| 依赖执行顺序的测试 | 添加正确的 fixtures / setup |
| 使用硬编码文件路径的测试 | 使用 `tmp_path` 或 `tempfile` fixtures |
| 事件循环冲突的异步测试 | 集成 conftest 中的 `reset_async_client` autouse fixture 处理了这个；检查单元测试是否需要类似的处理 |
| Mock 了已变更接口的测试 | 更新 mock 以匹配当前签名 |
| 可选依赖导致的导入错误 | 添加 `@pytest.mark.skipif` 守卫 |

**如果测试根本不可靠且无法确定性化，移除它**并记录它测试的内容，以便编写替代测试。

---

## 任务 4：为覆盖率空白添加新的单元测试

稳定现有测试后，检查覆盖率：

```bash
pytest libs/agno/tests/unit/ --cov=libs/agno/agno --cov-report=term-missing -v
```

新测试聚焦于影响最大的**核心模块**：

1. **`agno/agent/`** — Agent 初始化、运行生命周期、工具分发、错误处理
2. **`agno/models/base.py`** — 重试逻辑、错误分类、退避计算
3. **`agno/team/`** — 团队协调、成员路由、委派
4. **`agno/memory/`** — 记忆存储、检索、摘要
5. **`agno/knowledge/`** — 知识库加载、分块、检索

### 测试编写指南

- 遵循相邻测试文件中的现有模式
- 使用基于类的组织：`class TestFeatureName:`
- 使用 `@pytest.mark.parametrize` 处理多种输入
- Mock 所有外部依赖——单元测试绝不能发起网络调用
- 为公共方法编写同步和异步两种变体
- 使用描述性命名：`test_<什么>_<条件>_<预期结果>`
- 没有变量时不使用 f-string
- 测试输出或注释中不使用 emoji

---

## 任务 5：验证全部通过

完成所有修改后运行：

```bash
# 完整单元测试套件
./scripts/test.sh

# 集成测试（预期有些跳过来自速率限制——这正是目的）
pytest libs/agno/tests/integration/ -v 2>&1 | tail -50

# 格式化和验证
./scripts/format.sh
./scripts/validate.sh
```

**成功标准：**
- 所有单元测试通过（零失败）
- 集成测试失败仅来自缺失的 API 密钥或服务，绝不来自速率限制（那些应该被跳过）
- `format.sh` 和 `validate.sh` 干净通过

---

## 规则

- **只修改测试文件** — 不要更改 `libs/agno/agno/` 中的生产代码
- 修复保持最小化和有针对性
- 不添加不必要的依赖
- 修改后运行 `format.sh` 和 `validate.sh`

---

## 工作顺序

按以下顺序处理任务：

1. **任务 1** 优先（速率限制 conftest 钩子）— 收益最大，纯粹的增量添加
2. **任务 2** 其次（Agent 上的重试/退避）— 从源头减少速率限制触发
3. **任务 3** 然后（修复不通过的单元测试）— 稳定基础
4. **任务 4** 最后（新单元测试）— 在稳定基础上构建
5. **任务 5** 最终验证

---

## 输出

在 `.context/test-improvement-log.md` 中维护一个运行日志：

```markdown
## 已添加速率限制保护
- [ ] 提供商名称 — conftest.py 已创建/更新

## 已添加重试/退避
- [ ] path/to/test_file.py — N 个 Agent 已更新

## 已修复的测试
- [ ] path/to/test_file.py::test_name — 修复描述

## 已移除的测试
- [ ] path/to/test_file.py::test_name — 移除原因

## 已添加的测试
- [ ] path/to/test_file.py::test_name — 填补了什么空白

## 最终状态
- 单元测试：通过/失败（N 通过，N 失败，N 跳过）
- 集成测试：通过/失败（N 通过，N 失败，N 跳过）
- format.sh：通过/失败
- validate.sh：通过/失败
```
