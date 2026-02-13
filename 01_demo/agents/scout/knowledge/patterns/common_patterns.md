# 常见搜索模式

## 查找政策和手册

**最佳做法：**
1. 从 S3 `company-docs/policies/` 开始
2. 搜索政策名称或相关术语
3. 阅读完整文档，而不仅仅是片段

**已知位置：**
- 员工手册：`s3://company-docs/policies/employee-handbook.md`
- 带薪休假政策：在员工手册第 4 节
- 数据保留：`s3://company-docs/policies/data-retention.md`
- 安全政策：`s3://company-docs/policies/security-policy.md`

**注意：** 带薪休假信息在员工手册中，不是独立文档。

---

## 查找运行手册和流程

**最佳做法：**
1. 从 S3 `engineering-docs/runbooks/` 开始
2. 搜索流程名称
3. 阅读完整运行手册

**已知位置：**
- 部署：`s3://engineering-docs/runbooks/deployment.md`
- 事件响应：`s3://engineering-docs/runbooks/incident-response.md`
- 值班指南：`s3://engineering-docs/runbooks/oncall-guide.md`

---

## 查找 OKR 和规划文档

**最佳做法：**
1. 从 S3 `company-docs/planning/` 开始
2. 搜索季度（Q1、Q2、Q3、Q4）和年份
3. 阅读完整 OKR 文档

**已知位置：**
- 2024 Q4 OKR：`s3://company-docs/planning/q4-2024-okrs.md`
- 公司战略：`s3://company-docs/planning/2024-strategy.md`

---

## 查找技术文档

**最佳做法：**
1. 从 S3 `engineering-docs/architecture/` 开始
2. RFC 请查看 `engineering-docs/rfcs/`
3. 维基类内容可回退到 Notion

**已知位置：**
- 系统概览：`s3://engineering-docs/architecture/system-overview.md`
- API 设计：`s3://engineering-docs/architecture/api-design.md`
- RFC：`s3://engineering-docs/rfcs/`

---

## 查找近期决策

**最佳做法：**
1. 从 Slack 开始 —— 搜索相关频道
2. 查找回复较多的主题
3. 与已记录的决策交叉对照

**常见位置：**
- Slack：#product-decisions、#engineering、#leadership
- Notion：决策日志或会议笔记

---

## 查找谁了解某件事

**最佳做法：**
1. 从 Slack 开始 —— 查找近期讨论
2. 记录积极参与的人
3. 在 Notion 中查看页面负责人

---

## 多源搜索策略

当信息可能存在于任何地方时：

1. **识别信息类型**
   - 政策/正式文档 → S3
   - 讨论/决策 → Slack
   - 活文档/维基 → Notion
   - 电子表格 → Google Drive

2. **优先搜索主要来源**

3. **注意时间戳** —— 较新的信息可能取代较旧的

4. **交叉对照** —— 重要决策往往存在于多个地方

5. **保存所学** —— 如果位置出乎意料，请保存下来

---

## 处理「未找到」结果

如果搜索无结果：

1. **尝试同义词** —— 「PTO」vs「vacation」vs「time off」
2. **扩大搜索范围** —— 去掉具体术语
3. **检查其他来源** —— 信息可能在其他系统中
4. **检查父文档** —— 信息可能在更大文档的某一节中
5. **请求澄清** —— 用户可能知道确切位置
