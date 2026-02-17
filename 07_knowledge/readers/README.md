# Readers（文档读取器）

Reader 将原始数据转换为结构化的、可搜索的知识，供您的 Agent 使用。Agno 支持多种文档类型和数据源。

## 基础集成

Reader 与 Knowledge 系统集成以处理不同的数据源：

```python
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader

knowledge = Knowledge(vector_db=your_vector_db)
knowledge.add_content(
    path="documents/",
    reader=PDFReader(),
    metadata={"source": "docs"}
)

agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)
```

## 支持的 Reader

- **[ArXiv](./arxiv_reader.py)** - ArXiv 的学术论文
- **[ArXiv Async](./arxiv_reader_async.py)** - 异步 ArXiv 处理
- **[CSV](./csv_reader.py)** - 逗号分隔值文件
- **[CSV Async](./csv_reader_async.py)** - 异步 CSV 处理
- **[CSV from URL Async](./csv_reader_url_async.py)** - 从 URL 读取 CSV 文件
- **[Document Knowledge Base](./doc_kb_async.py)** - 多个文档源
- **[Excel](./excel_reader.py)** - Excel 工作簿（.xlsx、.xls）
- **[Excel Legacy XLS](./excel_legacy_xls.py)** - 旧版 .xls 格式支持
- **[Firecrawl](./firecrawl_reader.py)** - 高级网页抓取
- **[JSON](./json_reader.py)** - JSON 数据和 API 响应
- **[Markdown Async](./markdown_reader_async.py)** - Markdown 文档
- **[PDF Async](./pdf_reader_async.py)** - 带 OCR 的 PDF 文档
- **[PPTX](./pptx_reader.py)** - PowerPoint 演示文稿文件
- **[PPTX Async](./pptx_reader_async.py)** - 异步 PowerPoint 处理
- **[Web](./web_reader.py)** - 网站爬取和抓取 
