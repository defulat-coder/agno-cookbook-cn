# Embedding Models（嵌入模型）

Embedder 将文本转换为向量表示，用于语义搜索和知识检索。Agno 支持多个嵌入提供商以适应不同的部署需求。

## 设置

选择您首选的提供商并安装依赖项：

```bash
# OpenAI（默认）
uv pip install agno openai
export OPENAI_API_KEY=your_api_key

# 使用 Ollama 的本地模型
uv pip install agno ollama

# HuggingFace 模型
uv pip install agno transformers torch

# 云提供商
uv pip install agno cohere google-generativeai
```

## 嵌入维度

不同的模型产生不同的向量维度。更高的维度可以捕获更细微的含义，但需要更多存储空间：

```python
# 示例维度大小
embedder_dimensions = {
    'text-embedding-3-small': 1536,
    'text-embedding-3-large': 3072,
    'cohere-embed-english-v3.0': 1024,
    'all-MiniLM-L6-v2': 384,
}
```

## 基础集成

Embedder 通过 Knowledge 系统与向量数据库集成：

```python
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.vectordb.pgvector import PgVector

knowledge = Knowledge(
    vector_db=PgVector(
        embedder=OpenAIEmbedder(),
        table_name="knowledge",
        db_url="your_db_url"
    )
)
```

## 支持的嵌入提供商

- **[AWS Bedrock](./aws_bedrock_embedder.py)** - AWS 模型
- **[Azure OpenAI](./azure_embedder.py)** - 通过 Azure 的 OpenAI 模型
- **[Cohere](./cohere_embedder.py)** - 多语言嵌入模型
- **[Fireworks](./fireworks_embedder.py)** - 快速推理嵌入模型
- **[Google Gemini](./gemini_embedder.py)** - Google 的嵌入模型
- **[HuggingFace](./huggingface_embedder.py)** - Transformers 库模型
- **[Jina](./jina_embedder.py)** - Jina AI 嵌入模型
- **[LangDB](./langdb_embedder.py)** - LangDB 嵌入服务
- **[Mistral](./mistral_embedder.py)** - Mistral AI 嵌入模型
- **[Nebius](./nebius_embedder.py)** - Nebius 嵌入服务
- **[Ollama](./ollama_embedder.py)** - 通过 Ollama 的本地模型
- **[OpenAI](./openai_embedder.py)** - OpenAI 嵌入模型（默认）
- **[Qdrant FastEmbed](./qdrant_fastembed.py)** - 快速本地嵌入
- **[SentenceTransformers](./sentence_transformer_embedder.py)** - 本地 transformer 模型
- **[Together](./together_embedder.py)** - Together AI 嵌入模型
- **[VoyageAI](./voyageai_embedder.py)** - VoyageAI 嵌入模型
