"""
使用 AgentOSClient 上传内容到知识库

此示例演示如何使用 AgentOSClient 将文档和内容上传到知识库。

前置条件：
1. 启动配置了知识库的 AgentOS 服务器
2. 运行此脚本：python 09_upload_content.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def upload_text_content():
    """将文本内容上传到知识库。"""
    print("=" * 60)
    print("Uploading Text Content")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 要上传的文本内容
    content = """
    # Agno Framework Guide
    
    Agno is a powerful framework for building AI agents and teams.
    
    ## Key Features
    - Agent creation with custom tools
    - Team coordination for complex tasks
    - Workflow automation
    - Knowledge base integration
    - Memory management
    
    ## Getting Started
    1. Install agno: uv pip install agno
    2. Create an agent with a model
    3. Add tools for specific capabilities
    4. Deploy with AgentOS
    """

    try:
        print("Uploading text content...")

        # 使用 text_content 参数上传内容
        result = await client.upload_knowledge_content(
            text_content=content,
            name="Agno Guide",
            description="A guide to the Agno framework",
        )

        print("\nUpload successful!")
        print(f"Content ID: {result.id}")
        print(f"Status: {result.status}")

        # 检查状态
        if result.id:
            print("\nChecking processing status...")
            status = await client.get_content_status(result.id)
            print(f"Status: {status.status}")
            print(f"Message: {status.status_message}")

    except Exception as e:
        print(f"Error uploading: {e}")
        if hasattr(e, "response"):
            print(f"Response: {e.response.text}")


async def list_uploaded_content():
    """列出所有上传的内容。"""
    print("\n" + "=" * 60)
    print("Listing Uploaded Content")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    try:
        content = await client.list_knowledge_content()
        print(f"\nFound {len(content.data)} content items")

        for item in content.data:
            print(f"\n- ID: {item.id}")
            print(f"  Name: {item.name}")
            print(f"  Status: {item.status}")
            print(f"  Type: {item.type}")

    except Exception as e:
        print(f"Error listing content: {e}")


async def search_uploaded_content():
    """上传后搜索知识库。"""
    print("\n" + "=" * 60)
    print("Searching Knowledge Base")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    try:
        # 搜索内容
        results = await client.search_knowledge(
            query="What is Agno?",
            limit=5,
        )

        print(f"\nFound {len(results.data)} results")

        for result in results.data:
            content_preview = (
                str(result.content)[:150] if hasattr(result, "content") else "N/A"
            )
            print(f"\n- Content: {content_preview}...")

    except Exception as e:
        print(f"Error searching: {e}")


async def delete_content():
    """删除上传的内容。"""
    print("\n" + "=" * 60)
    print("Deleting Content")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    try:
        # 首先列出内容
        content = await client.list_content()
        if not content.data:
            print("No content to delete")
            return

        # 删除第一项（用于演示目的）
        content_id = content.data[0].id
        print(f"Deleting content: {content_id}")

        await client.delete_content(content_id)
        print("Content deleted successfully")

        # 验证删除
        content_after = await client.list_content()
        print(f"Remaining content items: {len(content_after.data)}")

    except Exception as e:
        print(f"Error deleting content: {e}")
        if hasattr(e, "response"):
            print(f"Response: {e.response.text}")


async def main():
    await upload_text_content()
    await list_uploaded_content()
    await search_uploaded_content()
    # 取消注释以测试删除：
    # await delete_content()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
