"""
停课三周后的复习（第 19 课之前做）

怎么用：
    第一轮「猜输出」：先只看某一题的代码，在纸上写下你猜的输出，
                     再运行这一题对答案：
                         python3 review_after_break.py 3      ← 只跑第 3 题
                     猜错了别急着看下一题，先说出"我以为……其实……"。

    第二轮「凭记忆写」：在文件最下面，不许翻第 15、16 课的代码。

这个文件里的日期都是写死的，所以哪天跑输出都一样。
"""

import json
import sys
from datetime import date, timedelta


# ============================================================
# 第一轮：猜输出（每题 1~3 分钟，共 9 题）
# ============================================================

# --- 第 1 题：字典（第 5 课）---
def q1():
    scores = {"语文": 88, "数学": 95, "英语": 72}
    print(scores.get("物理", 0))
    #0
    print(len(scores))
    #3
    for subject, score in scores.items():
        if score < 80:
            print(subject)
            #英语


# --- 第 2 题：列表推导式（第 4 课；你的老弱项）---
def q2():
    nums = [3, 8, 1, 10, 6]
    big = [n * 2 for n in nums if n > 5]
    print(big)
    #[16,20,12]
    print(len(nums), len(big))
    # 5,3


# --- 第 3 题：print 还是 return（第 6 课；你的老弱项）---
def q3():
    def add(a, b):
        print(a + b)

    result = add(2, 3)
    print(result)
    #None


# --- 第 4 题：异常处理（第 11 课）---
def q4():
    def to_int(text):
        try:
            return int(text)
        except ValueError:
            return None

    print(to_int("42"), to_int("3.5"), to_int(" 7 "))
    # 42 None 7


# --- 第 5 题：JSON（第 12 课）---
def q5():
    data = {"name": "小明", "tags": ["数学"]}
    print(json.dumps(data))
    print(json.dumps(data, ensure_ascii=False))

    text = '{"num": 8}'
    d = json.loads(text)
    print(type(d), d["num"] + 1)


# --- 第 6 题：类和 __repr__（第 15 课）---
def q6():
    class Card:
        def __init__(self, word, meaning):
            self.word = word
            self.meaning = meaning

        def __repr__(self):
            return f"Card({self.word})"

    c = Card("apple", "苹果")
    print(c)
    #'Card(apple)'
    print(c.meaning)
    # '苹果'
    cards = [c, Card("cat", "猫")]
    print(cards)
    # ['Card(apple),Card(cat)']


# --- 第 7 题：可变默认参数（第 15 课的坑）---
def q7():
    class Box:
        def __init__(self, items=[]):
            self.items = items

        def add(self, x):
            self.items.append(x)

    a = Box()
    b = Box([])
    a.add("笔")
    print(b.items)


# --- 第 8 题：日期（第 16 课）---
def q8():
    learned = date(2026, 10, 11)        # 第 18 课学完的那天
    today = date(2026, 11, 1)           # 今天
    print((today - learned).days)
    print(learned + timedelta(days=14))
    print(date.fromisoformat("2026-09-05").month)


# --- 第 9 题：发给大模型的 messages（第 18 课）---
def q9():
    messages = [
        {"role": "system", "content": "你是 Python 老师，回答不超过三句话"},
        {"role": "user", "content": "什么是 self？"},
    ]
    print(len(messages))
    print(messages[1]["role"])
    print(messages[0]["content"])
    # 跑完再口头回答：
    #   1. 最外面的方括号是什么？里面每个花括号又是什么？
    #   2. system 和 user 分别是谁在说话？如果想让 AI 记得上一轮它自己说过的话，
    #      该往列表里加一条什么 role 的消息？


# ============================================================
# 第二轮：凭记忆写（15 分钟，不许翻第 15、16 课的代码）
# ============================================================
# 写一个 Lesson 类：
#   __init__(self, num, title, learned)   learned 是 "2026-10-11" 这样的字符串
#   days_since(self, today)               today 是 date 对象，返回学完到 today 过了几天
#   __repr__(self)                        返回 "第 18 课：用 Python 调方舟大模型（2026-10-11）"
#
# 写完把下面 4 行测试的 # 去掉，再运行：python3 review_after_break.py write
#   l18 = Lesson(18, "用 Python 调方舟大模型", "2026-10-11")
#   print(l18)
#   print(l18.days_since(date(2026, 11, 1)))
#   print([Lesson(15, "类和对象", "2026-09-05"), l18])
#
# 应该看到：
#   第 18 课：用 Python 调方舟大模型（2026-10-11）
#   21
#   [第 15 课：类和对象（2026-09-05）, 第 18 课：用 Python 调方舟大模型（2026-10-11）]
#
# 自查：
#   [ ] 字符串转成 date，是在 __init__ 里转一次，还是每次 days_since 都转？哪种好？
#   [ ] 第 3 行测试为什么能打印出好看的列表？靠的是哪个方法？
#   [ ] days_since 用的是 return 还是 print？（回看第 3 题）
#
# ★ 这个类下节课会直接搬进 coach.py，今天写的不会白写。


class Lesson:
    def __init__(self, num, title, learned):
        self.num = num
        self.title = title
        self.learned = date.fromisoformat(learned)

    def days_since(self, today):
        return (today - self.learned).days

    def __repr__(self):
        return f"第 {self.num} 课：{self.title}（{self.learned}）"


def write():
    l18 = Lesson(18, "用 Python 调方舟大模型", "2026-10-11")
    print(l18)
    print(l18.days_since(date(2026, 11, 1)))
    print([Lesson(15, "类和对象", "2026-09-05"), l18])


# ============================================================
# 下面这段只负责"按题号运行"，不用看懂
# ============================================================
QUESTIONS = {
    "1": q1, "2": q2, "3": q3, "4": q4, "5": q5,
    "6": q6, "7": q7, "8": q8, "9": q9, "write": write,
}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in QUESTIONS:
        QUESTIONS[sys.argv[1]]()
    else:
        print("用法：python3 review_after_break.py 题号")
        print("      题号是 1 到 9，或者 write")
