from typing import List

from agno.agent import Agent
from agno.knowledge.chunking.strategy import ChunkingStrategy
from agno.knowledge.document.base import Document
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.pgvector import PgVector


class CustomSeparatorChunking(ChunkingStrategy):
    """
    自定义分块策略的示例实现。

    这演示了如何通过以下方式实现自己的分块策略：
    1. 继承自 ChunkingStrategy
    2. 实现 chunk() 方法
    3. 使用继承的 clean_text() 方法
    4. 添加您自己的自定义逻辑和参数

    您可以根据特定需求扩展此模式：
    - 不同的分割逻辑（正则表达式模式、基于 AI 的分割等）
    - 自定义参数（max_words、min_length、overlap 等）
    - 特定领域的分块（代码块、表格、章节等）
    - 自定义元数据和块增强
    """

    def __init__(self, separator: str = "---", **kwargs):
        """
        初始化您的自定义分块策略。

        Args:
            separator: The string pattern to split documents on
            **kwargs: Additional parameters for your custom logic
        """
        self.separator = separator

    def chunk(self, document: Document) -> List[Document]:
        """
        Implement your custom chunking logic.

        This method receives a Document and must return a list of chunked Documents.
        You can implement any splitting logic here - this example uses simple separator splitting.
        """
        # Split by your custom separator
        chunks = document.content.split(self.separator)

        result = []
        for i, chunk_content in enumerate(chunks):
            # Use the inherited clean_text method for consistent text processing
            chunk_content = self.clean_text(chunk_content)

            if chunk_content:  # Only create non-empty chunks
                # Preserve original metadata and add chunk-specific info
                meta_data = document.meta_data.copy()
                meta_data["chunk"] = i + 1
                meta_data["separator_used"] = self.separator  # Your custom metadata
                meta_data["chunking_strategy"] = "custom_separator"

                result.append(
                    Document(
                        id=f"{document.id}_{i + 1}" if document.id else None,
                        name=document.name,
                        meta_data=meta_data,
                        content=chunk_content,
                    )
                )
        return result


# Example usage showing how to use your custom chunking strategy
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

knowledge = Knowledge(
    vector_db=PgVector(table_name="recipes_custom_strategy", db_url=db_url),
)

# Use your custom chunking strategy with any reader
# You can customize the separator based on your document structure:
# - "###" for markdown headers
# - "||" for data separators
# - "\n\n" for paragraph breaks
# - "---" for section dividers
# - Any custom pattern that fits your content
knowledge.insert(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
    reader=PDFReader(
        name="Custom Strategy Reader",
        chunking_strategy=CustomSeparatorChunking(separator="---"),
    ),
)

agent = Agent(
    knowledge=knowledge,
    search_knowledge=True,
)

agent.print_response("How to make Thai curry?", markdown=True)
