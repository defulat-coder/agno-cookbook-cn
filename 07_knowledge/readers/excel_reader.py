from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.excel_reader import ExcelReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

reader = ExcelReader()

knowledge_base = Knowledge(
    vector_db=PgVector(
        table_name="excel_products_demo",
        db_url=db_url,
    ),
)

# 插入 Excel 文件 - ExcelReader 使用 openpyxl 处理 .xlsx，xlrd 处理 .xls
knowledge_base.insert(
    path="cookbook/07_knowledge/testing_resources/sample_products.xlsx",
    reader=reader,
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "你是一个产品目录助手。",
        "使用知识库回答有关产品的问题。",
        "数据来自包含产品和类别工作表的 Excel 工作簿。",
    ],
)

if __name__ == "__main__":
    agent.print_response(
        "目前有哪些电子产品有库存？包括它们的价格。",
        markdown=True,
        stream=True,
    )
    agent.print_response(
        "蓝牙音箱的价格是多少？",
        markdown=True,
        stream=True,
    )
