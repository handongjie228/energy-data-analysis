# 图表存放目录

运行以下任意命令后，生成的图表都会保存到这个目录：

```bash
.venv\Scripts\python.exe energy_all_in_one.py
.venv\Scripts\python.exe energy_analysis.py
```

运行后这里会出现：

| 文件 | 内容 |
|---|---|
| `energy_trend.png` | 月度用电量与 12 个月移动平均趋势图 |
| `yoy_growth.png` | 用电量同比增速图 |

图表底部会自动标注数据来源。默认来源是“内置示例数据（模拟），仅用于练习”；换成真实数据时，请用 `--source` 参数写清来源，例如：

```bash
.venv\Scripts\python.exe energy_all_in_one.py --source "国家统计局 2020-2025 年能源数据"
```

`clean_data.csv` 和 `summary.txt` 仍然保存在上一级 `output/` 目录。
