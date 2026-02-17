"""
AWS Bedrock Embedder
====================

演示通过 AWS Bedrock 使用 Cohere v3 嵌入和知识插入。

需求：
- AWS 凭证（AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY）
- AWS 区域配置（AWS_REGION）
- 安装 boto3：pip install boto3
"""

from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.knowledge.embedder.aws_bedrock import AwsBedrockEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
embedder = AwsBedrockEmbedder()

# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    vector_db=PgVector(
        table_name="recipes",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=AwsBedrockEmbedder(input_type="search_document"),
    ),
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    embeddings = embedder.get_embedding("The quick brown fox jumps over the lazy dog.")
    print(f"Embeddings (first 5): {embeddings[:5]}")
    print(f"Dimensions: {len(embeddings)}")

    knowledge.insert(
        url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
        reader=PDFReader(chunking_strategy=FixedSizeChunking(chunk_size=1500)),
    )


if __name__ == "__main__":
    main()
