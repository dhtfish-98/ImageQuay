# ImageQuay 防御用途与本轮复核范围

复核日期：2026-10-02。

## 实际防御用途

对有权限检查的本地 Mach-O、签名与 ObjC/Swift 元数据做静态安全复核。

## 实际能力

info/json/cs/list/symbols 等入口读取和展示数据。insert/edit/lipo 以及报告生成会写文件，库也有修改 API。CLI 继承了 PyPI 更新检查；KTOOL_NO_UPDATE_CHECK 可关闭该检查。

## 当前检查

本轮核对 CLI 子命令、修改/组合写出、更新检查和签名读取路径；保留来源与 MIT 许可。历史 34 项测试及 822 项观察的覆盖范围见 VALIDATION.md。

## 验证边界

安全评估报告应写明实际使用的子命令；编辑后的签名或程序运行效果没有在本轮验证。所有畸形文件和 GUI 交互未证明。

## 来源与 CVP

本项目的上游、固定提交和许可见 [ORIGIN.md](ORIGIN.md)。保留原作者与许可证；历史名称/模块重构和本轮 Codex 辅助维护均不代表申请人独立编写了上游算法。最新源码、历史包和实际运行结果须按各自提交分别核对。

[Anthropic 当前 CVP 说明](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)以受到网络安全防护影响的合法防御双用途任务为依据。项目数量、改名、构建和 CI 不证明申请资格；实际授权、身份、组织和受限任务仍需真实证据。这里没有本轮申请结果，也不保证某个模型永不触发网络安全防护。
