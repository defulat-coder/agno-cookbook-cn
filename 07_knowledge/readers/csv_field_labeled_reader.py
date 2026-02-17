"""
字段标记的 CSV Reader
=====================

演示电影元数据的字段标记 CSV 导入。
"""

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.field_labeled_csv_reader import FieldLabeledCSVReader
from agno.vectordb.pgvector import PgVector

# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------
db_url = "postgresql+psycopg://ai:ai@localhost:5532/ai"

reader = FieldLabeledCSVReader(
    chunk_title="Movie Information",
    field_names=[
        "Movie Rank",
        "Movie Title",
        "Genre",
        "Description",
        "Director",
        "Actors",
        "Year",
        "Runtime (Minutes)",
        "Rating",
        "Votes",
        "Revenue (Millions)",
        "Metascore",
    ],
    format_headers=True,
    skip_empty_fields=True,
)


# ---------------------------------------------------------------------------
# 创建知识库
# ---------------------------------------------------------------------------
knowledge_base = Knowledge(
    vector_db=PgVector(
        table_name="imdb_movies_field_labeled_readr",
        db_url=db_url,
    ),
)


# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    instructions=[
        "你是一个电影专家助手。",
        "使用 search_knowledge_base 工具查找关于电影的详细信息。",
        "电影数据以字段标记、人类可读的方式格式化，带有清晰的字段标签。",
        "每个电影条目以'Movie Information'开头，后跟标记的字段。",
        "根据可用的电影信息提供全面的答案。",
    ],
)


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
def main() -> None:
    knowledge_base.insert(
        url="https://agno-public.s3.amazonaws.com/demo_data/IMDB-Movie-Data.csv",
        reader=reader,
    )
    agent.print_response(
        "哪些电影是由克里斯托弗·诺兰导演的",
        markdown=True,
        stream=True,
    )


if __name__ == "__main__":
    main()
