from typing import Optional

from agno.agent import Agent
from agno.knowledge.embedder.openai import OpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.qdrant import Qdrant
from qdrant_client import QdrantClient

# ---------------------------------------------------------
# 此部分加载知识库。如果您的知识库已在其他地方填充，请跳过。
# 定义 embedder
embedder = OpenAIEmbedder(id="text-embedding-3-small")
# 初始化向量数据库连接
vector_db = Qdrant(
    collection="thai-recipes", url="http://localhost:6333", embedder=embedder
)
# 加载知识库
knowledge = Knowledge(
    vector_db=vector_db,
)

knowledge.insert(
    url="https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf",
)

# ---------------------------------------------------------


# 定义自定义知识检索器
# 这是 Agent 将用来检索文档的函数
def knowledge_retriever(
    query: str, agent: Optional[Agent] = None, num_documents: int = 5, **kwargs
) -> Optional[list[dict]]:
    """
    自定义知识检索器函数，用于在向量数据库中搜索相关文档。

    参数：
        query (str): 搜索查询字符串
        agent (Agent): 发起查询的 Agent 实例
        num_documents (int): 要检索的文档数量（默认：5）
        **kwargs: 其他关键字参数

    返回：
        Optional[list[dict]]: 检索到的文档列表，如果搜索失败则返回 None
    """
    try:
        qdrant_client = QdrantClient(url="http://localhost:6333")
        query_embedding = embedder.get_embedding(query)
        results = qdrant_client.query_points(
            collection_name="thai-recipes",
            query=query_embedding,
            limit=num_documents,
        )
        results_dict = results.model_dump()
        if "points" in results_dict:
            return results_dict["points"]
        else:
            return None
    except Exception as e:
        print(f"向量数据库搜索期间出错: {str(e)}")
        return None


def main():
    """主函数，演示 Agent 使用。"""
    # 使用自定义知识检索器初始化 Agent
    # Knowledge 对象是注册 search_knowledge_base 工具所必需的
    # knowledge_retriever 覆盖默认的检索逻辑
    agent = Agent(
        knowledge=knowledge,
        knowledge_retriever=knowledge_retriever,
        search_knowledge=True,
        instructions="在知识库中搜索信息",
    )

    # 示例查询
    query = "列出制作 Massaman Gai 的配料"
    agent.print_response(query, markdown=True)


if __name__ == "__main__":
    main()
