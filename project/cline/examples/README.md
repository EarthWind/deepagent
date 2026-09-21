# Cline 实现实验

两条路径用途不同：`runtime-lab.mjs` 对固定上游源码做隔离验证，已实际通过；`sdk-agent.mjs` 演示公开包接口，本次只做语法与源码接口检查，未安装完整 SDK 运行。

## 已运行：13 组源码实验

要求 Node 24+、Git 和指定提交的干净源码。实验不安装 npm 依赖、不调用模型或网络。

```bash
git clone https://github.com/cline/cline.git /tmp/cline-research
git -C /tmp/cline-research checkout 4a56a43f39c2c75f941220989d4c65db006ee531
node project/cline/examples/runtime-lab.mjs /tmp/cline-research \
  project/cline/research/runtime-results.json
```

loader 使用 Node 的 `stripTypeScriptTypes`，因此可能打印 experimental warning。它检查 Git HEAD 和每个加载文件与提交中内容相同，再将类型擦除并重接 imports。没有改写 AgentRuntime、policy、command guard、editor 的可执行主体，也不把上游源码复制到本目录。

依赖替身明确如下：

| 边界 | 替换方式 | 未覆盖内容 |
| --- | --- | --- |
| 模型 | ScriptedModel 输出预置事件 | 真实网络、模型质量、供应商流编码 |
| 遥测 | no-op | 统计服务与遥测时序 |
| nanoid | randomUUID | ID 格式与碰撞性质 |
| JSON-like 嵌套字符串规范化 | identity，工具输入使用已解析的值 | jsonrepair 与嵌套 schema 兼容 |
| provider 错误分类 / gateway | 调用即报错；overflow 提供显式分类 | 自动错误分类、真实 gateway |
| 拒绝提示后缀 | 实验常量 | 提示词措辞对真实模型的影响 |

真实上游模块还包括 token 估算、metadata 合并、对象/字符串 helpers、VS Code tool policy、Plan guard，以及 editor 的换行辅助函数。文件实验只操作 `mkdtemp` 创建的目录，finally 清理该目录；命令过滤实验仅解析字符串，不执行 shell。

完整报告：[runtime-results.json](../research/runtime-results.json)。它记录测试组、示例事件轨迹、Node 版本、提交号与实际加载源码哈希。

## 公开包示例：最小 Agent 与纯函数工具

在独立临时项目安装示例依赖，避免改动本博客仓库的包配置。以下命令以仓库根目录为工作目录，第一次安装需要网络。

```bash
mkdir -p /tmp/cline-public-sdk-example
cp project/cline/examples/sdk-agent.mjs /tmp/cline-public-sdk-example/
npm install --prefix /tmp/cline-public-sdk-example --save-exact @cline/sdk@0.0.83
node /tmp/cline-public-sdk-example/sdk-agent.mjs
```

这里固定的版本号来自源码 package.json；本次未验证 npm registry 中该版本及其打包依赖的可安装性。如需完全使用本文提交，应遵循上游仓库的 Bun 构建流程构建 workspace 包，不应把源码版本号当成 npm 发布成功的证据。

公开示例只使用脚本化模型和字符计数工具，不需要 key。若换成真实 provider/model，网络、费用、授权、超时和错误分类就进入另一组验证范围。本文没有进行这些在线验证。
