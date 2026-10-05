# ImageQuay 防御用途与当前复核范围

复核日期：2026-10-04；当前软件版本：1.0.6。

## 实际防御用途与能力

检查有权限分析的本地 Mach-O 结构、签名声明、ObjC/Swift 元数据。info/json/cs/list/symbols 读取和展示数据；insert/edit/lipo、头文件和 stub 生成保留合法本地编辑与组合能力。工具不执行输入程序。签名读取不证明信任链、签名有效性、身份或平台接受。

## 已发布的实质改写

- `container_io.py` 全模块改写：最多 1 GiB 的普通文件或有限可寻址流私有快照；读取/写补丁前检查完整范围；FAT 表、切片、CPU、对齐与重叠检查；有限字符串与 64 位 LEB。`--mmap` 保留，使用快照后端。头部增删替换统一重建原始命令块，保留未知尾部和 Unicode；CLI 不让头部增长覆盖声明的文件内容。
- `signing_reader.py` 全模块改写：SuperBlob 中检查索引、重复 slot、长度、魔数与 blob 重叠。
- `file_ops.py` 新架构：输入拒绝最终路径符号链接与非普通文件；输出先写同目录 0600 临时文件，成功后原子发布，失败清理描述符与临时文件。默认禁止覆盖，`--overwrite` 显式替换现有普通文件。元数据生成的文件名不可带路径或控制字符。调用者选择的父目录由调用者管理。
- `update_reader.py` 新架构：默认不联网；`--check-updates` 或明确调用 API 才查询本仓库发布元数据；3 秒 socket I/O 超时（不是整体硬性期限）、1 MiB 响应限额、禁止重定向，不下载或安装软件。
- VM 改为按段记录的半开文件区间，避免按恶意虚拟长度逐页分配；零填充不映射成文件数据。记录缓存区分结构类型、字节序、物理位置与补丁代数。
- export trie 改写：声明区域、路径环、终端长度、1,048,576 次节点工作预算、4096 级路径深度与 64 MiB 总名称预算；修复 export 地址丢失低 7 位，处理 reexport/resolver 声明。
- `record_engine.py` 全模块改写：独立布局计划，短记录拒绝，嵌套继承字节序和指针宽度；有符号数对称读写；每实例独立位字段状态与无损 union 存储；按完整字节宽度验证值；缺少指针宽度抛错，不退出调用进程。单记录最多 1 MiB、4096 字段、64 级嵌套。
- `plist_codec.py` 全模块改写：自有 XML 状态机和 binary 对象区域/引用图解码；拒绝实体与外部引用、重复键、环、表外引用、短数据和区域重叠。保留 Data、UID、空整数与十六进制整数扩展、路径和流读写 API。写出使用维护中的 Python 标准库并先检查对象图；最多 16 MiB、100000 对象/引用、128 级深度。
- `binding_reader.py` 新架构：普通、弱和延迟绑定模式，完整普通 opcode、显式状态、带符号特殊库 ordinal、64 位地址、SLEB addend、UTF-8 游标与有界 threaded apply。DONE 不产生多余绑定；旧 ARM64_32 的 uint64 游标后退编码在实际绑定位置仍检查文件范围。
- `chained_reader.py` 新架构：独立限制 linkedit 表、页和文件段；三种 import 格式与 pointer formats 1–14；有界多起点链、重复地址与表重叠检查；最多 128 MiB 元数据、1,048,576 工作单位、64 MiB 名称。外部 cache 的基址未提供时保留 `unresolved_rebases`；可显式传 `cache_bases`，不猜地址。压缩 symbol format 1 尚未实现，明确抛错。
- loader 先登记段和链接库，再解析依赖它们的元数据，不依赖命令顺序。SymbolTable 的记录与字符串分别受声明区域限制；function starts 遇零终止，检查后续填充和数值宽度。线程状态长度/预算受命令限制；完整 CPU flavor 到 PC 的解释仍继承旧选择方式。

- `objc_encoding.py` 全语法核心改写：最多 16384 字符、4096 节点、64 层类型；保留完整数组、指针、限定、具名成员、结构/union、位字段、对象/block、方法偏移、complex/atomic 类型。有限独立缓存与结构注册表，不把输入当表达式执行。未知类型明确抛错。
- `metadata_graph.py` 新架构：元数据读取限制在单一文件段、快照代数、指针宽度和工作/名称预算内。chained pointer 用解析视图解读，不改原始字节；未知外部缓存基址明确失败。Swift symbolic reference 仅保留原始字节/显示标记，不跟随任意指针或调用 accessor。
- `objc_model.py` 全模块算法改写：类/元类/继承、分类、协议继承及可选/类属性、方法、ivar 与属性读取均检查完整记录/列表范围；relative method 各字段用自己的带符号位移，协议 count 与指针同宽，ivar offset 读取实际 4 字节单元。局部损坏显式提供 `complete/errors/load_errors`；序列化局部结果包含 `metadata-status`。工作预算耗尽和输入变化不能忽略。
- `swift_model.py` 全模块算法改写：静态 class/struct/enum 声明头、字段描述与相对 type section，负位移/间接引用/父作用域均有范围、版本、环和数量检查。44 字节 class header 补全字段向量偏移。未知类型记录显式标为 unsupported；尾随泛型/resilient/runtime 数据仍不重建。Swift 名称解码改为有限且精确的简单名义文法，复杂名称不猜测。

## 当前验证与明确剩余工作

本地 Python 3.12/macOS 全套 386 项测试通过。1.0.5 只修正 ARM64_32 参考工具空 ObjC 输出的精确格式断言；解析代码未改。822 个历史观察中 416 原样；402 个旧位字段写出异常修复为正常结果，以独立位掩码、原始字节往返和完整输出断言验证；4 个 image 仅允许已列明的 export 地址与函数零终止修复，无无法解释差异。

4 个 fixture 的 export 地址与 Apple nm 对照。Apple dyld_info 另外核对全部 6 个切片的绑定位置、chained rebase 地址/目标和 function starts。5 个切片的绑定名直接匹配工具；ARM64_32 的连续复用目标在新版工具中会显示为下一符号，改用独立解释器解码工具打印的绑定指令，并核对 otool 段地址及 SHA 绑定向量；只允许已确认的两个名称位点差异，全部位置仍必须匹配。另以自有 Clang/Swift 样本分别验证 12 个 @encode 向量、3 个名义类型与字段/作用域、类/元类/外部分类和协议继承；全部仅静态编译与读取，未加载运行。ObjC 方法名称及地址对照覆盖旧 6 个切片：5 个使用 dyld_info；若固定 ARM64_32 样本仅输出空 ObjC 列表，则同时要求 nm 和 otool 完整一致，不能忽略其他差异。独立安装消费验证包身份、三个原始切片的不可变 ObjC 图和改写后的核心行为；另有 6 个安装后 CLI 编辑/组合/提取/覆盖流程，输入保持不变，输出权限 0600。

**完整项目重写尚未完成。** GUI 布局与交互、header/TBD 生成器及其渲染支持、诊断/队列/终端格式化、image 状态聚合、kernel 容器及通用命名兼容层仍含继承算法，需要继续完整复核与改写。高级 ObjC shared-cache/runtime 列表、完整 Swift 泛型/resilient 尾部和复杂名称还未实现；不能把静态字段解析写成全部语言 ABI 已完成。线程状态 CPU/ABI 解释、threaded rebase 语义、压缩 chained symbols、外部缓存/固件基址、真实设备/固件版本、所有畸形格式与 GUI 手工交互仍 OPEN。当前验证平台为 macOS/Python 3.12；Windows curses 行为尚未验证。

## 来源与 CVP

来源、固定上游提交与 MIT 许可见 [ORIGIN.md](ORIGIN.md)。保留作者与许可证；不把上游代码写成申请人独立原创。旧发布及资产保留并标注历史。

[Anthropic CVP 官方说明](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)依据实际受到防护影响的合法防御双用途任务。项目数量、改名、构建和 CI 不能证明申请资格。授权、身份、组织、实际受限任务与审批结果需要本人真实证据；不保证某一模型永不触发网络安全防护。

## 1.0.6 目录整理

旧上游指南的 8 个剩余配套文件原字节迁入 `项目文档/guides/`；运行源码、测试输入、真实上游 MIT 版权及外部许可保持原样。此次仅整理受控目录与源码包元数据；既有深层改写范围和 OPEN 项不因此改变。
