---
name: TypeScript project conventions
globs: "**/*.ts"
alwaysApply: false
---

修改 TypeScript 文件前，先阅读目标代码与相关测试，确认现有命名、错误处理与模块边界。

尽量保持变更聚焦。新增或改变业务行为时，运行能覆盖该行为的相关测试，并在最终说明中记录实际执行的命令与结果。

如果未运行测试，明确说明未验证的部分，不要将预期结果描述成已执行事实。
