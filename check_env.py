"""环境自检脚本。

用法：
    .venv\\Scripts\\python.exe check_env.py

它会检查 Python 版本、依赖库、数据文件、Notebook、输出目录和 Jupyter 内核。
任何一项失败都会以非零退出码结束，方便在 VS Code 任务或批处理里自动判断。
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "monthly_energy_sample.csv"
NOTEBOOK_PATH = BASE_DIR / "energy_analysis.ipynb"
OUTPUT_DIR = BASE_DIR / "output"
CHARTS_DIR = OUTPUT_DIR / "charts"
REQUIRED_COLUMNS = {"month", "electricity_mwh"}


def configure_console_encoding() -> None:
    """尽量把控制台切到 UTF-8；环境不支持时静默跳过，不影响自检。"""
    try:
        reconfigure = getattr(sys.stdout, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8")
    except Exception:
        pass


def check_python() -> str:
    if sys.version_info < (3, 10):
        raise RuntimeError("需要 Python 3.10 或更高版本")
    return f"Python {sys.version.split()[0]}"


def check_package(module_name: str, minimum: str) -> str:
    module = importlib.import_module(module_name)
    version = getattr(module, "__version__", "unknown")
    try:
        from packaging.version import Version

        if Version(version) < Version(minimum):
            raise RuntimeError(f"{module_name} {version} 低于最低要求 {minimum}")
    except ImportError:
        pass
    return f"{module_name} {version}"


def check_data_file() -> str:
    import pandas as pd

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"找不到数据文件：{DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"数据缺少列：{', '.join(sorted(missing))}")
    if len(df) < 12:
        raise ValueError(f"数据只有 {len(df)} 行，至少需要 12 个月")
    return f"{len(df)} 行，列：{', '.join(df.columns)}"


def check_notebook() -> str:
    import nbformat

    if not NOTEBOOK_PATH.exists():
        raise FileNotFoundError(f"找不到 Notebook：{NOTEBOOK_PATH}")
    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    if not code_cells:
        raise ValueError("Notebook 里没有代码单元格")
    return f"{len(nb.cells)} 个单元格，其中 {len(code_cells)} 个代码单元格"


def check_output_dir() -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    probe = OUTPUT_DIR / ".write_test"
    probe.write_text("ok", encoding="utf-8")
    probe.unlink()
    return f"{OUTPUT_DIR} 可写"


def check_charts_dir() -> str:
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    probe = CHARTS_DIR / ".write_test"
    probe.write_text("ok", encoding="utf-8")
    probe.unlink()
    return f"{CHARTS_DIR} 可写"


def check_kernel() -> str:
    from jupyter_client.kernelspec import KernelSpecManager

    manager = KernelSpecManager()
    kernels = manager.find_kernel_specs()
    if "energy-venv" not in kernels:
        raise RuntimeError(
            "找不到 energy-venv 内核。请运行 setup_env.bat，"
            "或在 VS Code 里选择 .venv\\Scripts\\python.exe 作为解释器。"
        )
    return f"energy-venv -> {kernels['energy-venv']}"


def main() -> None:
    configure_console_encoding()
    checks = [
        ("Python 版本", check_python),
        ("pandas", lambda: check_package("pandas", "2.0")),
        ("numpy", lambda: check_package("numpy", "1.24")),
        ("matplotlib", lambda: check_package("matplotlib", "3.7")),
        ("openpyxl", lambda: check_package("openpyxl", "3.1")),
        ("数据文件", check_data_file),
        ("Notebook", check_notebook),
        ("输出目录", check_output_dir),
        ("图表目录", check_charts_dir),
        ("Jupyter 内核", check_kernel),
    ]

    results: list[tuple[str, bool, str]] = []
    for name, func in checks:
        try:
            results.append((name, True, func()))
        except Exception as exc:  # noqa: BLE001 - 自检需要报告所有异常
            results.append((name, False, f"{type(exc).__name__}: {exc}"))

    width = max(len(name) for name, _, _ in results)
    print("环境自检报告")
    print("=" * 56)
    for name, ok, detail in results:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name:<{width}} : {detail}")
    print("=" * 56)

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        print(f"结果：{len(results) - len(failed)} 项通过，{len(failed)} 项失败")
        print("失败项：" + "、".join(failed))
        print("请先修复失败项，再运行 energy_analysis.py 或 Notebook。")
        raise SystemExit(1)

    print(f"结果：{len(results)} 项全部通过")
    print("环境正常，可以运行 energy_analysis.py 或 energy_analysis.ipynb。")


if __name__ == "__main__":
    main()
