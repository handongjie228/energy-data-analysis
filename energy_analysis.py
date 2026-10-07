"""兼容入口：复用 energy_all_in_one.py 的完整实现。

保留这个文件是为了兼容之前的运行方式：
    .venv\\Scripts\\python.exe energy_analysis.py --data data/我的数据.csv

所有分析逻辑、参数解析和图表代码都集中在 energy_all_in_one.py。
这样只需要维护一个文件，不会出现两份代码不同步的问题。
"""

from energy_all_in_one import main


if __name__ == "__main__":
    main()
