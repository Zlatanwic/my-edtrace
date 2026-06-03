"""edtrace 中文功能演示。

这是一个对照 examples.py 的中文版示例，用来演示 edtrace 的各项能力：
Markdown 文本、数学公式、图片、链接、Vega-Lite 图表，以及通过
@inspect / @clear / @stepover / @hide 指令观察程序执行过程中的变量。

运行方式（在 backend/src 目录下，源码读取依赖 UTF-8 修复）：
    PYTHONIOENCODING=utf-8 uv run --python 3.13 --with beautifulsoup4 \
        python -m edtrace.execute -m edtrace.examples_zh
生成的轨迹位于 var/traces/edtrace.examples_zh.json，在查看器中打开即可。
"""

import numpy as np
import torch
from dataclasses import dataclass
from .execute_util import text, image, link, plot, note


def main():
    展示文本()
    展示数值()
    展示图片与链接()
    展示图表()
    控制指令()


def 展示文本():
    text("# 一、文本与排版")
    text("edtrace 把每一次 `text(...)` 调用渲染成一行 Markdown，中文可以正常显示。")
    text("## 标题与强调")
    text("支持 **粗体**、*斜体*，以及行内代码 `for i in range(n)`。")
    text("## 无序列表")
    text("- 第一点：把 Python 程序当作讲义")
    text("- 第二点：边执行边展示变量")
    text("- 第三点：这一条特别长，用来验证当内容超出一行宽度时是否会自动换行，继续写一些字凑够长度")
    text("## 数学公式")
    text("行内公式 $a^2 + b^2 = c^2$，以及 softmax：$\\sigma(z)_i = \\frac{e^{z_i}}{\\sum_j e^{z_j}}$")
    text("一段被拆成多次调用的中文："), text("它们会"), text("拼接在同一行。")
    note("这是一条旁注（按 N 键切换显示），通常用于讲者备注。")
    text("下面这行源码会被隐藏，不出现在查看器里。")
    secret = "你看不到这行代码"  # @hide


def 展示数值():
    text("# 二、变量检查（@inspect）")
    text("在代码行末尾写注释指令 @inspect，右侧浮动面板会实时显示变量的值。")

    # NumPy 数组：不同 dtype
    向量 = np.array([1, 2, 3], dtype=np.int32)  # @inspect 向量
    矩阵 = np.zeros((2, 3))  # @inspect 矩阵

    # PyTorch 张量
    张量 = torch.tensor([[1.0, 2.0], [3.0, 4.0]])  # @inspect 张量

    # 列表与中文键的字典
    列表 = [1, 2, "三", [4, 5]]  # @inspect 列表
    字典 = {"姓名": "小明", "成绩": [90, 85, 100]}  # @inspect 字典

    # 数据类：类名与字段名都用中文
    @dataclass(frozen=True)
    class 学生:
        姓名: str
        成绩: list[int]
    某学生 = 学生(姓名="小红", 成绩=[88, 92])  # @inspect 某学生 某学生.姓名 某学生.成绩

    总分 = 累加(某学生.成绩)  # @inspect 总分 @stepover
    text("上面调用 `累加` 时使用了 @stepover，所以不会进入函数内部逐行追踪。")


def 累加(数列: list[int]) -> int:
    """对一个数列求和（被 @stepover 跳过内部细节）。"""
    结果 = 0
    for 元素 in 数列:
        结果 += 元素  # @inspect 结果
    return 结果


def 展示图片与链接():
    text("# 三、图片与链接")
    text("`image(url)` 可以展示本地或远程图片（此处演示本地图片）：")
    image("../../images/python-logo.png", width=200)
    text("`link(title=..., url=...)` 生成一个外部引用（鼠标悬停可看详情）：")
    link(title="edtrace 项目主页", url="https://github.com/percyliang/edtrace",
         organization="GitHub", description="一个把 Python 程序变成可执行讲义的工具。")
    text("`link(函数对象)` 生成跳转到源码的内部链接：")
    link(累加)


def 展示图表():
    text("# 四、图表（Vega-Lite）")
    text("`plot(spec)` 接收一个 Vega-Lite 规格，渲染成交互式图表：")
    规格 = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "各编程语言热度示例",
        "data": {"values": [
            {"语言": "Python", "热度": 95},
            {"语言": "JavaScript", "热度": 90},
            {"语言": "Rust", "热度": 72},
            {"语言": "Go", "热度": 65},
        ]},
        "mark": "bar",
        "encoding": {
            "x": {"field": "语言", "type": "nominal", "title": "编程语言"},
            "y": {"field": "热度", "type": "quantitative", "title": "热度"},
        },
    }
    plot(规格)


def 控制指令():
    text("# 五、@clear 指令")
    临时值 = 计算平方和(5)  # @inspect 临时值
    text("`临时值` 现在显示在面板里。")
    text("执行到下一行后，用 @clear 把它从面板移除。")  # @clear 临时值


def 计算平方和(n: int) -> int:
    总和 = 0
    for i in range(n):
        总和 += i * i  # @inspect i 总和
    return 总和


if __name__ == "__main__":
    main()
