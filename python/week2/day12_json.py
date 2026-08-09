"""
Day 12 (08-12)  JSON 读写

今天的目标：Python dict ↔ JSON 文件自由互转。
教程：https://liaoxuefeng.com/books/python/function/pickling/index.html

JSON 你比大多数初学者熟得多 —— calendar-app 的接口、方舟 API 的返回、
package.json，全是 JSON。今天只是学"在 Python 里怎么读写它"。

一句话总结今天：
    Day 10 你能把字符串存进文件，
    今天你能把**整个字典和列表**存进文件，读回来还是字典和列表。
    存到什么程度？程序关了再开，数据一模一样。
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"

# ============================================================
# 读一读
# ============================================================

# --- 四个函数，认准有没有 s ---
#
#   json.dumps(obj)      dict → 字符串        s = string
#   json.loads(text)     字符串 → dict
#   json.dump(obj, f)    dict → 文件         没有 s，跟文件打交道
#   json.load(f)         文件 → dict
#
# 记法：带 s 的跟字符串玩，不带 s 的跟文件玩。
#      dump 是往外写，load 是往里读。

event = {
    "id": "e1",
    "title": "写数学作业",
    "duration": 60,
    "done": False,
    "tags": ["study", "homework"],
    "note": None,
}

# --- dict → 字符串 ---
text = json.dumps(event)
print(text)
print(type(text))          # <class 'str'>  已经不是字典了

# 中文默认被转成 \uXXXX，能用但没法看：
print(json.dumps({"名字": "小明"}))                        # {"名字": ...}
print(json.dumps({"名字": "小明"}, ensure_ascii=False))     # {"名字": "小明"}  ← 中文必加

# 排版好看点（存文件时用，方便你自己打开看）：
print(json.dumps(event, ensure_ascii=False, indent=2))

# 所以存中文 JSON 的标准写法是这三个参数：
#     json.dumps(obj, ensure_ascii=False, indent=2)

# 键排序（想让文件 diff 稳定时有用）：
print(json.dumps({"b": 1, "a": 2}, sort_keys=True))


# --- 字符串 → dict ---
back = json.loads(text)
print(type(back), back["title"])
print(back == event)       # True   转过去再转回来，一模一样

# JSON 格式错了会抛 JSONDecodeError（它是 ValueError 的子类）：
bad = "{'title': '单引号不合法'}"      # JSON 只认双引号！
try:
    json.loads(bad)
except json.JSONDecodeError as e:
    print("JSON 解析失败：", e)
# ↑ 这个错你以后会经常遇到，尤其是拿到 AI 返回的"看起来像 JSON"的东西时。
#   Day 19 调方舟 API 就会碰上：模型有时会在 JSON 外面套一层 ```json 代码块。


# --- Python 和 JSON 的类型对照 ---
#   Python          JSON
#   dict         →  object    {}
#   list, tuple  →  array     []      ⚠️ 元组存进去会变成列表，读回来不是元组了
#   str          →  string
#   int, float   →  number
#   True/False   →  true/false        ⚠️ 大小写不一样
#   None         →  null              ⚠️ 名字不一样
#
# 这三个 ⚠️ 就是 Python 和 JS 写 JSON 的全部差异，你在 JS 那边写的是 true/null。

print(json.dumps({"t": (1, 2), "b": True, "n": None}))    # {"t": [1, 2], "b": true, "n": null}

# 不是所有东西都能转，比如日期对象：
from datetime import datetime
try:
    json.dumps({"now": datetime.now()})
except TypeError as e:
    print("存不了：", e)
# 解决办法：自己转成字符串再存。calendar-app 里 createdAt 存的就是字符串。
print(json.dumps({"now": datetime.now().isoformat()}))
# 字典的键也一样：JSON 的键只能是字符串，{1: "a"} 存进去键会变成 "1"
print(json.dumps({1: "a"}))        # {"1": "a"}  ← 读回来键是字符串了，这个坑要小心


# --- 从文件读：data/events.json ---
# 这份数据的结构照着你 calendar-app 的 events 表来的，字段名都一样

events_path = DATA / "events.json"

with open(events_path, encoding="utf-8") as f:
    events = json.load(f)          # 一句话，整个文件变成 Python 列表

print(f"读到 {len(events)} 条事项")
print(type(events), type(events[0]))       # list, dict

# 读出来就是普通的列表套字典，Day 4/5 学的全都能用：
for e in events:
    mark = "✓" if e["status"] == "done" else "○"
    print(f"{mark} {e['date']} {e['startTime'] or '(未定)':>5}  {e['title']}")
    #   ↑ e['startTime'] or '(未定)'：空字符串是 False，所以为空时用后面的值
    #     这个 or 技巧跟 JS 里一样

# 筛选、统计，全是列表推导式的活：
pending = [e for e in events if e["status"] == "pending"]
print(f"\n未完成 {len(pending)} 条")

total_min = sum(e["duration"] for e in events)
print(f"总时长 {total_min} 分钟 = {total_min / 60:.1f} 小时")

study = [e for e in events if e["activityType"] == "study"]
print(f"学习类 {len(study)} 条，共 {sum(e['duration'] for e in study)} 分钟")


# --- 按日期分组：字典套列表，很常用的套路 ---
by_date = {}
for e in events:
    by_date.setdefault(e["date"], []).append(e)
    #   ↑ setdefault(键, 默认值)：键不存在就先塞个空列表，然后 append
    #     等价于这三行：
    #         if e["date"] not in by_date:
    #             by_date[e["date"]] = []
    #         by_date[e["date"]].append(e)

for date in sorted(by_date):
    day_events = by_date[date]
    mins = sum(e["duration"] for e in day_events)
    print(f"{date}: {len(day_events)} 件事，{mins} 分钟")


# --- 写回文件 ---
out_path = HERE / "events_out.json"

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=2)

print(f"\n已写入 {out_path.name}，打开看看格式")

# 存 JSON 的标准写法，记住它，Day 14 和 Day 20 都要用：
#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)


# --- 封装成两个函数（这是今天最该带走的东西）---
# Day 14 的通讯录、Day 20 的待办工具，都会直接用这两个函数。

def load_json(path, default=None):
    """
    读 JSON 文件。文件不存在或内容坏了都返回 default，不抛错。

    为什么要这样设计：程序第一次运行时数据文件根本不存在，
    这不是"错误"，是正常情况，不该让程序崩。
    """
    path = Path(path)
    if not path.exists():
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"⚠️ {path.name} 格式坏了（{e}），用默认值")
        return default


def save_json(data, path):
    """写 JSON 文件，中文正常显示，缩进 2 格。"""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 试一下
demo_path = HERE / "demo.json"
save_json({"hello": "世界", "n": 42}, demo_path)
print(load_json(demo_path))
print(load_json(HERE / "根本没有这个文件.json", default={}))     # {}  没崩


# --- ⚠️ 一个真实会咬人的坑：写坏文件 ---
# save_json 如果在写的过程中崩了（断电、Ctrl+C），文件会只写一半，
# 下次 load 就 JSONDecodeError，数据全没了。
#
# 专业做法：先写临时文件，写成功了再替换原文件（叫"原子写入"）：
def save_json_safe(data, path):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)          # 替换是原子操作，要么成功要么原文件完好
    # 想一想：为什么这样就安全了？如果崩在 with 里面，原文件动过吗？

save_json_safe({"safe": True}, demo_path)
print(load_json(demo_path))
# 今天不要求你写这个，但 Day 14 存通讯录时可以用上，你的数据会更靠得住。


# ============================================================
# 练一练
# ============================================================

# 第 1-5 题都用 data/events.json，别改原文件（要写就写新文件）

# --- 第 1 题 ---
# 读 events.json，输出一份"日报"：
#   总共几件事、已完成几件、未完成几件、完成率（百分比，保留 1 位小数）
# 提示：完成率用 f"{已完成/总数:.1%}"
# TODO


# --- 第 2 题 ---
# 按 activityType 分组统计，输出每类有几件事、总共多少分钟，按时长从多到少排
# 期望大概是：
#   study  4 件  330 分钟
#   sport  1 件   90 分钟
#   life   1 件   40 分钟
# 提示：分组用上面的 setdefault 套路
# TODO


# --- 第 3 题 ---
# 把所有 pending 的事项挑出来，存成一个新文件 pending.json
# 存完再 load 回来，确认条数对得上（这一步是在验证"存得住"）
# TODO


# --- 第 4 题 ---
# 给 events 加一条新事项（自己编一件今天真要做的事），
# 要求 id 自动生成，不能跟已有的重复。
# 加完存成 events_new.json，原文件不动。
# 提示：id 现在是 "e1".."e6"，你可以数一下已有多少条然后 +1；
#      想一想这个办法在"中间删过事项"之后还对吗？
# TODO


# --- 第 5 题 ---
# 写一个函数 find_events(events, keyword)：
#   在 title 和 description 里模糊搜索关键词，返回匹配的列表
#   要求不区分大小写（搜 "python" 能找到 "学 Python"）
# 用 "python"、"作业"、"xyz" 分别测试
# 提示：keyword.lower() in title.lower()
# TODO


# --- 第 6 题 ---
# 把 Day 7 的成绩统计器数据改成 JSON 存储：
#   录入完存进 grades.json
#   下次运行先 load_json 读回来，能看到上次录的人，然后继续加
#   删掉 grades.json 再运行，程序应该正常启动（空列表开始），不能崩
# 直接用上面写好的 load_json / save_json
#
# 这题做完，你就完成了 Day 14 项目的核心机制。
# TODO


# --- 第 7 题（挑战）---
# 写一个函数 to_csv(events, path)，把 events 导出成 CSV 文件：
#   第一行是表头 date,title,startTime,duration,status
#   之后每行一条事项
# 然后写配套的 from_csv(path)，读回来变成列表套字典（duration 要转回 int）
# 用 to_csv 存了再 from_csv 读，对比一下和原来的 events 差在哪
# 提示：想一想如果 title 里本身有逗号会发生什么？（这就是 csv 模块存在的理由）
# TODO


# --- 第 8 题（挑战，跟你的项目连起来）---
# calendar-app 里事项有 recurrence（重复规则）和 reminders（提醒列表）字段。
# 设计一个 JSON 结构，能存"每周一三五 16:00 写作业，提前 10 分钟提醒"这件事，
# 写进 recurring.json，再写一个函数把它读出来，用中文描述一遍。
#
# 这题没有标准答案，重点是体会「设计数据结构」这件事 ——
# 你在 calendar-app 里是指挥 AI 做的，这次自己设计一遍。
# TODO


# ============================================================
# 自检
# ============================================================
# [ ] dumps / dump / loads / load 四个的区别？带 s 的是哪种？
# [ ] 存中文必须加什么参数？不加会怎样？
# [ ] Python 的 True / None 存成 JSON 是什么样？
# [ ] 元组存进 JSON 再读回来，还是元组吗？
# [ ] 为什么 load_json 要处理"文件不存在"？这算错误吗？
# [ ] JSON 里能用单引号吗？


# ============================================================
# 收尾
# ============================================================
# 今天开始，"数据存得住"这件事你已经会了。
# Day 14 的通讯录、Day 20 的待办工具，存储部分就是今天这两个函数。
# 建议把 load_json / save_json 抄进 Day 13 你自己的 mytools.py 里，之后随时 import。
