"""
使用 AgentOSClient 运行工作流

此示例演示如何使用 AgentOSClient 执行工作流运行，
包括流式和非流式响应。

前置条件：
1. 启动一个配置了工作流的 AgentOS 服务器
2. 运行此脚本：python 07_run_workflows.py
"""

import asyncio

from agno.client import AgentOSClient

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def run_workflow_non_streaming():
    """执行非流式工作流运行。"""
    print("=" * 60)
    print("Non-Streaming Workflow Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的工作流
    config = await client.aget_config()
    if not config.workflows:
        print("No workflows available")
        return

    workflow_id = config.workflows[0].id
    print(f"Running workflow: {workflow_id}")

    try:
        # 执行工作流
        result = await client.run_workflow(
            workflow_id=workflow_id,
            message="What are the benefits of using Python for data science?",
        )

        print(f"\nRun ID: {result.run_id}")
        print(f"Content: {result.content}")
    except Exception as e:
        print(f"Error: {e}")
        if hasattr(e, "response"):
            print(f"Response: {e.response.text}")


async def run_workflow_streaming():
    """执行流式工作流运行。"""
    print("\n" + "=" * 60)
    print("Streaming Workflow Run")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的工作流
    config = await client.aget_config()
    if not config.workflows:
        print("No workflows available")
        return

    workflow_id = config.workflows[0].id
    print(f"Streaming from workflow: {workflow_id}")
    print("\nResponse: ", end="", flush=True)

    try:
        # 流式响应 - 返回类型化的 WorkflowRunOutputEvent 对象
        # 工作流可以发出工作流事件和嵌套的 agent 事件
        async for event in client.run_workflow_stream(
            workflow_id=workflow_id,
            message="Explain machine learning in simple terms.",
        ):
            # 处理来自 agent 事件（RunContent）或工作流完成的内容
            if event.event == "RunContent" and hasattr(event, "content"):
                print(event.content, end="", flush=True)
            elif (
                event.event == "WorkflowAgentCompleted"
                and hasattr(event, "content")
                and event.content
            ):
                print(event.content, end="", flush=True)

        print("\n")
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")


async def main():
    await run_workflow_non_streaming()
    await run_workflow_streaming()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
