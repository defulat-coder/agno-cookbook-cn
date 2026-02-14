# 04_workflows/06_advanced_concepts/long_running

## 范围
cookbook/04_workflows/06_advanced_concepts/long_running 目录下的可运行 Workflow（工作流）示例

## 文件
- disruption_catchup.py: 演示中断恢复
- events_replay.py: 演示事件重放
- websocket_reconnect.py: 演示 WebSocket 重连

## 先决条件
- 激活演示环境：.venvs/demo/bin/python
- 使用 direnv allow 加载 API 密钥（需要本地 .envrc 文件）
- 某些示例需要本地 AgentOS 服务（参见文件头部的服务器 URL）
