# Python 能源数据分析小项目

从一份 CSV 开始，做出一个能拿给老师、学长和面试官看的数据分析作品。

> 交付物怎么做（GitHub 仓库、1 页报告、5 分钟演示、12 周计划）见 [PROJECT_DELIVERABLES_GUIDE.md](PROJECT_DELIVERABLES_GUIDE.md)。

> GitHub 注册与上传步骤见 [GITHUB_SETUP_GUIDE.md](GITHUB_SETUP_GUIDE.md)。

## 项目目标

- 学会用 pandas 读取、清洗、汇总时间序列数据。
- 学会计算环比、同比、移动平均，并画出论文级图表。
- 学会写 1 页数据分析报告，并上传到 GitHub。
- 为转专业面试、节能减排竞赛、能源经济大赛、数模国赛和大创积累素材。

## 适用对象

江苏大学 2026 级物理学（师范），计划转入能源与动力工程，目前 Python 零基础或刚入门。

## 目录结构

```
Energy_Data_Project/
├── README.md                    本文件
├── requirements.txt             依赖库
├── energy_analysis.py           主脚本
├── energy_all_in_one.py         单文件完整版（推荐直接运行）
├── check_env.py                 环境自检脚本
├── report_template.md           1 页报告模板
├── data/
│   └── monthly_energy_sample.csv  模拟示例数据
└── output/                      运行后自动生成
    ├── clean_data.csv
    ├── summary.txt
    └── charts/                   所有图表保存在这里
        ├── energy_trend.png
        ├── yoy_growth.png
        └── README.md
```

## 环境准备

本项目已经在本机创建好专用虚拟环境 `.venv`，用的是你电脑上的 Python 3.11.5，不会影响全局 Python：

| 包 | 版本 |
|---|---|
| Python | 3.11.5 |
| pandas | 3.0.6 |
| numpy | 2.4.6 |
| matplotlib | 3.11.2 |
| ipykernel | 7.4.0 |
| jupyter_client | 8.10.0 |
| nbformat | 5.11.1 |
| nbclient | 0.11.0 |
| nbconvert | 7.17.1 |
| packaging | 26.3 |

这些依赖也已经同步安装到全局 Python `D:\python311`，所以直接运行 `python energy_all_in_one.py` 也可以；但运行 Notebook 时推荐使用项目虚拟环境 `.venv`。

以后运行不需要再装任何东西。如果换电脑或误删 `.venv`，双击 `setup_env.bat` 会自动重建并安装全部依赖。

所有批处理脚本和 VS Code 终端都设置了 `PYTHONUTF8=1` 和 `PYTHONIOENCODING=utf-8`，从根源上避免中文乱码；代码里也保留了容错的 `configure_console_encoding()`，即使某个环境不支持 `reconfigure` 也不会报错。

PSReadLine 已修复：Windows PowerShell 5.1 和 PowerShell 7 都安装了 **2.4.5**，并已解除文件阻止、把 CurrentUser 执行策略设为 `RemoteSigned`。如果 VS Code 终端已经打开，关掉终端重新开一个（或 Reload Window）即可生效。

如果你想自己装 Anaconda，或者用其他 Python 环境，也可以：

```bash
pip install -r requirements.txt
```

## 运行方式

最省事的方式：直接双击 `run_analysis.bat`。它会自动使用 `.venv` 里的 Python 运行脚本，并生成图表。

如果想在命令行里运行，先跑不画图的版本，确认数据能读进来：

```bash
.venv\Scripts\python.exe energy_analysis.py --no-plot
```

再跑完整版本，生成图表：

```bash
.venv\Scripts\python.exe energy_analysis.py
```

如果你想换成自己的数据：

```bash
.venv\Scripts\python.exe energy_analysis.py --data data/我的数据.csv --out output
```

如果你想在图和摘要里标注真实数据来源：

```bash
.venv\Scripts\python.exe energy_analysis.py --source "国家统计局 2020-2025 年能源生产与消费数据"
```

想额外安装新的 Python 包时，用这一条命令，不要直接 `pip install`：

```bash
.venv\Scripts\python.exe -m pip install 包名
```

## 在 VS Code 中运行

1. 打开 VS Code，选择 **File > Open Folder**，打开 `Energy_Data_Project` 文件夹。
2. 解释器已经配置为 `.venv\Scripts\python.exe`，配置文件在 `.vscode\settings.json`。
3. 运行脚本：打开 `energy_analysis.py`，按 **F5**，或在左侧 **Run and Debug** 里选择"运行能源数据分析（完整）"。
4. 运行 Notebook：打开 `energy_analysis.ipynb`，右上角内核选择 **Python 3.11 (Energy Data Project)**，点击 **Run All**。
5. 一键运行：按 `Ctrl+Shift+B`，选择 **执行 Notebook（Jupyter 内核）**，它会在 VS Code 内部执行整个 Notebook。
6. 环境自检：按 `Ctrl+Shift+P` → **Tasks: Run Task** → **环境自检**，或双击 `run_all.bat`。
7. 已安装的 VS Code 扩展：`ms-python.python`、`ms-python.vscode-pylance`、`ms-python.debugpy`、`ms-toolsai.jupyter`。

如果 Notebook 提示找不到内核：

1. 按 `Ctrl+Shift+P`。
2. 运行 **Python: Select Interpreter**。
3. 选择 `.venv\Scripts\python.exe`。
4. 回到 Notebook，右上角重新选择内核 **Python 3.11 (Energy Data Project)**。

## 单文件版（推荐）

如果你只想要一个文件，直接用 `energy_all_in_one.py`。它把环境自检、数据读取、清洗、指标、图表和报告输出全部合并在一个文件里，并且内置了一份示例数据：即使外部 CSV 丢失，也能完整跑通。

```bash
.venv\Scripts\python.exe energy_all_in_one.py --check
.venv\Scripts\python.exe energy_all_in_one.py
.venv\Scripts\python.exe energy_all_in_one.py --no-plot
.venv\Scripts\python.exe energy_all_in_one.py --use-embedded
```

在 VS Code 里也可以按 `Ctrl+Shift+P` → **Tasks: Run Task**，选择：

- **单文件环境自检**
- **运行单文件版（完整）**
- **运行单文件版（不画图）**

也可以直接双击 `run_all_in_one.bat`，或者在 VS Code 里打开 `energy_all_in_one.py` 后按 `F5`，选择 **运行单文件版（完整）**。

图表风格说明：两张图统一使用 0 基线、浅色横向网格、去掉顶部和右侧边框，只标注最高点和最低点，并在图底部标注数据来源。这样既简洁，也避免用截断坐标轴夸大变化。默认数据来源是“内置示例数据（模拟），仅用于练习”；换成真实数据后，用 `--source` 写明来源即可。

图表保存位置：默认保存到 `output/charts/`，其中 `energy_trend.png` 是趋势图，`yoy_growth.png` 是同比图。`clean_data.csv` 和 `summary.txt` 仍然保存在 `output/`。如果你想换个目录，可以用 `--charts-dir`：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --charts-dir output/我的图表
```

## 数据说明

`data/monthly_energy_sample.csv` 是为了练习**模拟生成**的校园用电数据，不是真实统计数据，仅用于跑通流程。包含字段：

| 字段 | 含义 | 单位 |
|---|---|---|
| month | 月份 | YYYY-MM |
| electricity_mwh | 校园月度用电量 | MWh |
| temperature_c | 月平均气温 | ℃ |
| occupancy_rate | 在校人数比例 | 0-1 |

真实数据来源：

| 来源 | 网址 | 能拿到什么 |
|---|---|---|
| 国家统计局 国家数据 | https://data.stats.gov.cn/ | 能源生产、消费、电力、经济数据 |
| 国家能源局 | https://www.nea.gov.cn/ | 电力、新能源、政策 |
| 中国电力企业联合会 | https://www.cec.org.cn/ | 电力工业统计 |
| IEA | https://www.iea.org/data-and-statistics | 国际能源数据 |
| Our World in Data | https://ourworldindata.org/energy | 全球能源与碳排放 |
| 江苏大学图书馆 | https://lib.ujs.edu.cn/ | CNKI、Web of Science、论文 |

换数据时参考下面的“如何分析其他数据”。

## 如何分析其他数据

单文件版 `energy_all_in_one.py` 支持 CSV、XLSX、XLSM，支持自定义列名和不同时间频率。

### 1. 数据最少需要两列

| 列 | 含义 | 是否必需 |
|---|---|---|
| 日期列 | 月份、季度、年份或具体日期 | 必需 |
| 数值列 | 要分析的指标 | 必需 |
| 温度列 | 做相关性分析 | 可选 |
| 占用率列 | 做相关性分析 | 可选 |

### 2. 列名一样时

如果列名就是 `month`、`electricity_mwh`、`temperature_c`、`occupancy_rate`，直接传数据文件：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/我的数据.csv
```

### 3. 列名不一样时

例如列名是 `日期`、`用电量`、`气温`：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/我的数据.csv --date-col 日期 --value-col 用电量 --temp-col 气温 --title "某市用电量" --value-label "用电量（亿千瓦时）"
```

如果数据里没有温度或占用率列，不用管它们，程序会自动跳过相关性分析。

### 4. Excel 文件

`.xlsx` 和 `.xlsm` 直接传：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/我的数据.xlsx --date-col date --value-col value
```

如果数据不在第一个工作表，用 `--sheet` 指定工作表名称或序号：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/多表.xlsx --sheet 数据 --date-col date --value-col value
```

如果表头不在第一行，用 `--header-row` 指定（0 表示第一行，1 表示第二行）：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/我的数据.csv --header-row 1 --date-col date --value-col value
```

旧版 `.xls` 请先另存为 `.xlsx` 或 `.csv`。

### 5. 不同时间频率

`--periods` 表示同比周期：月度=12，季度=4，年度=1，日度=365。

```bash
.venv\Scripts\python.exe energy_all_in_one.py --data data/季度数据.csv --periods 4 --title "某市季度用电量"
```

日期列支持 `YYYY-MM`、`YYYY-Q1`、`YYYY-MM-DD` 等格式。

### 6. 换数据时的检查清单

1. 日期列能解析成日期。
2. 数值列是数字，不是带单位的文本。
3. 缺失值和重复日期会自动处理，但要在报告中说明。
4. 所有数字写清来源、时间范围和单位，用 `--source` 标注。

### 7. 输出位置

- `output/clean_data.csv`：清洗后的数据。
- `output/summary.txt`：摘要。
- `output/charts/energy_trend.png`：趋势图。
- `output/charts/yoy_growth.png`：同比图。
- 用 `--out` 和 `--charts-dir` 可以修改输出目录。

## 8 周执行计划

| 周次 | 任务 | 交付物 |
|---|---|---|
| 第 1 周 | 安装环境，运行脚本，理解每一列 | 环境截图 + 能跑通的脚本 |
| 第 2 周 | 换一份真实数据，处理日期、缺失值、单位 | `output/clean_data.csv` + 数据质量说明 |
| 第 3 周 | 计算环比、同比、12 个月移动平均 | 指标表 + 3 条发现 |
| 第 4 周 | 画月度趋势图和同比图 | `energy_trend.png`、`yoy_growth.png` |
| 第 5 周 | 加入第二个变量（气温、GDP、人口等） | 相关性分析 |
| 第 6 周 | 写 1 页报告（数据来源、方法、发现、局限） | `report.md` |
| 第 7 周 | 写 README，上传 GitHub | GitHub 仓库链接 |
| 第 8 周 | 录 5 分钟演示，收集 3 条反馈 | 演示视频 + 反馈记录 |

## 交付物清单

- [ ] `energy_analysis.py` 能一键运行。
- [ ] `output/clean_data.csv` 清洗后的数据。
- [ ] 数据质量说明：缺失值数量、重复月份、单位与口径。
- [ ] 2 张带标题、单位、数据来源的图。
- [ ] 1 页报告，至少 3 条结论和 1 条局限。
- [ ] GitHub 仓库和一个 5 分钟演示。

## 如何升级为竞赛或科研项目

1. 把示例数据换成真实数据（国家统计局、中电联、IEA）。
2. 把题目从"趋势分析"升级为"影响因素分析"或"预测"。
3. 加入第二个变量，做相关性或简单回归。
4. 报名全国大学生能源经济学术创意大赛（https://energy.qibebt.ac.cn/eneco/contribution/index.html）。
5. 把代码和报告作为大创、节能减排、数模国赛的支撑材料。

## 注意事项

1. 不伪造数据，所有数字写清来源、时间和口径。
2. 相关性不等于因果，报告里不要下过度结论。
3. 图表必须有标题、单位、数据来源。
4. 先跑通最小版本，再慢慢加功能，不要一开始就追求完美。
