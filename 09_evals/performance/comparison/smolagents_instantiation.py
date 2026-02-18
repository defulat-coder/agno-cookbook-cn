"""
Smolagents 实例化性能评估
===============================================

演示使用 Smolagents 进行 Agent 实例化基准测试。
"""

from agno.eval.performance import PerformanceEval
from smolagents import InferenceClientModel, Tool, ToolCallingAgent


# ---------------------------------------------------------------------------
# 创建基准测试工具
# ---------------------------------------------------------------------------
class WeatherTool(Tool):
    name = "weather_tool"
    description = """
    This is a tool that tells the weather"""
    inputs = {
        "city": {
            "type": "string",
            "description": "The city to look up",
        }
    }
    output_type = "string"

    def forward(self, city: str):
        """使用此工具获取天气信息。"""
        if city == "nyc":
            return "It might be cloudy in nyc"
        elif city == "sf":
            return "It's always sunny in sf"
        else:
            raise AssertionError("Unknown city")


# ---------------------------------------------------------------------------
# 创建基准测试函数
# ---------------------------------------------------------------------------
def instantiate_agent():
    return ToolCallingAgent(
        tools=[WeatherTool()],
        model=InferenceClientModel(model_id="meta-llama/Llama-3.3-70B-Instruct"),
    )


# ---------------------------------------------------------------------------
# 创建评估
# ---------------------------------------------------------------------------
smolagents_instantiation = PerformanceEval(func=instantiate_agent, num_iterations=1000)

# ---------------------------------------------------------------------------
# 运行评估
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    smolagents_instantiation.run(print_results=True, print_summary=True)
