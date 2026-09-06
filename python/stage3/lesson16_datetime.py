"""
第 16 课  datetime 时间处理

文档：https://docs.python.org/zh-cn/3/library/datetime.html
速查：https://www.runoob.com/python3/python3-date-time.html

「读一读」里的输出都是实测的。
为了让你能对得上，例子里的日期我全部写死成 2026-08-29，
只有 3.2 那一处用了 now()，那个每次跑都不一样，已经标出来了。
"""

from datetime import date, datetime, timedelta

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】

    时间是每个真实程序都要碰的东西，也是最容易写错的东西。

    "两个日期差几天" 听起来像小学数学，但跨月、跨年、闰年、
    每月天数不同 —— 自己算一定会错。datetime 帮你算对。

【对用好 AI 的意义】★ 这节的重点

    日期是 AI 最不可靠的领域，没有之一。原因很实在：

        **AI 不知道今天几号。**

    它是在过去某个时间点训练出来的，之后就"停在那里"了。
    你问它"明天是几号"，它只能猜，而且经常猜得很自信。

    证据就在你自己的项目里 —— 打开 calendar-app/server/index.cjs，
    找到 AI 解析那段的 system prompt，你会看到这么一句：

        核心规则：
        - 今天是 ${today}，时区 ${tzStr}
        - 计算日期时，今天=${today}，"明天"=${today}的第二天

    当时这段是 AI 帮你写的，你可能没想过为什么要有这几行。
    现在你知道了：**不写这几行，"明天下午三点"就会被解析到一个随机的日期上。**

    这就是"把 AI 当零件"的第一课：
    **算术、日期、精确计数这类事，不要交给 AI —— 用 Python 算好，喂给它。**

【不学会的后果】

    第 19 课的工具核心逻辑是"挑一个你隔了足够久没复习的知识点"。
    这个"隔了多久"必须算准。算错了，工具要么天天考你刚学的（没用），
    要么永远想不起三周前那节（更没用）。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【一句话】

    时间有两种形态，你要一直清楚手里拿的是哪种：

        "2026-08-29"              字符串  → 给人看的，能存能打印，**不能算**
        date(2026, 8, 29)         对象    → 给程序算的，能加减能比大小

【生活里的例子】

    字符串像**照片上的时钟**：你能看清它显示几点，但你没法把指针拨快 10 分钟。
    datetime 对象像**真的时钟**：你能拨，拨完还能再拍张照片（转回字符串）。

    所以标准流程永远是这三步：

        从文件/用户/网络拿到字符串
              ↓  解析（拍照 → 真钟）
          datetime 对象
              ↓  在这里做所有的加减和比较
          datetime 对象
              ↓  格式化（真钟 → 拍照）
        字符串，存回文件或显示给人

    **所有计算都在中间那层做。** 两头都是字符串，中间必须是对象。

【为什么不能直接拿字符串算】

    "2026-9-1" 和 "2026-08-29" 哪个晚？
    按字符串比：'9' > '0'，所以 Python 认为 "2026-9-1" 更大 —— 这次碰巧对了。

    再看："2026-9-1" 和 "2026-10-1" 哪个晚？
    按字符串比："2026-1..." 里的 '1' < '9'，Python 说 10 月**小于** 9 月。错了。

    这个坑很隐蔽，因为它在一年里大部分时候都碰巧是对的，
    只在跨到两位数月份时才错。3.7 会详细讲。
"""


# ============================================================
# 三、读一读
# ============================================================

# ---------- 3.1 三种类型 ----------

# date      只有年月日
# time      只有时分秒（很少单独用）
# datetime  年月日 + 时分秒，最常用

d = date(2026, 8, 29)
dt = datetime(2026, 8, 29, 15, 30, 0)

print(d)
# 输出：2026-08-29

print(dt)
# 输出：2026-08-29 15:30:00

# 各个部分都能单独取出来
print(dt.year, dt.month, dt.day, dt.hour, dt.minute)
# 输出：2026 8 29 15 30

print(dt.weekday())
# 输出：5        ← 星期几。★ 注意：周一是 0，周日是 6。所以 5 = 周六

print(dt.date(), dt.time())
# 输出：2026-08-29 15:30:00
#       ↑ 这是两个值：date 部分和 time 部分，print 用空格连起来了


# ---------- 3.2 现在几点 ----------

now = datetime.now()
print("=============")
print(now.isoformat())
today = date.today()

# ⚠ 这两行的输出每次跑都不一样，你看到的跟我不同是正常的
print(type(now).__name__, type(today).__name__)
# 输出：datetime date

# datetime.now() 拿到的是本机时区的时间。
# 时区是个大坑，但你现在的程序全在自己电脑上跑，可以先不管。
# 什么时候要管：程序上线到服务器（服务器常年 UTC，跟北京差 8 小时）。


# ---------- 3.3 对象 → 字符串：strftime ----------

# f = format，格式化出去
print(dt.strftime("%Y-%m-%d"))
# 输出：2026-08-29

print(dt.strftime("%Y年%m月%d日 %H:%M"))
# 输出：2026年08月29日 15:30

print(dt.strftime("%m/%d %H:%M"))
# 输出：08/29 15:30

# 常用格式符（记这几个就够）：
#   %Y  四位年 2026        %y  两位年 26
#   %m  两位月 08          %d  两位日 29
#   %H  24小时制 15        %I  12小时制 03
#   %M  分 30              %S  秒 00
#   %A  星期全称           %a  星期缩写
#
# 想不去掉前面的 0（8 而不是 08），macOS/Linux 上用 %-m %-d：
print(dt.strftime("%-m月%-d日"))
# 输出：8月29日
# ⚠ 这个写法在 Windows 上会报错，Windows 要用 %#m。不跨平台，知道就行。

# 还有一个更省事的：isoformat()，标准格式，存 JSON 首选
print(dt.isoformat())
# 输出：2026-08-29T15:30:00

print(d.isoformat())
# 输出：2026-08-29


# ---------- 3.4 字符串 → 对象：strptime ----------

# p = parse，解析进来。注意格式串要跟字符串**完全对得上**
s = "2026-08-29 15:30"
parsed = datetime.strptime(s, "%Y-%m-%d %H:%M")
print(parsed)
# 输出：2026-08-29 15:30:00

print(type(parsed).__name__)
# 输出：datetime

# 对不上就报错：
# datetime.strptime("2026/08/29", "%Y-%m-%d")
#   → ValueError: time data '2026/08/29' does not match format '%Y-%m-%d'
#     （字符串里是斜杠，格式串里是横杠）

# 反过来，从 isoformat 字符串还原有个专用的、更省事的方法：
print(datetime.fromisoformat("2026-08-29T15:30:00"))
# 输出：2026-08-29 15:30:00

print(date.fromisoformat("2026-08-29"))
# 输出：2026-08-29

# 【记法】两个方法名只差一个字母，很容易记混：
#     strFtime  → F = Format  = 出去，变成字符串
#     strPtime  → P = Parse   = 进来，变成对象


# ---------- 3.5 timedelta：时间的加减 ----------

# timedelta 表示"一段时长"，不是"某个时刻"
base = date(2026, 8, 29)

print(base + timedelta(days=1))
# 输出：2026-08-30

print(base + timedelta(days=7))
# 输出：2026-09-05        ← 自动跨月了，你不用管每月几天

print(base - timedelta(days=30))
# 输出：2026-07-30

# datetime 可以加小时、分钟
meeting = datetime(2026, 8, 29, 15, 30)
print(meeting + timedelta(hours=2, minutes=15))
# 输出：2026-08-29 17:45:00

# 跨天也自动处理
print(datetime(2026, 8, 29, 23, 30) + timedelta(hours=2))
# 输出：2026-08-30 01:30:00

# ⚠ timedelta 没有 months 和 years 参数！
#   因为"一个月"不是固定长度（28/29/30/31 天都可能）。
#   要加一个月得用第三方库 dateutil，或者自己处理。
#   timedelta(weeks=4) 是有的，但那是 28 天，不是"一个月"。


# ---------- 3.6 ★ 两个日期相减：这是工具的核心 ----------

learned = date(2026, 8, 15)      # 这节课是这天学的
today_ = date(2026, 8, 29)       # 今天

gap = today_ - learned
print(gap)
# 输出：14 days, 0:00:00

print(type(gap).__name__)
# 输出：timedelta

# 只要天数，用 .days
print(gap.days)
# 输出：14

# ★★ 这一行就是第 19 课"该不该复习"的判断依据

# 跨月也完全正确，这就是不自己算的理由：
print((date(2026, 9, 3) - date(2026, 8, 28)).days)
# 输出：6

# 跨年、闰年同理：
print((date(2025, 3, 1) - date(2025, 2, 28)).days)
# 输出：1        ← 2025 不是闰年

print((date(2024, 3, 1) - date(2024, 2, 28)).days)
# 输出：2        ← 2024 是闰年，中间多了 2 月 29 日
#
# 你要是自己写"天数差"的公式，闰年这种事迟早翻车。

# 负数也正常，表示未来
print((date(2026, 8, 20) - date(2026, 8, 29)).days)
# 输出：-9


# ---------- 3.7 ★ 坑：用字符串比日期 ----------

# ISO 格式（YYYY-MM-DD，补零）字符串比较**碰巧**是对的：
print("2026-08-29" < "2026-09-01")
# 输出：True        ← 对的

# 因为补了零，位数固定，逐字符比较正好等于按大小比较。
# 所以 ISO 格式排序可以直接 sort()，很方便。

# 但只要格式不规范，立刻就错：
print("2026-9-1" < "2026-10-1")
# 输出：False
#       ↑ 错！9 月明明早于 10 月。
#         原因：逐字符比到第 6 位，'9' 和 '1'，'9' 更大，就判 9月 > 10月

# 更常见的翻车姿势：跟用户输入的日期比
print("2026-8-29" < "2026-08-30")
# 输出：False
#       ↑ 错！比到第 6 位，'8' > '0'，就判 8-29 更晚

# 【结论】
#   要比较、要计算 → 一律先 strptime 成对象，别偷懒
#   只是存起来、排序、显示 → ISO 字符串很好用
#
# 判断标准：只要涉及"减"或"加"，就必须转成对象。


# ---------- 3.8 排序 ----------

dates = [date(2026, 9, 3), date(2026, 8, 15), date(2026, 8, 29)]
dates.sort()
print(dates)
# 输出：[datetime.date(2026, 8, 15), datetime.date(2026, 8, 29), datetime.date(2026, 9, 3)]
#       ↑ 列表里显示的是 repr 形式，比较啰嗦。想好看就自己格式化：

print([x.isoformat() for x in dates])
# 输出：['2026-08-15', '2026-08-29', '2026-09-03']
#       ↑ 顺手还债：这就是第 4 课欠的列表推导式，这个阶段要练到顺手

# 按日期给字典排序（第 19 课挑复习内容会用到这个套路）
lessons = [
    {"num": 8, "learned": "2026-08-15"},
    {"num": 12, "learned": "2026-08-22"},
    {"num": 5, "learned": "2026-08-08"},
]
lessons.sort(key=lambda x: x["learned"])
print([x["num"] for x in lessons])
# 输出：[5, 8, 12]
#
# 这里 ISO 字符串直接排序是安全的（格式统一、补了零）。
# 但如果要算"隔了几天"，还是得转成对象。


# ---------- 3.9 把它用起来：间隔复习 ----------

# 「艾宾浩斯遗忘曲线」的大意：学完之后，在第 1、2、4、7、15 天各复习一次，
# 间隔越拉越长，记得最牢。这就是第 19 课挑题目的算法。

INTERVALS = [1, 2, 4, 7, 15, 30]


def next_review(learned_on, review_count):
    """算下次该复习的日期。review_count 是已经复习过几次。"""
    if review_count >= len(INTERVALS):
        return None                      # 复习够了，出师
    return learned_on + timedelta(days=INTERVALS[review_count])


learned_on = date(2026, 8, 15)
print(next_review(learned_on, 0))
# 输出：2026-08-16

print(next_review(learned_on, 3))
# 输出：2026-08-22

print(next_review(learned_on, 99))
# 输出：None


def is_due(learned_on, review_count, today_):
    """今天该不该复习这个知识点。"""
    nxt = next_review(learned_on, review_count)
    if nxt is None:
        return False
    return today_ >= nxt


print(is_due(date(2026, 8, 15), 0, date(2026, 8, 29)))
# 输出：True        ← 8/16 就该复习了，拖到 8/29 早该考

print(is_due(date(2026, 8, 28), 0, date(2026, 8, 29)))
# 输出：True        ← 昨天学的，今天正好第 1 次复习

print(is_due(date(2026, 8, 29), 0, date(2026, 8, 29)))
# 输出：False       ← 今天刚学，不用急着考


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题（热身）---
# 写 days_since(iso_str)：
#   传入一个 "2026-08-15" 这样的字符串，返回距今天多少天（整数）
# 要求：内部必须先转成 date 对象再算，不许用字符串切片
# 测试：传今天的日期应该返回 0
# 提示：date.fromisoformat() 和 date.today()
# TODO

def days_since(iso_str):
    target_day = date.fromisoformat(iso_str)
    return (date.today() - target_day).days

print(days_since("2026-08-15"))
print(days_since(date.today().isoformat()))
# 输出：0   ← 传今天，返回 0

# --- 第 2 题 ---
# 写 friendly(iso_str)，把日期变成人话：
#   今天      → "今天"
#   昨天      → "昨天"
#   2-6 天前  → "3 天前"
#   7-29 天前 → "2 周前"      （除以 7 取整）
#   30 天以上 → "2026-08-15"  （太久了就直接显示日期）
#   未来的日期 → "还没到"
# 测试至少 5 个不同的输入。
# TODO
from datetime import date

def friendly(iso_str):
    target = date.fromisoformat(iso_str)
    today = date.today()
    delta = (today - target).days

    if delta < 0:
        return "还没到"
    if delta == 0:
        return "今天"
    if delta == 1:
        return "昨天"
    if 2 <= delta <= 6:
        return f"{delta} 天前"
    if 7 <= delta <= 29:
        return f"{delta // 7} 周前"
    return iso_str


# 测试
print(friendly(date.today().isoformat()))      # 今天
print(friendly("2026-09-05"))                   # 昨天
print(friendly("2026-09-03"))                   # 3 天前
print(friendly("2026-08-30"))                   # 1 周前
print(friendly("2026-08-01"))                   # 2026-08-01
print(friendly("2026-09-10"))   


# --- 第 3 题 ---
# 第 3.7 节说字符串比日期会错。自己造一个例子证明：
#   找两个日期，它们的字符串比较结果和真实的日期比较结果**相反**。
#   两种比较都打印出来。
# 不许直接抄我上面的例子，自己找一组。
# TODO
from datetime import datetime

def demo_reverse_compare():
    s1 = "2026-9-15"
    s2 = "2026-10-01"

    try:
        d1 = datetime.strptime(s1, "%Y-%m-%d").date()
        d2 = datetime.strptime(s2, "%Y-%m-%d").date()

        print("字符串比较：", s1 < s2)
        print("真实日期比较：", d1 < d2)

    except ValueError:
        print("日期格式不对，不能转换成 date 对象")


demo_reverse_compare()

# --- 第 4 题（工具用得上）---
# 写 parse_flexible(text)：
#   接受多种格式，都返回 date 对象，实在解析不了返回 None
#       "2026-08-29"   → date(2026, 8, 29)
#       "2026/08/29"   → date(2026, 8, 29)
#       "8月29日"       → date(今年, 8, 29)
#       "今天"          → 今天
#       "明天"          → 明天
#       "乱七八糟"       → None
# 提示：用 try/except ValueError 挨个试格式（第 11 课的东西）
# 提示：别用裸 except —— 你知道该接哪个错
# TODO
from datetime import date

def parse_flexible(text):
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    try:
        return date.fromisoformat(text.replace("/", "-"))
    except ValueError:
        pass

    return None

print(parse_flexible("2026-08-29"))
print(parse_flexible("2026/08/29"))
print(parse_flexible("乱七八糟"))

# --- 第 5 题（挑战，第 19 课直接会用）---
# 写 pick_review_lesson(lessons, today_)：
#   lessons 是一个列表，每项形如
#       {"num": 8, "title": "字符串", "learned": "2026-08-15", "reviews": 0}
#   返回今天最该复习的**那一节**（返回整个字典），没有该复习的返回 None
#
# 「最该」的定义你自己定，但要在注释里写清楚规则。参考思路：
#   · 先筛出所有 is_due 的
#   · 从中挑"逾期最久"的（应复习日期离今天最远的那个）
#   · 都不 due 就返回 None
#
# ★ 这题的重点不是语法，是**你能不能把一句人话规则翻译成代码**。
#   这也正是你以后向 AI 描述需求时最需要的能力 ——
#   说不清楚规则，AI 给你的东西一定不是你要的。
# TODO
def pick_review_lesson(lessons, today_):
    """
    规则：挑今天已经到期、且「到期日最早」（= 拖得最久）的那一节；
         一节都没到期就返回 None。
    """
    best = None          # 目前挑中的那节课
    best_due = None      # 它的到期日，用来跟后面的比

    for lesson in lessons:
        learned = date.fromisoformat(lesson["learned"])
        nxt = next_review(learned, lesson["reviews"])
        print(f"lesson {lesson['num']} learned {learned} reviews {lesson['reviews']} next {nxt}")
        if nxt is None:          # 复习次数用完了（间隔表走到头），毕业，不用再考
            continue
        if today_ < nxt:         # 还没到期，跳过
            continue

        # 到这儿说明这节课到期了。跟目前的擂主比一比
        if best_due is None or nxt < best_due:
            best = lesson
            best_due = nxt

    return best      # 一个都没到期的话，best 从头到尾就是 None


# 测试数据：固定住"今天"，这样输出永远一样，好对答案
TODAY = date(2026, 9, 6)

LESSONS = [
    {"num": 8,  "title": "字符串",   "learned": "2026-08-15", "reviews": 0},  # 到期日 08-16，逾期 21 天
    {"num": 12, "title": "JSON",     "learned": "2026-09-01", "reviews": 1},  # 到期日 09-03，逾期 3 天
    {"num": 16, "title": "datetime", "learned": "2026-09-06", "reviews": 0},  # 到期日 09-07，还没到
    {"num": 5,  "title": "字典",     "learned": "2026-08-11", "reviews": 6},  # 复习满了，毕业
]

print(pick_review_lesson(LESSONS, TODAY))
# 输出：{'num': 8, 'title': '字符串', 'learned': '2026-08-15', 'reviews': 0}

print(pick_review_lesson([LESSONS[2]], TODAY))   # 只留没到期的那节
# 输出：None

print(pick_review_lesson([], TODAY))             # 空列表
# 输出：None

# --- 第 6 题（挑战）---
# 3.5 说 timedelta 没有 months 参数。
# 那"三个月后"怎么算？查文档或问 AI，回答下面三个问题（写注释里）：
#   1. 为什么 timedelta 故意不支持 months？（想一想 1月31日 + 1个月 = ?）
#   2. 标准库里有办法吗？第三方库 dateutil 是怎么做的？
#   3. 如果让你自己实现"加一个月"，1月31日加一个月你会返回什么？为什么？
# 这题没有标准答案，考的是你对"模糊需求"的判断。
# TODO
answer = """
# 1. 因为"一个月"不是固定长度（28/29/30/31 天都可能），而 timedelta 是"固定时长"，
#    内部只存天/秒/微秒，能乘能除能比大小。timedelta(months=1) * 2 等于几天？答不上来。
#    1月31日 + 1个月 至少有四个说得通的答案：
#        2月28日（月末对月末）/ 3月3日（往后数31天）/ 3月1日（往后数28天）/ 报错
#    Python 的态度写在 Zen of Python 里："面对模糊，拒绝猜测的诱惑。"
#    宁可不提供，也不替你猜——猜错了你还不知道，比报错危险。
#    另一个硬理由：钳月末会让 1月31日+1月+1月(=3月28日) ≠ 1月31日+2月(=3月31日)，
#    连"加两次1等于加一次2"都不成立，放进 timedelta 会到处埋雷。
#
# 2. 标准库没有现成的"加一个月"，但给了块砖：calendar.monthrange(年, 月)
#    返回 (当月1号是周几, 当月天数)，闰年它自己算对。有了天数就能自己拼。
#    标准库把"查天数"这种客观的事包了，把"日号溢出怎么办"这种主观的事留给你。
#    ⚠ 别拿 timedelta(weeks=4) 当一个月：1月31日+4周碰巧等于2月28日，纯属巧合，换年就错。
#    dateutil 的 relativedelta(months=1)：保留日号，越界才钳到月末（1月31日 → 2月28日）。
#
# 3. 我的规则「月末对齐」：
#      · 先把年月推 n 个月，日号先不动
#      · 起点若是当月最后一天 → 结果取目标月的最后一天
#      · 否则保留日号；目标月没这个日号就钳到月末
#    验算：1月31日+1月=2月28日  1月30日+1月=2月28日
#          平年2月28日+1月=3月31日（28是月末）  闰年2月28日+1月=3月28日（29才是月末）
#
#    理由：1月31日 语义上是"月末"而不是"第31天"，加一个月加的是**位置**不是数字。
#    金融业管这叫 EOM 惯例（End-Of-Month），房租、利息、订阅都这么算。
#    好处：月末日期的加法可结合了——1月31日+1月+1月 == +2月 == 3月31日，dateutil 做不到。
#
#    我认下的三个代价：
#      · 平年/闰年 2月28日 结果差 3 天（因为"是不是月末"取决于年份）
#      · 1月29/30/31 号加完全撞成 2月28日，信息丢失，减不回去
#      · 非月末日期链式相加仍会漂：1月30日+1月+1月=3月31日，但 +2月=3月30日
#
#    API：只给 add_months(d, n) 一个函数，不加 eom=True/False 参数。
#    加参数等于把"你到底要哪种语义"原样甩回给调用方，他多半也不知道，随便填一个，
#    坑还在只是多了一层。与其提供两种都半懂的行为，不如提供一种写清楚了的行为。
#    真需要另一种语义时再加 add_months_strict()，名字直说，比布尔参数好读.


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑 ----------
"""
下面这段是我见过的、AI 真实写出来过的"计算天数差"。找出 3 个问题：

    def days_between(date1, date2):
        # date1, date2 格式如 "2026-08-15"
        y1 = int(date1[0:4])
        m1 = int(date1[5:7])
        d1 = int(date1[8:10])
        y2 = int(date2[0:4])
        m2 = int(date2[5:7])
        d2 = int(date2[8:10])
        return (y2 - y1) * 365 + (m2 - m1) * 30 + (d2 - d1)

先别问 AI，先自己动手：
    把这个函数抄下来跑一遍，跟 (date2 - date1).days 的结果对比。
    找三组输入，让它们的差值**越大越好**。

写下你找到的：
    1.
    2.
    3.
    我造出的最大误差是：____ 天，输入是 ____ 和 ____

【提示】想想这三种情况：
    · 跨月的时候（8月31日 → 9月1日，实际差 1 天，公式算出来差多少？）
    · 跨很多年的时候（365 天的误差会怎么累积？）
    · 字符串格式不是 "2026-08-15" 而是 "2026-8-15" 的时候

【为什么这个坑值得专门练】
    这段代码有个恶劣的特点：**它在大部分测试里是对的。**
    同一个月里的两个日期，它算得完全正确。你随手测两下，通过了，就用上了。
    然后在某个跨月的日子悄悄出错，而你根本不会去查这个"已经测过"的函数。

    AI 写出这种代码的概率不低，因为它"看起来是在认真计算"。
    **你的防线不是"看起来对不对"，是"我有没有拿边界情况试过"。**
"""

# ---------- 5.2 去问 ----------
"""
【模板 1 —— 亲手验证 AI 不知道今天几号】

    先问它：

        今天是几月几号？

    再问：

        我说今天是 2026 年 8 月 29 日。那么"下周三"是几月几号？

    观察两件事：
        · 第一问它是怎么回答的？说不知道，还是给了个具体日期？
        · 告诉它今天之后，第二问答对了吗？（自己用 Python 算一遍核对）

    ★ 这个实验做完，你就永远记住"日期要自己算好再喂给它"了。
      calendar-app 里那句"今天是 ${today}"，就是这个道理。

【模板 2 —— 让它讲清楚而不是给代码】

    不要给我代码。
    解释一下：为什么 Python 的 timedelta 有 days 和 weeks 参数，
    但故意没有 months 和 years？这个设计决定背后的取舍是什么？

【模板 3 —— 让它出题考你】

    我刚学完 Python 的 datetime：strftime、strptime、timedelta、日期相减。
    出 3 道有陷阱的题考我，重点考"容易想当然但其实是错的"地方。
    先只给题目，我答完你再给答案和讲解。

    ↑ 记住这个模板，第 20 课你的工具就是把它自动化。

【做完记在 summary 里】
    · 模板 1 的实验结果（AI 第一问是怎么回答的？）
    · 模板 3 里你答错的那道题，错在哪
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] strftime 和 strptime 哪个是"进来"哪个是"出去"？你用什么办法记住的？
# [ ] 为什么不能直接用字符串比较日期？举一个会出错的具体例子
# [ ] 那为什么 ISO 格式（2026-08-29）字符串排序又是安全的？
# [ ] 两个 date 相减得到什么类型？怎么拿到天数？
# [ ] timedelta 为什么没有 months 参数？
# [ ] AI 为什么算不准日期？你的程序里该怎么补这个洞？
# [ ] weekday() 里星期一是几？


if __name__ == "__main__":
    print("\n第 16 课「读一读」全部跑完。")
    print("往上翻做「练一练」，第 5 题是第 19 课要直接用的，别跳。")
