"""使用 MongoDb 作为 Agent 的数据库。

运行 `uv pip install openai pymongo` 安装依赖

使用以下命令运行本地 MongoDB 服务器：
```bash
docker run -d \
  --name local-mongo \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=mongoadmin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo
```
或使用我们的脚本：
```bash
./scripts/run_mongodb.sh
```
"""

from agno.agent import Agent
from agno.db.mongo import MongoDb
from agno.tools.websearch import WebSearchTools

# ---------------------------------------------------------------------------
# 设置
# ---------------------------------------------------------------------------
db_url = "mongodb://mongoadmin:secret@localhost:27017"
db = MongoDb(db_url=db_url)

# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent(
    db=db,
    tools=[WebSearchTools()],
    add_history_to_context=True,
)

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("How many people live in Canada?")
    agent.print_response("What is their national anthem called?")
