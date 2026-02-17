目标：彻底测试和验证 `cookbook/07_knowledge`，使其符合我们的 cookbook 标准。

上下文文件（首先阅读这些）：
- `AGENTS.md` — 项目约定、虚拟环境、测试工作流
- `cookbook/STYLE_GUIDE.md` — Python 文件结构规则

环境：
- Python: `.venvs/demo/bin/python`
- API 密钥：通过 `direnv allow` 加载
- 数据库：`./cookbook/scripts/run_pgvector.sh`（向量数据库示例所需）

执行要求：
1. **在进行任何更改之前读取目标 cookbook 目录中的每个 `.py` 文件**。
   不要仅依赖 grep 或结构检查器 — 打开并阅读每个文件以了解其完整内容。这可确保您捕获自动检查器可能遗漏的问题（例如，section 内的 import、注释中过时的模型引用、不一致的模式）。

2. 为 `cookbook/07_knowledge/` 下的每个顶级子目录生成一个并行 agent。每个 agent 独立处理一个子目录，包括其中的任何嵌套子目录。

3. 每个 agent 必须：
   a. 运行 `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/07_knowledge/<SUBDIR> --recursive` 并修复任何违规。
   b. 使用 `.venvs/demo/bin/python` 运行该子目录（和嵌套子目录）中的所有 `*.py` 文件并捕获结果。跳过 `__init__.py`。
   c. 确保 Python 示例符合 `cookbook/STYLE_GUIDE.md`：
      - 带有 `=====` 下划线的模块 docstring
      - Section 分隔符：`# ---------------------------------------------------------------------------`
      - Docstring 和第一个分隔符之间的 import
      - `if __name__ == "__main__":` 门控
      - 无 emoji 字符
   d. 还要检查目录中的非 Python 文件（`README.md` 等）是否存在过时的 `OpenAIChat` 引用并更新它们。
   e. 仅在需要样式合规性的地方进行最小的、保持行为的编辑。
   f. 使用每个文件的最新 PASS/FAIL 条目更新 `cookbook/07_knowledge/<SUBDIR>/TEST_LOG.md`。

4. 所有 agent 完成后，收集并合并结果。

特殊情况：
- 这是**最大的 cookbook section 之一**，有许多子目录（chunking、embedders、vector_db、readers 等）。
- `vector_db/` 子目录需要特定的向量数据库服务 — 跳过任何需要不可用服务的（Pinecone、Weaviate、Qdrant、Milvus 等）。PgVector 示例应该可以使用 `run_pgvector.sh`。
- `embedders/` 子目录可能需要特定的嵌入提供商 API 密钥 — 如果不可用则跳过。
- `readers/` 子目录可能需要外部服务或大文件 — 验证 import 和基本设置，如果缺少依赖项则跳过。
- `cloud/` 示例需要云凭据 — 如果不可用则跳过。
- `01_quickstart/` 和 `filters/` 应该只需要 pgvector 和 OpenAI API 密钥即可工作。
- `testing_resources/` 包含测试数据，不是可运行示例 — 跳过。

验证命令（在完成之前必须全部通过）：
- `.venvs/demo/bin/python cookbook/scripts/check_cookbook_pattern.py --base-dir cookbook/07_knowledge/<SUBDIR> --recursive`（针对每个子目录）
- `source .venv/bin/activate && ./scripts/format.sh` — 格式化所有代码（ruff format）
- `source .venv/bin/activate && ./scripts/validate.sh` — 验证所有代码（ruff check、mypy）

最终响应格式：
1. 发现（不一致、失败、风险）及文件引用。
2. 运行的测试/验证命令及结果。
3. 任何剩余的差距或手动后续工作。
4. 此格式的结果表：

| 子目录 | 文件 | 状态 | 注释 |
|-------------|------|--------|-------|
| `01_quickstart` | `quickstart.py` | PASS | 知识库已加载和查询 |
| `vector_db/pinecone` | `pinecone_kb.py` | SKIP | Pinecone API 密钥不可用 |
