"""
GitHub 内容源知识库
===================

从 GitHub 仓库加载文件和文件夹到您的知识库。
支持使用细粒度个人访问令牌的公共和私有仓库。

特性：
- 递归加载单个文件或整个文件夹
- 适用于公共仓库（无需令牌）或私有仓库（需要令牌）
- 自动文件类型检测和读取器选择
- 为每个文件存储丰富的元数据（仓库、分支、路径）

需求：
- 对于私有仓库：需要具有"Contents: read"权限的 GitHub 细粒度 PAT

用法：
    1. 使用仓库和可选令牌配置 GitHubConfig
    2. 通过 content_sources 在 Knowledge 上注册配置
    3. 使用 .file() 或 .folder() 创建内容引用
    4. 使用 knowledge.insert() 插入到知识库

运行此示例：
    python cookbook/07_knowledge/cloud/github.py
"""

from os import getenv

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.remote_content import GitHubConfig
from agno.vectordb.pgvector import PgVector

# 配置 GitHub 内容源
# 对于私有仓库，将 GITHUB_TOKEN 环境变量设置为具有"Contents: read"权限的细粒度 PAT
github_config = GitHubConfig(
    id="my-repo",
    name="My Repository",
    repo="private/repo",  # 格式：owner/repo
    token=getenv("GITHUB_TOKEN"),  # 公共仓库可选
    branch="main",  # 默认分支
)

# 创建以 GitHub 作为内容源的 Knowledge
knowledge = Knowledge(
    name="GitHub Knowledge",
    vector_db=PgVector(
        table_name="github_knowledge",
        db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
    ),
    content_sources=[github_config],
)

if __name__ == "__main__":
    # 插入单个文件
    print("从 GitHub 插入单个文件...")
    knowledge.insert(
        name="README",
        remote_content=github_config.file("README.md"),
    )

    # 插入整个文件夹（递归）
    # 使用尾部斜杠或只是文件夹名称 - 两者都有效
    print("从 GitHub 插入文件夹...")
    knowledge.insert(
        name="Cookbook Examples",
        remote_content=github_config.folder("cookbook/01_basics"),
    )

    # 从不同分支插入
    print("从特定分支插入...")
    knowledge.insert(
        name="Dev Docs",
        remote_content=github_config.file("docs/index.md", branch="dev"),
    )
