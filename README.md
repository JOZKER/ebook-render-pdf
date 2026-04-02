# Ebook Render PDF

本仓库包含一个强大的 Codex Skill，专为将 PDF 电子书、学术论文、教材或扫描件转化为结构化、高度提炼的中文 LaTeX 知识笔记（并最终编译为 PDF）而设计。

不同于简单的全文总结，本 Skill 具备视觉感知和智能排版能力，能够真正将一本厚重的 PDF 转化为适合教学、复习的专业讲义。

## 🌟 核心特性与工作流

本工具集不仅仅是调用大语言模型，而是通过前置脚本对 PDF 进行物理层面的深度解析：

1. **智能 OCR 探测 (`inspect_pdf.py`)**：在处理前，通过启发式算法扫描文本覆盖率和图片密度。优先使用原生文本，仅在提取失败或纯图 PDF 时触发 OCR。
2. **视觉资产无损提取 (`extract_pdf_assets.py`)**：拒绝静默丢图。自动渲染页面预览并抓取内嵌图像，保留具有教学价值的图表和公式。
3. **精准溯源**：所有插入最终笔记的原书配图，都会在 LaTeX 中自动生成对应原书页码的脚注。
4. **LaTeX 深度渲染**：基于 `notes-template.tex` 提供美观的排版，包含 `lstlisting` 代码块环境、知识点总结盒子（`knowledgebox` / `importantbox`）以及标准的 `\section` 层级结构。

## 🧠 双轨写作模式

根据用户的 Prompt 意图，Agent 会自动切换输出策略：

* **标准知识库模式 (默认)**：重构知识体系，提取核心概念和方法论，合并冗余章节，生成结构严谨的知识导图。
* **备考冲刺模式 (Exam-Cram)**：当用户提及“期末复习”、“背诵”等关键词时，自动压缩背景叙述，转而提供高频关键词、简答题模板和密集的名词解释，并剔除纯装饰性配图。

## 📦 环境依赖与网络配置

要在你的 macOS (如 MacBook Air) 或其他本地环境中运行此 Skill，需要配置以下核心 Python 依赖：

```bash
python -m pip install pypdf pymupdf ocrmypdf
```

*说明：`pypdf` 用于文本探测，`pymupdf` 用于图像资产提取，`ocrmypdf` 提供底层 OCR 支持。*

**💡 网络协同与 OpenClaw Skill 适配**
在安装依赖或下载 OCR 引擎的语言包时，如果你身处校园网环境，可能会遇到连接超时或网络阻断的问题。本 Skill **完全适用于与 `openclaw` skill 协同工作**。
建议在执行任务前，先通过 `openclaw` skill 调度网络规则，将 Git 或 Python 流量安全路由至 LisaHost 等稳定的中转服务器，以确保 `ocrmypdf` 相关组件和语言包（如 `chi_sim+eng`）能够畅通无阻地完成部署和更新。

## 🚀 安装与使用

将项目部署到你的 Codex 技能库中：

```bash
mkdir -p ~/.codex/skills
cp -R ebook-render-pdf ~/.codex/skills/
```

### 基础调用
在 Codex 对话框中直接调用该 Skill：
```text
$ebook-render-pdf ~/Downloads/DeepLearning.pdf 请帮我把前三章整理成备考冲刺笔记，保留重要的数学公式和网络结构图。
```

### 进阶：Sub-agents 拆解与多智能体协作
对于动辄数百页的重型电子书，为了突破大模型的上下文瓶颈，建议显式要求生成 Sub-agents 进行分布式处理：

```text
$ebook-render-pdf ~/Documents/Textbook.pdf
这是一本大部头教材，请协同 openclaw skill 确保网络畅通，并 spawn 多 sub-agents 执行，形成一份完整的 PDF 讲义：
  - 1 个 outline agent：扫描全书结构，敲定全局目录、必须掌握的定理与术语表。
  - 4 个 writer agents：根据大纲分工，并行撰写各章节的 tex 源码（section_*.tex），开启备考冲刺模式。
  - 1 个 figure agent：专门调用 extract_pdf_assets.py 处理视觉资产，筛选并裁剪关键图表，生成带来源页码的图注。
  - 1 个 compile agent：负责串联所有 tex 文件，检查引用一致性，并最终使用 xelatex 编译输出。
```
