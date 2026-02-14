"""
数据库
==

演示数据库。
"""

from agno.db.surrealdb import SurrealDb

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------

# ************* SurrealDB 配置 *************
SURREALDB_URL = "ws://localhost:8000"
SURREALDB_USER = "root"
SURREALDB_PASSWORD = "root"
SURREALDB_NAMESPACE = "agno"
SURREALDB_DATABASE = "agent_os_demo"
# *******************************

# ************* 创建 SurrealDB 实例 *************
creds = {"username": SURREALDB_USER, "password": SURREALDB_PASSWORD}
db = SurrealDb(None, SURREALDB_URL, creds, SURREALDB_NAMESPACE, SURREALDB_DATABASE)
# *******************************

# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    raise SystemExit("此模块旨在被导入。")
