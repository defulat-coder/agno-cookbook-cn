"""
AWS Bedrock Reranker 与 PgVector 示例
====================================

演示使用 AWS Bedrock rerankers 与 PgVector 进行检索增强生成。

需求：
- AWS 凭证（AWS_ACCESS_KEY_ID、AWS_SECRET_ACCESS_KEY）
- AWS 区域配置（AWS_REGION）
- 安装 boto3：pip install boto3
- 运行中的 PostgreSQL 与 pgvector
"""

from agno.agent import Agent
from agno.knowledge.embedder.aws_bedrock import AwsBedrockEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reranker.aws_bedrock import (
    AmazonReranker,
    AwsBedrockReranker,
    CohereBedrockReranker,
)
from agno.models.aws.bedrock import AwsBedrock
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge_cohere = Knowledge(
    vector_db=PgVector(
        table_name="bedrock_rag_demo",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=AwsBedrockEmbedder(
            id="cohere.embed-multilingual-v3",
            input_type="search_document",
        ),
        reranker=AwsBedrockReranker(
            model="cohere.rerank-v3-5:0",
            top_n=5,
        ),
    ),
)

knowledge_convenience = Knowledge(
    vector_db=PgVector(
        table_name="bedrock_rag_demo_v2",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=AwsBedrockEmbedder(
            id="cohere.embed-v4:0",
            output_dimension=1024,
            input_type="search_document",
        ),
        reranker=CohereBedrockReranker(top_n=5),
    ),
)

knowledge_amazon = Knowledge(
    vector_db=PgVector(
        table_name="bedrock_rag_amazon",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
        embedder=AwsBedrockEmbedder(
            id="cohere.embed-multilingual-v3",
            input_type="search_document",
        ),
        reranker=AmazonReranker(
            top_n=5,
            aws_region="us-west-2",
        ),
    ),
)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    model=AwsBedrock(id="anthropic.claude-sonnet-4-20250514-v1:0"),
    knowledge=knowledge_cohere,
    markdown=True,
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    knowledge_cohere.insert(
        name="Agno Docs", url="https://docs.agno.com/introduction.md"
    )
    _ = knowledge_convenience
    _ = knowledge_amazon
    agent.print_response("关键特性有哪些？")


if __name__ == "__main__":
    main()
