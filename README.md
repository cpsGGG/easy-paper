# Easy Paper

`easy-paper` 是一个专门帮助用户读论文的 skill。

它不是单纯的摘要工具，而是一个围绕“读懂论文”设计的阅读助手。它的目标是帮助用户先建立整篇论文的结构感，再逐个解决公式、图表、表格、代码块、引用文献、术语这些真正容易卡住的点。

## 1. 适合什么人

`easy-paper` 特别适合下面这几类用户：

- 刚开始读某个方向论文的人
- 想先快速判断一篇论文值不值得细读的人
- 读论文时经常卡在公式、图表、实验结果上的人
- 希望把多轮阅读过程整理成结构化笔记的人

## 2. 核心亮点

相比“给你一段摘要”，`easy-paper` 更强调下面这些能力：

- 全文视角优先  
  优先建立整篇论文的整体结构，而不是一上来就陷入局部细节。

- 难点解释优先  
  更关注公式、图、表、代码块、引用文献、术语这些最容易阻塞阅读的部分。

- 解释而不是堆术语  
  回答会尽量用人话解释，让用户知道“它在解决什么问题”“它为什么在这里出现”。

- 保留来源定位  
  默认尽量带页码、章节、Figure、Table、Equation 等定位信息，方便回到原文。
  默认不要报提取文本里的原始行号区间；像“第 683-960 行”这类定位通常对 PDF 读者没有实际帮助。

- 图文结合  
  以全文文本为主，在需要时自动补关键视觉页，兼顾理解效果和响应速度。

- 多轮阅读友好  
  不只支持一次性说明，还支持围绕同一篇论文持续追问，并最终整理为阅读笔记。

- 多 PDF 结果隔离  
  每篇 PDF 可以写入自己的输出目录，避免不同论文的中间结果混在一起。

## 3. 核心交互方式

统一入口是：

```text
/easy-paper <mode>
/ep <mode>
```

注意：

- `/easy-paper` 是主入口
- `/ep` 是短别名
- 不同 agent 对别名的支持方式不同
- 如果某个平台不会自动把 `/ep` 识别成 `easy-paper`，就需要额外的适配文件

当前仓库已经附带 Claude Code 的 `/ep` 适配文件：

- `agents/claude/commands/ep.md`

也就是说：

- 根目录的 `SKILL.md` 负责核心能力
- `agents/` 目录负责平台适配

当前支持的模式有：

- `map`
- `formula`
- `section`
- `figure`
- `table`
- `code`
- `cite`
- `term`
- `summary`

常见用法如下：

```text
/easy-paper map
/ep map
/easy-paper formula 请解释 Equation 4
/ep formula 请解释 Equation 4
/easy-paper section 请详细讲一下 4.2 Experimental Setup
/ep section 请详细讲一下 4.2 Experimental Setup
/easy-paper figure 请解释 Figure 2
/easy-paper table 请告诉我 Table 1 最重要的结果
/easy-paper code 请解释 Section 3 的算法流程
/easy-paper cite 21
/easy-paper term 请解释 score matching
/easy-paper summary 请整理成一份阅读笔记
```

## 4. 每个模式适合做什么

### `/easy-paper map`

这是最推荐的起手式。

它会帮助用户快速建立论文地图，重点说明：

1. 论文问题与意义
2. 核心思路与创新点
3. 方法与验证主线
4. 阅读难点
5. 下一步建议

适合场景：

- 第一次打开一篇论文
- 不确定整篇结构时
- 想先判断值不值得细读时

### `/easy-paper formula`

用于解释某个公式、loss、目标函数、更新规则。

回答通常会先解释：

1. 这个公式在解决什么问题
2. 符号分别是什么意思
3. 直觉是什么
4. 它在整篇方法里起什么作用
5. 是否需要进一步推导

### `/easy-paper section`

用于详细解释论文中的某一章节级局部单元。

这里的 `section` 是统一的用户用词，不强制区分：

- section
- subsection
- subsubsection
- 某个具名模块
- 某段实验或方法部分

回答通常会重点说明：

1. 这一节在整篇论文里要完成什么任务
2. 它和前后文的关系是什么
3. 这一节内部的关键内容是如何展开的
4. 这一节里最值得关注的公式、图、表、模块是什么
5. 这一节最容易读晕或忽略的点是什么

适合场景：

- 想详细读懂 Introduction、Method、Experiments、Conclusion
- 想解释某个 subsection，比如 `4.2 Experimental Setup`
- 想先吃透某一个局部，再回到整篇主线

### `/easy-paper figure`

用于解释图。

重点通常包括：

- 图在展示什么
- 横轴、纵轴、图例、对比组怎么读
- 最重要的趋势是什么
- 图支持了论文的什么结论

### `/easy-paper table`

用于解释表格和实验结果。

重点通常包括：

- 在比较什么
- 行列和指标怎么读
- 哪个对比最关键
- 作者希望读者从这张表中得出什么结论

### `/easy-paper code`

用于解释伪代码、算法步骤、过程框架或论文中的代码式流程块。

重点通常包括：

- 输入和输出
- 主流程
- 循环与关键判断
- 和正文方法、公式的对应关系

### `/easy-paper cite`

用于解释论文中的某一条引用文献。

回答通常会尽量包含：

1. 这条引用的完整条目信息
2. 这篇被引文献大致是什么类型的工作
3. 当前论文为什么引用它
4. 这条引用在当前论文的哪些位置或语境里出现
5. 原文链接
6. 这条引用值不值得继续读

这里有一个很重要的原则：

- 标题、作者、年份、venue、DOI、arXiv、链接这类内容，尽量作为事实给出
- “它是背景工作 / 方法来源 / baseline / 经典工作”这类内容，应该明确说是基于当前论文引用语境做出的判断

适合场景：

- 想知道参考文献 `[21]` 到底是哪篇
- 想知道某条引用为什么会出现在这里
- 想决定下一篇该顺着读哪篇参考文献

### `/easy-paper term`

用于解释术语、背景概念、默认假设。

优先按论文上下文解释，如果论文本身没有讲清楚，再补通用背景定义。

### `/easy-paper summary`

用于整理多轮讨论后的阅读笔记。

适合场景：

- 一轮阅读结束后
- 想记录自己的理解收获时
- 想把前面问过的问题收束成一份清晰总结时

## 5. 推荐使用方式

如果只给一个推荐，我建议这样用：

1. 在 VS Code 中打开包含 PDF 的文件夹
2. 打开你正在读的那篇 PDF
3. 先输入 `/easy-paper map`
4. 再围绕自己真正卡住的点继续追问
5. 最后用 `/easy-paper summary` 收尾

推荐阅读顺序通常是：

1. `/easy-paper map`
2. `/easy-paper section`
3. `/easy-paper formula`
4. `/easy-paper figure`
5. `/easy-paper table`
6. `/easy-paper code`
7. `/easy-paper cite`
8. `/easy-paper term`
9. `/easy-paper summary`

这套节奏的好处是：

- 先建立主线
- 再解决难点
- 最后整理认知

如果你觉得 `/easy-paper` 太长，可以直接用 `/ep`。两者是等价入口。

## Claude Code 安装补充

如果你是给 Claude Code 安装这个 skill，除了把 skill 主体放到 `~/.claude/skills/easy-paper/` 之外，还需要把下面这个文件放到 `~/.claude/commands/`：

- `agents/claude/commands/ep.md`

这样才能真正支持：

```text
/easy-paper map
/ep map
```

如果只安装 skill 主体而没有这个 alias 文件，通常只有 `/easy-paper` 能被识别，`/ep` 不一定能直接生效。

## 6. 我推荐你怎么用这个技能

### 推荐方式：在 VS Code 里配合 PDF 阅读

这是我最推荐的使用方式，因为它兼顾了这几件事：

- 你可以直接看原始 PDF 排版
- 你可以在聊天里持续追问
- 你能很快根据页码、Figure、Table 回到原文
- 如果需要截图，也方便立即操作

它不是“必须”，但确实是当前最自然、最稳定的使用姿势。

### 会不会麻烦

如果用户已经习惯在 VS Code 里工作，这个门槛并不高。

真正可能让用户觉得麻烦的，不是 VS Code 本身，而是如果他需要理解太多内部文件、缓存目录、脚本产物，那就会显得复杂。

所以更推荐的心智模型应该是：

- 用户只需要关心 PDF 和聊天命令
- 中间产物是系统内部辅助材料

### 如果只用终端行不行

可以，但我不推荐把“纯终端”作为主用法。

原因很简单：

- 终端适合看文本
- 终端不适合稳定地查看复杂 PDF 页面、图表、公式和版面结构

如果用户只使用终端，比较适合这些场景：

- 先抽取全文文本
- 快速看某几页文本
- 做基础问答
- 配合渲染后的图片路径进行辅助定位

但如果问题高度依赖图、表、复杂公式、双栏排版，还是图形界面更舒服。

## 7. 终端里能不能显示 PDF

单纯回答你的好奇：能做到一部分，但通常不理想。

大致分成三种情况：

- 终端看提取后的文本  
  这个很容易，适合快速浏览内容主线。

- 终端里调用外部程序打开 PDF  
  这比较常见，但本质上已经跳到图形界面了。

- 终端里直接显示图片或页面  
  某些终端和工具链可以做到，但兼容性、体验和可移植性都不太稳定，不适合作为默认产品方案。

所以结论是：

- “终端辅助阅读 PDF”可以
- “终端作为主要 PDF 阅读界面”通常不够好

## 8. 遇到这些情况时，优先用截图或页图

下面这些情况，建议优先走视觉解释：

- 双栏提取顺序乱了
- 公式乱码或符号缺失
- 图表太密集
- 表格结构丢失
- PDF 是扫描版
- 只想问页面上的某个局部区域

这时推荐流程是：

1. 打开 PDF
2. 截图整页或局部
3. 把截图发给智能体
4. 再配合对应模式提问

例如：

```text
/easy-paper figure 请解释这张截图里的图
/easy-paper formula 请解释这张截图里的公式
/easy-paper table 请解释这张截图里的表格
```

## 9. PDF 辅助脚本

当前 skill 自带两个辅助脚本：

- [extract_pdf_text.py](D:\startup\easy-paper\scripts\extract_pdf_text.py)
- [render_pdf_pages.py](D:\startup\easy-paper\scripts\render_pdf_pages.py)

它们分别用来：

- 提取全文文本
- 渲染关键 PDF 页面为图片

推荐命令：

```bash
python scripts/extract_pdf_text.py path/to/paper.pdf --output-root out
python scripts/render_pdf_pages.py path/to/paper.pdf --output-root out
```

推荐使用 `--output-root out` 的原因是：

- 每篇 PDF 会自动写入自己的目录
- 不同论文的输出不会混在一起
- 更适合多 PDF、多轮阅读场景

目录结构会类似这样：

```text
out/
  paper/
    paper.json
    paper.txt
    pages/
```

## 10. 最常用的命令

如果只记最常用的一组，记这 9 条就够了：

```text
/easy-paper map
/easy-paper formula
/easy-paper section
/easy-paper figure
/easy-paper table
/easy-paper code
/easy-paper cite
/easy-paper term
/easy-paper summary
```

## 11. 一句话总结

`easy-paper` 是一个以 `/easy-paper <mode>` 为统一入口、强调结构理解、难点解释、图文结合和多轮阅读支持的论文阅读 skill。
