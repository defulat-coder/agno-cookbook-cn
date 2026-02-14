"""
使用 AgentOSClient 运行评估

此示例演示如何使用 AgentOSClient 运行和管理评估。

前置条件：
1. 启动带有 agent 的 AgentOS 服务器
2. 运行此脚本：python 08_run_evals.py
"""

import asyncio

from agno.client import AgentOSClient
from agno.db.schemas.evals import EvalType

# ---------------------------------------------------------------------------
# 创建示例
# ---------------------------------------------------------------------------


async def run_accuracy_eval():
    """运行准确性评估。"""
    print("=" * 60)
    print("Running Accuracy Evaluation")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的 agent
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    print(f"Evaluating agent: {agent_id}")

    # 运行准确性评估
    try:
        eval_result = await client.run_eval(
            agent_id=agent_id,
            eval_type=EvalType.ACCURACY,
            input_text="What is 2 + 2?",
            expected_output="4",
        )

        if eval_result:
            print(f"\nEval ID: {eval_result.id}")
            print(f"Eval Type: {eval_result.eval_type}")
            print(f"Eval Data: {eval_result.eval_data}")
        else:
            print("Evaluation returned no result")

    except Exception as e:
        print(f"Error running eval: {e}")
        if hasattr(e, "response"):
            print(f"Response: {e.response.text}")


async def run_performance_eval():
    """运行性能评估。"""
    print("\n" + "=" * 60)
    print("Running Performance Evaluation")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    # 获取可用的 agent
    config = await client.aget_config()
    if not config.agents:
        print("No agents available")
        return

    agent_id = config.agents[0].id
    print(f"Evaluating agent: {agent_id}")

    # 运行性能评估
    try:
        eval_result = await client.run_eval(
            agent_id=agent_id,
            eval_type=EvalType.PERFORMANCE,
            input_text="Hello, how are you?",
            num_iterations=2,  # 运行两次以测量性能
        )

        if eval_result:
            print(f"\nEval ID: {eval_result.id}")
            print(f"Eval Type: {eval_result.eval_type}")
            print(f"Performance Data: {eval_result.eval_data}")
        else:
            print("Evaluation returned no result")

    except Exception as e:
        print(f"Error running eval: {e}")
        if hasattr(e, "response"):
            print(f"Response: {e.response.text}")


async def list_eval_runs():
    """列出所有评估运行。"""
    print("\n" + "=" * 60)
    print("Listing Evaluation Runs")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    try:
        evals = await client.list_eval_runs()
        print(f"\nFound {len(evals.data)} evaluation runs")

        for eval_run in evals.data[:5]:  # 显示前 5 个
            print(f"\n- ID: {eval_run.id}")
            print(f"  Name: {eval_run.name}")
            print(f"  Type: {eval_run.eval_type}")
            print(f"  Agent: {eval_run.agent_id}")

    except Exception as e:
        print(f"Error listing evals: {e}")


async def get_eval_details():
    """获取特定评估的详细信息。"""
    print("\n" + "=" * 60)
    print("Getting Evaluation Details")
    print("=" * 60)

    client = AgentOSClient(base_url="http://localhost:7777")

    try:
        # 首先列出评估以获取 ID
        evals = await client.list_eval_runs()
        if not evals.data:
            print("No evaluations found")
            return

        eval_id = evals.data[0].id
        print(f"Getting details for eval: {eval_id}")

        eval_run = await client.get_eval_run(eval_id)
        print(f"\nEval ID: {eval_run.id}")
        print(f"Name: {eval_run.name}")
        print(f"Type: {eval_run.eval_type}")
        print(f"Agent ID: {eval_run.agent_id}")
        print(f"Data: {eval_run.eval_data}")

    except Exception as e:
        print(f"Error getting eval: {e}")


async def main():
    await run_accuracy_eval()
    await run_performance_eval()
    await list_eval_runs()
    await get_eval_details()


# ---------------------------------------------------------------------------
# 运行示例
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
