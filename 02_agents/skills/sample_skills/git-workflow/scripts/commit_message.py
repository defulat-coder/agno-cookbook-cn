# ---------------------------------------------------------------------------
# 创建 Agent
# ---------------------------------------------------------------------------
#!/usr/bin/env python3
"""
提交消息
=============================

验证或生成约定式提交消息。
"""

import json
import sys

COMMIT_TYPES = {
    "feat": "新功能",
    "fix": "Bug 修复",
    "docs": "文档修改",
    "style": "格式化，不改变代码逻辑",
    "refactor": "代码重构",
    "perf": "性能改进",
    "test": "添加/更新测试",
    "chore": "维护任务",
    "build": "构建系统修改",
    "ci": "CI/CD 修改",
}


def validate(message: str) -> dict:
    """验证提交消息。"""
    errors = []
    warnings = []

    lines = message.strip().split("\n")
    if not lines or not lines[0]:
        return {"valid": False, "errors": ["Empty commit message"]}

    subject = lines[0]

    # 检查格式：type: description
    if ":" not in subject:
        errors.append("Missing ':' separator (expected 'type: description')")
    else:
        type_part, desc = subject.split(":", 1)
        type_part = type_part.strip().rstrip("!").split("(")[0]
        desc = desc.strip()

        if type_part not in COMMIT_TYPES:
            errors.append(
                f"Unknown type '{type_part}'. Valid: {', '.join(COMMIT_TYPES.keys())}"
            )

        if not desc:
            errors.append("Description required after ':'")

        if len(subject) > 72:
            warnings.append(f"Subject is {len(subject)} chars (recommended: ≤72)")

    return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}


def generate(commit_type: str, description: str, scope: str = None) -> dict:
    """生成提交消息。"""
    if commit_type not in COMMIT_TYPES:
        return {
            "error": f"Unknown type '{commit_type}'. Valid: {', '.join(COMMIT_TYPES.keys())}"
        }

    if scope:
        message = f"{commit_type}({scope}): {description}"
    else:
        message = f"{commit_type}: {description}"

    return {"message": message, "type": commit_type, "description": description}


def list_types() -> dict:
    """列出所有有效的提交类型。"""
    return {"types": COMMIT_TYPES}


# ---------------------------------------------------------------------------
# 运行 Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(
                json.dumps(
                    {
                        "error": "Usage: commit_message.py <validate|generate|types> [args]"
                    }
                )
            )
            sys.exit(1)

        command = sys.argv[1]

        if command == "validate":
            msg = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
            result = validate(msg)
        elif command == "generate":
            if len(sys.argv) < 4:
                result = {
                    "error": "Usage: commit_message.py generate <type> <description> [scope]"
                }
            else:
                commit_type = sys.argv[2]
                description = sys.argv[3]
                scope = sys.argv[4] if len(sys.argv) > 4 else None
                result = generate(commit_type, description, scope)
        elif command == "types":
            result = list_types()
        else:
            result = {
                "error": f"Unknown command '{command}'. Use: validate, generate, types"
            }

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
