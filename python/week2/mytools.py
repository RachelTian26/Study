"""
mytools —— 我自己的通用小工具库（Day 13）

这个文件是我以后会一直复用的模块：
- 读写 JSON
- 安全转数字
- 输入控制
- 常见统计和评分
- 手机号码脱敏

照着 textstats.py 的结构来写：
    模块说明
    常量
    函数
    if __name__ == "__main__" 自测
"""

import json
from pathlib import Path

VERSION = "1.0"


def load_json(path, default=None):
    """读取 JSON 文件；文件不存在或内容损坏时返回默认值。"""
    path = Path(path)
    if not path.exists():
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def save_json(data, path):
    """把 Python 数据写成 JSON 文件，并保留中文可读性。"""
    path = Path(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def safe_int(text, default=0):
    """把字符串转成整数；转换失败时返回默认值。"""
    try:
        return int(str(text).strip())
    except (TypeError, ValueError):
        return default


def get_number(prompt, low, high):
    """反复要求用户输入，直到输入的是 low 到 high 之间的数字。"""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("请输入一个数字。")
            continue

        if low <= value <= high:
            return value

        print(f"输入必须在 {low} 到 {high} 之间，请重新输入。")


def average(numbers):
    """返回数字列表的平均值；空列表返回 0.0。"""
    if not numbers:
        return 0.0

    total = 0
    for num in numbers:
        total += float(num)
    return total / len(numbers)


def grade(score):
    """根据分数返回 A、B、C、D、F 等级。"""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"


def mask_phone(phone):
    """把手机号中间几位隐藏，保留前 3 位和后 4 位。"""
    text = str(phone).strip()

    if len(text) <= 4:
        return "*" * len(text)

    if len(text) <= 7:
        return text[:3] + "*" * (len(text) - 3)

    return text[:3] + "*" * (len(text) - 7) + text[-4:]


# ============================================================
# 这一段只在“直接运行 mytools.py”时执行。
# 其他文件 import mytools 时，不会执行这里。
# ============================================================
if __name__ == "__main__":
    demo_path = Path(__file__).with_name("mytools_demo.json")
    save_json({"name": "小明", "age": 18}, demo_path)
    print(f"mytools v{VERSION} 自测")
    print("load_json:", load_json(demo_path))
    print("safe_int:", safe_int(" 42 ", 0), safe_int("abc", 0))
    print("average:", average([80, 90, 100]))
    print("grade:", grade(88))
    print("mask_phone:", mask_phone("13800138000"))

    try:
        print("get_number 演示：")
        value = get_number("请输入一个 1 到 10 之间的数字：", 1, 10)
        print("你输入的是：", value)
    except EOFError:
        print("（没有输入内容，跳过交互演示）")

    if demo_path.exists():
        demo_path.unlink()
