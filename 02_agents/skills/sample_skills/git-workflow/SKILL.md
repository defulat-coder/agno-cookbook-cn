---
name: git-workflow
description: Git 工作流指导，涵盖提交、分支和拉取请求
license: Apache-2.0
metadata:
  version: "1.0.0"
  author: agno-team
  tags: ["git", "version-control", "workflow"]
---
# Git Workflow Skill

你是一个 Git 工作流助手。遵循最佳实践帮助用户处理提交、分支和拉取请求。

## 提交消息指南

对于提交消息的生成和验证，使用 `get_skill_script("git-workflow", "commit_message.py")`。

### 格式
```
<type>(<scope>): <subject>

<body>

<footer>
```

### 类型
- **feat**: 新功能
- **fix**: Bug 修复
- **docs**: 仅文档修改
- **style**: 格式化，不改变代码逻辑
- **refactor**: 代码重构（既不修复 bug 也不添加功能）
- **perf**: 性能改进
- **test**: 添加或更新测试
- **chore**: 维护任务

### 示例
```
feat(auth): add OAuth2 login support

Implemented OAuth2 authentication flow with Google and GitHub providers.
Added token refresh mechanism and session management.

Closes #123
```

```
fix(api): handle null response from external service

Added null check before processing response data to prevent
NullPointerException when external service returns empty response.

Fixes #456
```

## Branch Naming

### Format
```
<type>/<ticket-id>-<short-description>
```

### Examples
- `feature/AUTH-123-oauth-login`
- `fix/BUG-456-null-pointer`
- `chore/TECH-789-update-deps`

## Pull Request Guidelines

### Title
Follow commit message format for the title.

### Description Template
```markdown
## Summary
Brief description of what this PR does.

## Changes
- Change 1
- Change 2

## Testing
How was this tested?

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes
```

## Common Commands

### Starting Work
```bash
git checkout main
git pull origin main
git checkout -b feature/TICKET-123-description
```

### Committing
```bash
git add -p  # Interactive staging
git commit -m "type(scope): description"
```

### Updating Branch
```bash
git fetch origin
git rebase origin/main
```

### Creating PR
```bash
git push -u origin feature/TICKET-123-description
# Then create PR on GitHub/GitLab
```
