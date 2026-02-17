"""
AWS Bedrock Embedder v4
=======================

演示在 AWS Bedrock 上使用 Cohere v4 嵌入，支持可配置的维度。

需求：
- AWS 凭证（AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY）
- AWS 区域配置（AWS_REGION）
- 安装 boto3：pip install boto3
"""

from agno.knowledge.embedder.aws_bedrock import AwsBedrockEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
embedder_v4 = AwsBedrockEmbedder(
    id="cohere.embed-v4:0",
    output_dimension=1024,
    input_type="search_query",
)

# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge = Knowledge(
    vector_db=PgVector(
        table_name="ml_knowledge",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=AwsBedrockEmbedder(
            id="cohere.embed-v4:0",
            output_dimension=1024,
            input_type="search_document",
        ),
    ),
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    text = "What is machine learning?"
    embeddings = embedder_v4.get_embedding(text)
    print(f"模型: {embedder_v4.id}")
    print(f"嵌入（前5个）: {embeddings[:5]}")
    print(f"维度: {len(embeddings)}")

    print("\n--- 测试不同维度 ---")
    for dim in [256, 512, 1024, 1536]:
        emb = AwsBedrockEmbedder(id="cohere.embed-v4:0", output_dimension=dim)
        result = emb.get_embedding("Test text")
        print(f"维度 {dim}: 获得 {len(result)} 维向量")

    _ = knowledge


if __name__ == "__main__":
    main()
