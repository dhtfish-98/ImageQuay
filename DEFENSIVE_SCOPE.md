# ImageQuay 防御用途与当前复核范围

复核日期：2026-10-02；当前软件版本：1.0.2。

## 实际防御用途与能力

检查有权限分析的本地 Mach-O 结构、签名声明、ObjC/Swift 元数据。info/json/cs/list/symbols 读取和展示数据；insert/edit/lipo、头文件和 stub 生成保留合法本地编辑与组合能力。工具不执行输入程序，签名读取不证明信任链、签名有效性、身份或平台接受。

## 本轮实质改写

- `container_io.py` 全模块改写：最多 1 GiB 的普通文件或有限可寻址流私有快照；读取/写补丁前检查完整范围；FAT 表、切片、CPU、对齐与重叠检查；C 字符串只在有效范围终止；ULEB128 限定 64 位。`--mmap` 与旧参数保留，但使用快照后端。
- 头部增删替换统一通过原始命令块重建，保留未知命令尾部和 Unicode 字符串；CLI 检查新增头部不覆盖声明的文件内容。
- `signing_reader.py` 全模块改写：索引、重复 slot、长度、魔数与 blob 重叠都在声明的 SuperBlob 中检查。
- `file_ops.py` 新架构：CLI/GUI 读取拒绝最终路径符号链接与非普通文件。输出先写同目录 0600 临时文件，成功后原子发布；默认禁止覆盖，`--overwrite` 显式替换现有普通文件；二进制元数据生成的文件名不可带路径或控制字符。调用者选择的父目录仍由调用者管理。
- `update_reader.py` 新架构：默认无更新联网；`--check-updates` 或明确调用 API 才查询本仓库 GitHub 发布元数据，3 秒超时、1 MiB 响应限额、禁止重定向，不下载或安装软件。
- VM 页表改为按段记录的半开文件区间，避免恶意虚拟长度按页分配；零填充不映射为文件数据。记录缓存区分结构类型、字节序、物理位置与补丁代数。
- export trie 解码改写：声明区域、路径环、终端长度与 1,048,576 次节点预算、4096 级路径深度与 64 MiB 总名称预算；修复继承算法丢失 export 地址低 7 位的问题，处理 reexport/resolver 元数据。Binding/function-start 输入使用独立字节区域与有限工作预算；Binding 字符串按 UTF-8 字节移动、SLEB 按有符号数读取。

## 当前验证与明确剩余工作

159 项测试通过；822 个历史对照观察中 818 个保持一致，4 个完整 image 输出仅有已列明的 export 地址修复。4 个 fixture 的当前 export 地址另外与 Apple nm 对照；独立安装验证覆盖包身份和新的输入、export、私有输出行为；另有 6 个安装后 CLI 编辑/组合/提取/覆盖流程，输入字节保持不变。

本轮完成的是上述共享边界与指定算法重写。**不是全部上游算法已经重写**。ObjC/Swift 解释器、chained-fixup 的完整解释算法、SymbolTable/其余 loader 行为、GUI 布局与交互、header/TBD 生成器、plist/record 支持内核仍需要完整重写与扩展验证。Binding 的完整语义（包括 threaded apply）仍 OPEN。真实设备/固件集合、全部畸形格式与 GUI 手工交互仍 OPEN。

## 来源与 CVP

来源、固定上游提交与 MIT 许可见 [ORIGIN.md](ORIGIN.md)。保留原作者与许可证，使用 Codex 辅助维护；不把上游算法写成申请人独立原创。历史发布保留，并与当前改写发布分开标明。

[Anthropic CVP 官方说明](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)依据实际受到防护影响的合法防御双用途任务。项目数量、源码改名、构建和 CI 不能证明申请资格。真实授权、身份、组织、受限任务与审批结果仍需本人真实证据；不保证某一模型永不触发网络安全防护。
