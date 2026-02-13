# hooks（钩子）

hooks 中团队工作流的示例。

## 前置条件

- 通过 direnv allow 加载环境变量（例如 OPENAI_API_KEY）。
- 使用 .venvs/demo/bin/python 运行手册示例。
- 某些示例需要额外的服务（例如 PostgreSQL、LanceDB 或 Infinity 服务器），如文件文档字符串中所述。

## 文件说明

- post_hook_output.py - 演示后置钩子输出。
- pre_hook_input.py - 演示前置钩子输入。
- stream_hook.py - 演示流钩子。
