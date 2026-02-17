from pathlib import Path

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.excel_reader import ExcelReader
from agno.models.openai import OpenAIChat
from agno.vectordb.pgvector import PgVector

db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# ExcelReader 自动为 .xls 文件使用 xlrd
# 日期值从 Excel 序列号转换为 ISO 格式
# 布尔值从 0/1 转换为 True/False
reader = ExcelReader()

knowledge_base = Knowledge(
    vector_db=PgVector(
        table_name="excel_legacy_xls",
        db_url=db_url,
    ),
)

data_path = Path(__file__).parent.parent / "testing_resources" / "legacy_data.xls"

knowledge_base.insert(
    path=str(data_path),
    reader=reader,
)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "你是传统 Excel 文件的数据助手。",
        "工作簿有两个工作表：销售数据和库存。",
        "销售数据包含：日期、产品、数量、价格、总计。",
        "库存包含：项目、可用（True/False）。",
        "日期采用 ISO 格式（YYYY-MM-DD）。",
    ],
)

if __name__ == "__main__":
    print("=" * 60)
    print("Excel 传统 XLS - .xls 格式兼容性")
    print("=" * 60)

    print("\n--- 查询 1：销售记录 ---\n")
    agent.print_response(
        "售出了哪些产品？包括日期和数量。",
        markdown=True,
        stream=True,
    )

    print("\n--- 查询 2：库存状态 ---\n")
    agent.print_response(
        "库存中目前有哪些可用的项目？",
        markdown=True,
        stream=True,
    )
