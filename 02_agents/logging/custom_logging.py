"""
自定义日志
=============================

展示如何在 Agno 中使用自定义 logger 的示例。
"""

import logging

from agno.agent import Agent
from agno.utils.log import configure_agno_logging, log_info


def get_custom_logger():
    """返回一个示例自定义 logger。"""
    custom_logger = logging.getLogger("custom_logger")
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[CUSTOM_LOGGER] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    custom_logger.addHandler(handler)
    custom_logger.setLevel(logging.INFO)  # 将级别设置为 INFO 以显示信息消息
    custom_logger.propagate = False
    return custom_logger


# 获取我们将用于示例的自定义 logger。
custom_logger = get_custom_logger()

# 配置 Agno 使用我们的自定义 logger。它将用于所有日志记录。
configure_agno_logging(custom_default_logger=custom_logger)

# 现在 agno.utils.log 中的日志函数的每次使用都将使用我们的自定义 logger。
log_info("This is using our custom logger!")

# 现在让我们设置一个 Agent 并运行它。
# 来自 Agent 的所有日志记录都将使用我们的自定义 logger。
# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
agent = Agent()

# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    agent.print_response("What can I do to improve my sleep?")
