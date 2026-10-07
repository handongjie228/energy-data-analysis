"""能源数据分析单文件完整版。

这个文件把项目的全部代码合并到一个 Python 文件里：
    1. 环境自检
    2. 读取 CSV（支持外部数据，也内置一份示例数据）
    3. 数据清洗：日期、数值、缺失值、重复月份
    4. 指标：环比、同比、12 个月移动平均
    5. 摘要：总量、均值、最高/最低月份、相关系数
    6. 图表：趋势图、同比图
    7. 输出：clean_data.csv、summary.txt、两张 PNG

用法（在项目根目录）：
    .venv\\Scripts\\python.exe energy_all_in_one.py
    .venv\\Scripts\\python.exe energy_all_in_one.py --no-plot
    .venv\\Scripts\\python.exe energy_all_in_one.py --check
    .venv\\Scripts\\python.exe energy_all_in_one.py --use-embedded
    .venv\\Scripts\\python.exe energy_all_in_one.py --data data/我的数据.csv --out output

分析其他数据：
    .venv\\Scripts\\python.exe energy_all_in_one.py --data data/其他数据.csv --date-col 日期 --value-col 用电量
    .venv\\Scripts\\python.exe energy_all_in_one.py --data data/其他数据.xlsx --date-col date --value-col value
    .venv\\Scripts\\python.exe energy_all_in_one.py --data data/多表.xlsx --sheet 数据 --header-row 0
    .venv\\Scripts\\python.exe energy_all_in_one.py --data data/季度数据.csv --periods 4 --title "某市用电量" --value-label "用电量（亿千瓦时）"

支持的输入格式：CSV、XLSX、XLSM。旧版 .xls 请先另存为 .xlsx 或 .csv。
"""

from __future__ import annotations

import argparse
import importlib
import io
import math
import sys
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd

DATE_COL = "month"
VALUE_COL = "electricity_mwh"
TEMP_COL = "temperature_c"
OCCUPANCY_COL = "occupancy_rate"

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "monthly_energy_sample.csv"
DEFAULT_OUTPUT_DIR = BASE_DIR / "output"
DEFAULT_CHARTS_DIR = DEFAULT_OUTPUT_DIR / "charts"

# 内置示例数据：外部 CSV 丢失时，程序仍然可以完整跑通。
SAMPLE_CSV = """month,electricity_mwh,temperature_c,occupancy_rate
2025-01,1850,3.2,0.85
2025-02,1500,6.1,0.55
2025-03,1650,11.4,0.95
2025-04,1550,17.2,0.97
2025-05,1700,22.3,0.98
2025-06,1950,26.1,0.95
2025-07,,30.2,0.45
2025-08,2050,29.4,0.50
2025-09,1750,25.1,0.98
2025-10,1500,19.3,0.98
2025-11,1600,12.2,0.97
2025-12,1900,6.4,0.90
2026-01,1920,3.5,0.85
2026-02,1560,6.3,0.55
2026-03,,11.8,0.95
2026-04,1600,17.6,0.97
2026-05,1760,22.8,0.98
2026-06,2030,26.5,0.95
2026-07,2300,30.6,0.45
2026-08,2140,29.8,0.50
2026-09,1820,25.4,0.98
2026-10,1560,19.6,0.98
2026-11,1660,12.5,0.97
2026-12,1980,6.6,0.90
"""


# ---------------------------------------------------------------------------
# 基础工具
# ---------------------------------------------------------------------------
def configure_console_encoding() -> None:
    """尽量把控制台切到 UTF-8；环境不支持时静默跳过。"""
    try:
        reconfigure = getattr(sys.stdout, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    except Exception:
        pass


def _package_version(module_name: str) -> str:
    module = importlib.import_module(module_name)
    return str(getattr(module, "__version__", "unknown"))


def _version_at_least(version: str, minimum: str) -> bool:
    try:
        from packaging.version import Version

        return Version(version) >= Version(minimum)
    except Exception:
        return True


# ---------------------------------------------------------------------------
# 环境自检
# ---------------------------------------------------------------------------
def check_environment() -> int:
    checks: list[tuple[str, Callable[[], str], bool]] = [
        ("Python 版本", lambda: f"Python {sys.version.split()[0]}", sys.version_info >= (3, 10)),
    ]

    for module_name, minimum in [
        ("pandas", "2.0"),
        ("numpy", "1.24"),
        ("matplotlib", "3.7"),
    ]:
        checks.append(
            (
                module_name,
                lambda name=module_name, low=minimum: (
                    f"{name} {_package_version(name)}"
                    if _version_at_least(_package_version(name), low)
                    else f"{name} 版本过低，需要 >= {low}"
                ),
                True,
            )
        )

    def data_detail() -> str:
        if DEFAULT_DATA_PATH.exists():
            df = pd.read_csv(DEFAULT_DATA_PATH)
            return f"外部数据 {len(df)} 行：{DEFAULT_DATA_PATH.name}"
        return "外部数据不存在，将使用内置示例数据"

    def openpyxl_detail() -> str:
        try:
            return f"openpyxl {_package_version('openpyxl')}（Excel 支持）"
        except Exception as exc:  # noqa: BLE001
            return f"未安装（CSV 不受影响，Excel 需要）：{type(exc).__name__}"

    def output_detail() -> str:
        DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        probe = DEFAULT_OUTPUT_DIR / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return f"{DEFAULT_OUTPUT_DIR} 可写"

    def charts_detail() -> str:
        DEFAULT_CHARTS_DIR.mkdir(parents=True, exist_ok=True)
        probe = DEFAULT_CHARTS_DIR / ".write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
        return f"{DEFAULT_CHARTS_DIR} 可写"

    def kernel_detail() -> str:
        try:
            from jupyter_client.kernelspec import KernelSpecManager

            kernels = KernelSpecManager().find_kernel_specs()
            if "energy-venv" in kernels:
                return "energy-venv 已注册（Notebook 可用）"
            return "未注册 energy-venv（仅 Notebook 需要，脚本运行不受影响）"
        except Exception as exc:  # noqa: BLE001
            return f"未检查（{type(exc).__name__}），脚本运行不受影响"

    checks.extend(
        [
            ("数据文件", data_detail, True),
            ("openpyxl", openpyxl_detail, False),
            ("输出目录", output_detail, True),
            ("图表目录", charts_detail, True),
            ("Jupyter 内核", kernel_detail, False),
        ]
    )

    print("环境自检报告")
    print("=" * 60)
    failed_required: list[str] = []
    for name, func, required in checks:
        try:
            detail = func()
            status = "PASS"
        except Exception as exc:  # noqa: BLE001
            detail = f"{type(exc).__name__}: {exc}"
            status = "FAIL" if required else "INFO"
        if status == "FAIL":
            failed_required.append(name)
        print(f"[{status}] {name:<12}: {detail}")
    print("=" * 60)

    if failed_required:
        print("失败项：" + "、".join(failed_required))
        print("请先修复失败项，再运行完整分析。")
        return 1

    print("环境检查通过，可以开始分析。")
    return 0


# ---------------------------------------------------------------------------
# 数据读取与清洗
# ---------------------------------------------------------------------------
def load_data(
    path: Path | None,
    sheet: int | str = 0,
    header_row: int = 0,
) -> pd.DataFrame:
    """读取 CSV 或 Excel；找不到时改用内置示例数据。

    sheet 可以是工作表序号或名称；header_row 是表头所在行（0 表示第一行）。
    """
    if path is not None and path.exists():
        print(f"读取数据文件：{path}")
        suffix = path.suffix.lower()
        if suffix in {".xlsx", ".xlsm"}:
            try:
                import openpyxl  # noqa: F401
            except ImportError as exc:
                raise SystemExit(
                    "读取 Excel 需要 openpyxl，请运行：\n"
                    "  python -m pip install -r requirements.txt"
                ) from exc
            df = pd.read_excel(path, sheet_name=sheet, header=header_row)
        elif suffix == ".xls":
            raise SystemExit("旧版 .xls 请先另存为 .xlsx 或 .csv，再运行。")
        else:
            df = pd.read_csv(path, header=header_row)
    else:
        if path is not None:
            print(f"未找到数据文件：{path}")
        print("使用内置示例数据（模拟数据，仅用于练习）。")
        df = pd.read_csv(io.StringIO(SAMPLE_CSV))

    df.columns = [str(c).strip() for c in df.columns]
    if DATE_COL not in df.columns:
        raise ValueError(f"数据缺少月份列：{DATE_COL}")
    if VALUE_COL not in df.columns:
        raise ValueError(f"数据缺少用电量列：{VALUE_COL}")

    df[DATE_COL] = pd.to_datetime(
        df[DATE_COL], errors="coerce", format="mixed"
    )
    df = df.dropna(subset=[DATE_COL])

    duplicate_count = int(df[DATE_COL].duplicated().sum())
    if duplicate_count:
        print(f"发现 {duplicate_count} 个重复月份，已保留每月最后一条记录。")
        df = df.drop_duplicates(subset=[DATE_COL], keep="last")

    df = df.sort_values(DATE_COL).reset_index(drop=True)
    return df


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """数值列转数字，时间插值补缺失值，并记录缺失情况。"""
    df = df.copy()
    numeric_cols = [
        col
        for col in [VALUE_COL, TEMP_COL, OCCUPANCY_COL]
        if col in df.columns
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_before = {
        str(col): int(count)
        for col, count in df[numeric_cols].isna().sum().items()
    }

    df = df.set_index(DATE_COL)
    df[numeric_cols] = df[numeric_cols].interpolate(
        method="time", limit_direction="both"
    )
    df[numeric_cols] = df[numeric_cols].ffill().bfill()
    df = df.reset_index()
    return df, missing_before


def add_metrics(df: pd.DataFrame, periods: int = 12) -> pd.DataFrame:
    """计算环比、同比和移动平均；periods 由数据频率决定。"""
    df = df.sort_values(DATE_COL).reset_index(drop=True)
    df["mom_growth"] = df[VALUE_COL].pct_change(periods=1)
    df["yoy_growth"] = df[VALUE_COL].pct_change(periods=periods)
    window = max(2, int(periods))
    df["ma12"] = df[VALUE_COL].rolling(
        window=window, min_periods=max(2, window // 2)
    ).mean()
    return df


# ---------------------------------------------------------------------------
# 摘要与图表
# ---------------------------------------------------------------------------
def _as_float(value: Any) -> float:
    """把 pandas/numpy 标量安全转成 Python float。"""
    array = np.asarray(value, dtype=float).reshape(-1)
    if array.size == 0:
        raise ValueError("无法把空值转换成数值")
    return float(array[0])


def _correlation(df: pd.DataFrame, other_col: str) -> float | None:
    """用 numpy 计算两列相关系数；样本不足或结果无效时返回 None。"""
    pair = df[[VALUE_COL, other_col]].astype(float).dropna()
    if len(pair) < 3:
        return None
    array = np.asarray(pair, dtype=float)
    if array.ndim != 2 or array.shape[1] != 2 or array.shape[0] < 3:
        return None
    corr = float(np.corrcoef(array[:, 0], array[:, 1])[0, 1])
    return None if math.isnan(corr) else corr


def summarize(df: pd.DataFrame, missing_before: dict[str, int]) -> dict[str, Any]:
    """生成可直接写进报告的摘要。"""
    valid = df.dropna(subset=[VALUE_COL])
    if valid.empty:
        raise ValueError("清洗后没有可用的数值数据。")

    values = np.asarray(valid[VALUE_COL], dtype=float)
    max_pos = int(np.argmax(values))
    min_pos = int(np.argmin(values))
    max_value = float(values[max_pos])
    min_value = float(values[min_pos])
    max_date = pd.Timestamp(valid[DATE_COL].iloc[max_pos])
    min_date = pd.Timestamp(valid[DATE_COL].iloc[min_pos])
    yoy_values = np.asarray(df["yoy_growth"].dropna(), dtype=float)

    date_values = df[DATE_COL].to_numpy()
    start = pd.Timestamp(date_values.min()).strftime("%Y-%m")
    end = pd.Timestamp(date_values.max()).strftime("%Y-%m")
    summary: dict[str, Any] = {
        "行数": len(df),
        "时间范围": f"{start} 至 {end}",
        "缺失值处理前": missing_before,
        "总数值": round(_as_float(np.nansum(values)), 2),
        "平均每期": round(_as_float(np.nanmean(values)), 2),
        "最高期": f"{max_date:%Y-%m}（{max_value:.2f}）",
        "最低期": f"{min_date:%Y-%m}（{min_value:.2f}）",
        "平均同比增速": (
            f"{_as_float(np.nanmean(yoy_values)) * 100:.1f}%"
            if yoy_values.size > 0
            else "样本不足"
        ),
    }

    if TEMP_COL in df.columns:
        corr_value = _correlation(df, TEMP_COL)
        if corr_value is not None:
            summary["数值与温度相关系数"] = round(corr_value, 3)

    if OCCUPANCY_COL in df.columns:
        corr_occ_value = _correlation(df, OCCUPANCY_COL)
        if corr_occ_value is not None:
            summary["数值与占用率相关系数"] = round(corr_occ_value, 3)

    return summary


def setup_matplotlib() -> Any:
    """延迟导入 matplotlib，并设置中文字体。"""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.sans-serif"] = [
        "Microsoft YaHei",
        "SimHei",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    plt.rcParams["axes.unicode_minus"] = False
    return plt


def _style_axes(ax: Any) -> None:
    """统一图表风格：轻网格、去顶右边框、清晰刻度。"""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#9CA3AF")
    ax.spines["bottom"].set_color("#9CA3AF")
    ax.grid(axis="y", color="#D1D5DB", linewidth=0.7, alpha=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", labelsize=9, colors="#374151")


def _add_footnote(fig: Any, source: str) -> None:
    """在图底部标注数据来源，保证图表客观、可追溯。"""
    fig.text(0.01, 0.015, f"数据来源：{source}", fontsize=8, color="#6B7280")


def plot_trend(
    df: pd.DataFrame,
    charts_dir: Path,
    source: str,
    title: str,
    value_label: str,
    periods: int,
) -> Path | None:
    try:
        plt = setup_matplotlib()
    except ImportError:
        print("未安装 matplotlib，跳过趋势图。运行：pip install -r requirements.txt")
        return None

    import matplotlib.dates as mdates

    ma_label = {
        12: "12 个月移动平均",
        4: "4 个季度移动平均",
        1: "年度移动平均",
        365: "365 天移动平均",
    }.get(periods, f"{periods} 期移动平均")

    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.plot(
        df[DATE_COL],
        df[VALUE_COL],
        color="#1F4E79",
        linewidth=1.6,
        marker="o",
        markersize=3,
        label="实际值",
    )
    ax.plot(
        df[DATE_COL],
        df["ma12"],
        color="#2A7F7A",
        linestyle="--",
        linewidth=2.6,
        label=ma_label,
    )

    values = np.asarray(df[VALUE_COL], dtype=float)
    mean_value = _as_float(np.nanmean(values))
    ax.axhline(
        mean_value,
        color="#6B7280",
        linestyle=":",
        linewidth=1.2,
        label=f"历史均值 {mean_value:.0f} MWh",
    )

    max_pos = int(np.argmax(values))
    min_pos = int(np.argmin(values))
    max_value = float(values[max_pos])
    min_value = float(values[min_pos])
    max_date = pd.Timestamp(df[DATE_COL].iloc[max_pos])
    min_date = pd.Timestamp(df[DATE_COL].iloc[min_pos])
    ax.annotate(
        f"最高 {max_value:.0f}",
        xy=(max_date, max_value),
        xytext=(8, 10),
        textcoords="offset points",
        fontsize=8,
        color="#1F4E79",
    )
    ax.annotate(
        f"最低 {min_value:.0f}",
        xy=(min_date, min_value),
        xytext=(8, -16),
        textcoords="offset points",
        fontsize=8,
        color="#B23A48",
    )

    date_values = df[DATE_COL].to_numpy()
    start = pd.Timestamp(date_values.min()).strftime("%Y-%m")
    end = pd.Timestamp(date_values.max()).strftime("%Y-%m")
    ax.set_title(
        f"{title}与 {ma_label}（{start} 至 {end}）",
        loc="left",
        fontsize=13,
        fontweight="bold",
        color="#111827",
        pad=12,
    )
    ax.set_xlabel("时间", fontsize=10)
    ax.set_ylabel(value_label, fontsize=10)
    ax.set_ylim(0, float(np.nanmax(values)) * 1.15)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.legend(frameon=False, ncol=3, loc="upper left", fontsize=9)
    _style_axes(ax)

    fig.autofmt_xdate(rotation=45)
    _add_footnote(fig, source)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.88, bottom=0.20)

    path = charts_dir / "energy_trend.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_yoy(
    df: pd.DataFrame,
    charts_dir: Path,
    source: str,
    title: str,
) -> Path | None:
    try:
        plt = setup_matplotlib()
    except ImportError:
        print("未安装 matplotlib，跳过同比图。运行：pip install -r requirements.txt")
        return None

    import matplotlib.dates as mdates

    yoy = df.dropna(subset=["yoy_growth"]).copy()
    if yoy.empty:
        print("样本不足 12 个月，跳过同比图。")
        return None

    yoy_values = np.asarray(yoy["yoy_growth"], dtype=float) * 100
    colors = ["#2A7F7A" if value >= 0 else "#B23A48" for value in yoy_values]

    fig, ax = plt.subplots(figsize=(10, 5.2))
    ax.bar(yoy[DATE_COL], yoy_values, color=colors, width=20)
    ax.axhline(0, color="#374151", linewidth=0.9)

    max_pos = int(np.argmax(yoy_values))
    min_pos = int(np.argmin(yoy_values))
    for pos, offset in [(max_pos, 8), (min_pos, -16)]:
        value = float(yoy_values[pos])
        date = pd.Timestamp(yoy[DATE_COL].iloc[pos])
        ax.annotate(
            f"{value:.1f}%",
            xy=(date, value),
            xytext=(0, offset),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color="#2A7F7A" if value >= 0 else "#B23A48",
        )

    date_values = yoy[DATE_COL].to_numpy()
    start = pd.Timestamp(date_values.min()).strftime("%Y-%m")
    end = pd.Timestamp(date_values.max()).strftime("%Y-%m")
    ax.set_title(
        f"{title}同比增速（{start} 至 {end}）",
        loc="left",
        fontsize=13,
        fontweight="bold",
        color="#111827",
        pad=12,
    )
    ax.set_xlabel("时间", fontsize=10)
    ax.set_ylabel("同比增速（%）", fontsize=10)
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    _style_axes(ax)

    fig.autofmt_xdate(rotation=45)
    _add_footnote(fig, source)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.88, bottom=0.24)

    path = charts_dir / "yoy_growth.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return path


def write_summary(summary: dict[str, Any], path: Path) -> None:
    lines = ["能源数据分析摘要", "=" * 20]
    for key, value in summary.items():
        lines.append(f"{key}：{value}")
    lines.extend(
        [
            "",
            "提示：如果使用的是内置或示例数据，请在报告中写明",
            "“数据为模拟数据，仅用于练习，不代表任何真实机构”。",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# 主程序
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="能源数据分析单文件完整版")
    parser.add_argument(
        "--data",
        default=str(DEFAULT_DATA_PATH),
        help="数据文件路径（CSV/XLSX/XLSM）；找不到时自动使用内置示例数据",
    )
    parser.add_argument(
        "--sheet",
        default="0",
        help="Excel 工作表名称或序号；默认第一个工作表",
    )
    parser.add_argument(
        "--header-row",
        type=int,
        default=0,
        help="表头所在行；0 表示第一行",
    )
    parser.add_argument(
        "--out",
        default=str(DEFAULT_OUTPUT_DIR),
        help="输出目录",
    )
    parser.add_argument(
        "--charts-dir",
        default=str(DEFAULT_CHARTS_DIR),
        help="图表保存目录；默认是 output/charts",
    )
    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="只做数据分析，不生成图表",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="只做环境自检，然后退出",
    )
    parser.add_argument(
        "--use-embedded",
        action="store_true",
        help="强制使用内置示例数据",
    )
    parser.add_argument(
        "--source",
        default="内置示例数据（模拟），仅用于练习",
        help="图表和摘要中的数据来源说明",
    )
    parser.add_argument(
        "--date-col",
        default="month",
        help="日期/时间列名；默认 month",
    )
    parser.add_argument(
        "--value-col",
        default="electricity_mwh",
        help="要分析的数值列名；默认 electricity_mwh",
    )
    parser.add_argument(
        "--temp-col",
        default="temperature_c",
        help="温度列名；没有该列时自动跳过温度相关性",
    )
    parser.add_argument(
        "--occupancy-col",
        default="occupancy_rate",
        help="在校人数/占用率列名；没有该列时自动跳过",
    )
    parser.add_argument(
        "--periods",
        type=int,
        default=12,
        help="同比周期：月度=12，季度=4，年度=1，日度=365",
    )
    parser.add_argument(
        "--title",
        default="校园用电量",
        help="图表标题主体；例如 某市用电量",
    )
    parser.add_argument(
        "--value-label",
        default="用电量（MWh）",
        help="趋势图 Y 轴单位；例如 用电量（亿千瓦时）",
    )
    return parser


def main() -> None:
    global DATE_COL, VALUE_COL, TEMP_COL, OCCUPANCY_COL

    configure_console_encoding()
    args = build_parser().parse_args()

    if args.check:
        raise SystemExit(check_environment())

    DATE_COL = args.date_col
    VALUE_COL = args.value_col
    TEMP_COL = args.temp_col
    OCCUPANCY_COL = args.occupancy_col
    sheet: int | str = int(args.sheet) if str(args.sheet).isdigit() else args.sheet

    data_path = None if args.use_embedded else Path(args.data)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    charts_dir = Path(args.charts_dir)
    charts_dir.mkdir(parents=True, exist_ok=True)

    df = load_data(data_path, sheet=sheet, header_row=args.header_row)
    df, missing_before = clean_data(df)
    df = add_metrics(df, periods=args.periods)

    clean_path = out_dir / "clean_data.csv"
    df.to_csv(clean_path, index=False, encoding="utf-8-sig")

    summary = summarize(df, missing_before)
    summary["数据来源"] = args.source
    summary["数值标签"] = args.value_label
    summary_path = out_dir / "summary.txt"
    write_summary(summary, summary_path)

    print("\n分析摘要")
    for key, value in summary.items():
        print(f"  {key}：{value}")
    print(f"\n已保存清洗后的数据：{clean_path}")
    print(f"已保存摘要：{summary_path}")

    if not args.no_plot:
        trend = plot_trend(
            df,
            charts_dir,
            args.source,
            args.title,
            args.value_label,
            args.periods,
        )
        yoy = plot_yoy(df, charts_dir, args.source, args.title)
        if trend:
            print(f"已生成趋势图：{trend}")
        if yoy:
            print(f"已生成同比图：{yoy}")

    print(f"\n完成。输出目录：{out_dir}")
    print(f"图表目录：{charts_dir}")
    print("下一步：把 output/summary.txt 和两张图放进 report_template.md。")


if __name__ == "__main__":
    main()
