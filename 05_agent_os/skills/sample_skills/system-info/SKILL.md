---
name: system-info
description: 使用可执行脚本获取系统信息
license: MIT
metadata:
  version: "1.0.0"
  author: agno
---
# System Info Skill

这个 Skill 提供脚本来收集系统信息。

## 可用脚本

- `get_system_info.py` - 返回基本系统信息（操作系统、Python 版本、当前时间）
- `list_directory.py` - 列出指定目录中的文件

## 使用方法

1. 使用 `run_skill_script("system-info", "get_system_info.py")` 获取系统信息
2. 使用 `run_skill_script("system-info", "list_directory.py", args=["path"])` 列出目录
