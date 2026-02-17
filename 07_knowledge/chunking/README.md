# Text Chunking（文本分块）

分块将大型文档分解为可管理的片段，以便在数据库中进行高效的知识检索和处理。

## 设置

```bash
uv pip install agno openai
```

设置您的 OpenAI API 密钥：

```bash
export OPENAI_API_KEY=your_api_key
```

## 基础集成

分块策略与 reader 集成以处理文档：

```python
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.chunking.semantic import SemanticChunking

reader = PDFReader(
    chunking_strategy=SemanticChunking()
)
knowledge.add_content(url="document.pdf", reader=reader)

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response(
    "What are the key concepts covered in this document?",
    markdown=True
)
```

## 实现您自己的分块策略

您可以通过继承 `ChunkingStrategy` 并实现 `chunk()` 方法来实现自定义分块策略。这允许您创建针对您的内容和用例量身定制的特定领域的分块逻辑。

有关完整的演练，请参阅 [自定义策略示例](./custom_strategy_example.py)。

## 支持的分块策略

- **[Agentic Chunking](./agentic_chunking.py)** - AI 驱动的智能块边界
- **[CSV Row Chunking](./csv_row_chunking.py)** - 每个 CSV 行作为单独的块
- **[Document Chunking](./document_chunking.py)** - 将整个文档视为单个块
- **[Fixed Size Chunking](./fixed_size_chunking.py)** - 固定字符/token 长度的块
- **[Recursive Chunking](./recursive_chunking.py)** - 自然边界感知分块
- **[Semantic Chunking](./semantic_chunking.py)** - 语义连贯的块
- **[Custom Strategy Example](./custom_strategy_example.py)** - 学习如何实现您自己的分块策略
