# Async MongoDB Integration（异步 MongoDB 集成）

演示异步 MongoDB 与 Agno agents、teams 和 workflows 集成的示例。

## Setup（设置）

```shell
uv pip install pymongo motor
```

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

## Examples（示例）

- [`async_mongodb_for_agent.py`](async_mongodb_for_agent.py) - 使用 AsyncMongoDb storage 的 Agent
- [`async_mongodb_for_team.py`](async_mongodb_for_team.py) - 使用 AsyncMongoDb storage 的 Team
- [`async_mongodb_for_workflow.py`](async_mongodb_for_workflow.py) - 使用 AsyncMongoDb storage 的 Workflow
