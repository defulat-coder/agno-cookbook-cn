# Commit 类型参考

## 主要类型

| 类型 | 描述 | 示例 |
|------|-------------|---------|
| `feat` | 用户新功能 | `feat(cart): add checkout button` |
| `fix` | 用户 bug 修复 | `fix(login): correct password validation` |
| `docs` | 仅文档修改 | `docs(readme): update installation steps` |
| `style` | 格式化、缺少分号等 | `style(api): format with prettier` |
| `refactor` | 既不修复 bug 也不添加功能的代码修改 | `refactor(auth): simplify token logic` |
| `perf` | 性能改进 | `perf(query): add database index` |
| `test` | 添加或更新测试 | `test(api): add user endpoint tests` |
| `chore` | 维护任务 | `chore(deps): update lodash to 4.17.21` |

## Additional Types (Optional)

| Type | Description | Example |
|------|-------------|---------|
| `build` | Build system or external dependencies | `build(docker): optimize image size` |
| `ci` | CI/CD configuration | `ci(github): add lint workflow` |
| `revert` | Reverting a previous commit | `revert: feat(cart): add checkout button` |

## Scope Examples

Scopes should be short and identify the area of the codebase:

- `auth` - Authentication module
- `api` - API endpoints
- `ui` - User interface
- `db` - Database
- `config` - Configuration
- `deps` - Dependencies
- `core` - Core functionality

## Breaking Changes

Use `!` after type/scope for breaking changes:

```
feat(api)!: change response format

BREAKING CHANGE: Response now uses camelCase instead of snake_case.
Migration guide available in docs/migration-v2.md
```

## Multi-line Commits

For complex changes, use a body:

```
feat(search): implement fuzzy matching

Added fuzzy matching algorithm to improve search results.
Users can now find items even with typos or partial matches.

- Implemented Levenshtein distance calculation
- Added configurable threshold for match sensitivity
- Updated search index to support fuzzy queries

Closes #789
```
