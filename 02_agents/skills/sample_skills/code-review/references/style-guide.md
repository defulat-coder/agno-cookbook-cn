# Python 风格指南

## 命名约定

### 变量和函数
- 变量和函数使用 `snake_case`
- 使用描述性名称来解释用途
- 除了循环计数器外避免使用单字母名称

```python
# 好
user_count = 10
def calculate_total_price(items):
    pass

# 不好
uc = 10
def calc(i):
    pass
```

### 类
- 类名使用 `PascalCase`
- 使用名词来描述类所代表的内容

```python
# 好
class UserAccount:
    pass

class OrderProcessor:
    pass

# 不好
class user_account:
    pass

class Process:
    pass
```

### 常量
- 常量使用 `UPPER_SNAKE_CASE`
- 在模块级别定义

```python
# 好
MAX_RETRY_COUNT = 3
DEFAULT_TIMEOUT = 30

# 不好
maxRetryCount = 3
default_timeout = 30
```

## 代码组织

### 导入
- 按以下顺序分组导入：标准库、第三方库、本地库
- 在每组内按字母顺序排序
- 使用绝对导入

```python
# 标准库
import os
import sys
from typing import List, Optional

# 第三方库
import requests
from pydantic import BaseModel

# 本地库
from myapp.models import User
from myapp.utils import helper
```

### 函数长度
- 函数保持在 50 行以下
- 如果更长，考虑拆分成更小的函数
- 每个函数应该做好一件事

### 文档
- 为公共函数和类使用 docstring
- 遵循 Google 或 NumPy docstring 风格
- 包含参数类型和返回类型

```python
def process_user_data(user_id: str, include_history: bool = False) -> dict:
    """处理用户数据并返回格式化的结果。

    Args:
        user_id: 用户的唯一标识符。
        include_history: 是否包含用户历史。默认为 False。

    Returns:
        包含处理后用户数据的字典。

    Raises:
        ValueError: 如果 user_id 为空或无效。
    """
    pass
```

## 错误处理

### 要具体
- 捕获特定的异常，而不是裸的 `except:`
- 包含有帮助的错误消息

```python
# 好
try:
    result = process_data(data)
except ValueError as e:
    logger.error(f"无效的数据格式: {e}")
    raise
except ConnectionError as e:
    logger.error(f"连接失败: {e}")
    return None

# 不好
try:
    result = process_data(data)
except:
    pass
```

## 安全性

### 永远不要硬编码秘密
- 使用环境变量或秘密管理器
- 永远不要将凭证提交到版本控制

```python
# 好
import os
api_key = os.environ.get("API_KEY")

# 不好
api_key = "sk-1234567890abcdef"
```
