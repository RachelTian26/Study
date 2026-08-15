"""
Day 9 (08-09 周日)  轻松日：手感自测 + Codewars

今天没有新语法。目标是两件事：
    1. 摸清哪些东西你以为会了、其实写不出来（自测）
    2. 第一次看见"别人怎么写同一道题"（Codewars）

第二件事是今天真正的价值。你前 8 天只见过自己的代码和我的示范，
Codewars 会让你看到几十个人解同一道题 —— 你写 8 行，最高赞 1 行。
这种冲击是"手感"最快的来源，比再做 10 道题有用。

━━━ 今天怎么安排 2 小时 ━━━

    25 分钟   Part 0 从零重写 Day 7 的三个函数（新增，今天最硬的一段）
    25 分钟   Part 1 自测 10 题（关掉所有文件，默写）
    50 分钟   Part 2 Codewars 做 5 道 8kyu
    20 分钟   Part 3 回头看别人的解法，记下来

今天是轻松日，但**不是可选日**。四段都要做完。
"轻松"指的是不学新语法、脑子不用装新东西，不是指今天可以跳过。

如果时间实在不够（比如只有 40 分钟），按这个优先级砍：
    Part 0 必做  →  Part 1 必做  →  Part 2 减到 2 道  →  Part 3 只记 1 道
Part 0 和 Part 1 是今天的核心，它们决定后半周你该补什么。
"""


# ============================================================
# Part 0  从零重写（25 分钟）★ 今天最有用的一段
# ============================================================
#
# 规则：**新建一个空文件 week2/day9_rewrite.py，从零开始写。**
#       不许打开 day7_project.py，不许打开 day7_summary.md，不许复制粘贴。
#
# 重写 Day 7 的这三个函数（挑的都是有原因的）：
#
#   1) get_score(subject)
#      要求变了：这次要能接受小数（"87.5" 合法）和拒绝负数（"-3" 非法）。
#      Day 7 你用的 .isdigit() 这两件事都做不到。
#      提示：先想清楚 .isdigit() 为什么不行，再想别的办法。
#           float() 转不了会报错 —— 这正好是 Day 11 要学的东西，今天先感受一下难点在哪。
#           今天用别的办法绕过去也行，绕不过去就把问题记下来，Day 11 会给你正确工具。

def get_score(subject):
    while True:
        score_str = input(f"请输入{subject}成绩（0-100）：")
        try:
            score = float(score_str)
            if 0 <= score <= 100:
                return score
            else:
                print("分数必须在 0 到 100 之间，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个数字。")


#   2) grade(avg)
#      纯逻辑，应该 2 分钟写完。写不出来说明 elif 链还没熟。

def grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 80:
        return "B"
    elif avg >= 70:
        return "C"
    elif avg >= 60:
        return "D"
    else:
        return "F"

#   3) print_summary(students)
#      ⚠️ 这个 Day 7 你没写对 —— 需求要的是**全班统计**，你写的是又把每个人打印了一遍。
#      这次严格按需求来，输出三样东西：
#          共 N 人
#          各科平均：语文 89.0  数学 88.5  英语 86.5
#          总分最高：小红 (275)
#      提示：算各科平均要跨所有学生取同一个键。
#           找总分最高的，先假设第一个是最高，再遍历比较替换。
#           students 是空列表时不能崩（除以 0 会报 ZeroDivisionError）。
#
# 写完之后，用这份固定数据测（直接抄这段到你的新文件里）：
#
#     students = [
#         {"name": "小明", "chinese": 90, "math": 85, "english": 78},
#         {"name": "小红", "chinese": 88, "math": 92, "english": 95},
#     ]
#     print_summary(students)
#     print_summary([])          # 这行不能崩
#
# 全部写完、跑通之后，才去 diff 一下：
#
#     diff week2/day9_rewrite.py week1/day7_project.py
#
# 别急着看谁写得好。只看一件事：**哪个函数你这次写得比上次快、比上次干净？**
#
# 为什么要重写？
#   第 1 周你是"跟着提示写出来的"，那和"自己能写出来"是两回事。
#   隔一周从零再写一遍，才知道哪些是真的进了脑子。
#   这个动作 Day 30 还会再做一次整套 —— 今天先小规模练一下。

def print_summary(students):
    print("total student number is", len(students))

    max_score = 0
    max_student = ""
    chinese_sum = 0
    math_sum = 0
    english_sum = 0
    for student in students:
        total_score = 0
        total_score = (student["chinese"] + student["math"] + student["english"])
        chinese_sum += student["chinese"]
        math_sum += student["math"]
        english_sum += student["english"]
        print("max score "  , max_score)
        if total_score > max_score:
            max_score = total_score
            max_student = student["name"]

    print("chinese average score is", chinese_sum / len(students))
    print("math average score is", math_sum / len(students))
    print("english average score is", english_sum / len(students))
    print("max score and max student is "  , max_score, max_student)


students = [
    {"name": "小明", "chinese": 90, "math": 85, "english": 78},
    {"name": "小红", "chinese": 88, "math": 92, "english": 95},
]
print_summary(students)
# print_summary([])

# ============================================================
# Part 1  手感自测（30 分钟）
# ============================================================
#
# 规则：**关掉 week1/ 和 day8 的所有文件，不查资料。**
# 卡住超过 2 分钟就跳过，跳过本身就是有用的信息 —— 那里就是你的漏洞。
#
# 做完之后再去对答案，然后在下面每题后面标一个字：
#     顺 = 直接写出来了
#     卡 = 想了一会儿才写出来
#     漏 = 写不出来，得回去看
#
# "漏"的那几项，就是 Day 10-14 之前要补的。

# --- 1 --- 输入 5 个数字（用一行逗号分隔的输入），输出平均值和最大值
# （这是根 README 里第 1 周的验收标准第一条，必须会）
# TODO

# def average(numbers):
#     total = 0
#     for num in numbers:
#         total += int(num)
#     return total / len(numbers)

# input_numbers = input("请输入五个数字，用逗号分隔")
# parts = input_numbers.split(",")
# numbers = [float(p.strip()) for p in parts]

# if len(numbers) != 5:
#     print("请输入五个数字，用逗号分隔")
# else:
#     print("max number is", max(numbers))
#     print("average number is", average(numbers))


# --- 2 --- 把 [3, 7, 3, 1, 7, 9] 去重，保持第一次出现的顺序
# TODO
numbers = [3, 7, 3, 1, 7, 9]
result = []
for num in numbers:
    if num not in result:
        result.append(num)
print(result)

# --- 3 --- 用**列表推导式**做出 1-20 里所有偶数的平方
# （不许用 for + append。这是你第 1 周的弱项，今天专门练）
# TODO
numbers = 0
for num in range(1, 21):
    if num % 2 == 0:
        print ("num is ", num , num**2)

# --- 4 --- 统计 "the quick brown fox jumps over the lazy dog the end" 里每个词出现几次
# TODO
text = "the quick brown fox jumps over the lazy dog the end"
words = text.split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print(counts)


# --- 5 --- 把 {"数学": 92, "语文": 78, "英语": 85} 里分数最高的科目名找出来
# （Day 5 第 2 题你这里写出过 bug，看看今天能不能写对）
# TODO
score = {"数学": 92, "语文": 78, "英语": 85}
max_score = 0
max_subject = " "
for subject in score:
    print (score[subject])
    if score[subject] > max_score:
        max_score = score[subject]
        max_subject = subject
print (max_subject, max_score)

# --- 6 --- 写一个函数，接收一个列表，返回里面所有偶数的和。列表为空要返回 0，不能崩
# TODO
# def sumodd(numbers):
#     total = 0
#     for num in numbers:
#         if num % 2 == 0:
#             total += int(num)
#     return total


# input_numbers = input("请输入一组数字，用空格分开: ")
# parts = input_numbers.split(" ")
# numbers = [float(p.strip()) for p in parts]

# print("sum of odd number is", sumodd(numbers))


# --- 7 --- 把 "  2026-08-09  " 解析成三个整数 year, month, day
# TODO
date = "2026-08-09"
parts = date.split("-")
print(parts[0],"year",parts[1],"month",parts[2],"day")


# --- 8 --- 把 ["小明", "小红", "小刚"] 拼成 "小明、小红、小刚"
# TODO
names = ["小明", "小红", "小刚"]
result = "、".join(names)
print(result)

# --- 9 --- 打印一行，姓名左对齐占 8 格，分数右对齐占 5 格保留 1 位小数
# TODO


# --- 10 --- 下面这段代码有 3 个问题，不运行，先用眼睛找出来
#
#     def get_avg(scores):
#         sum = 0
#         for s in scores:
#             sum += s
#         return sum / len(scores)
#
#     result = get_avg([90, 85, 78])
#     print(f"平均分 {result}")
#
# 提示：一个是命名问题，一个是 print/return 问题，一个是"某种输入会崩"
# 三个都是你第 1 周真实犯过的。把你找到的写在下面注释里：
#
# 问题 1： 253行，”90, 85, 78“应该是scores
# 问题 2：
# 问题 3：
#
# 找完了再自己改对：
# TODO


# ============================================================
# Part 2  Codewars（60 分钟）
# ============================================================
"""
━━━ 注册 ━━━

1. 打开 https://www.codewars.com  → Sign up（GitHub 账号可以直接登）
2. 会让你先做一道入门题才能进站，语言选 **Python**
3. 进去之后左上角确认语言是 Python，不是 JavaScript

━━━ 怎么找 8kyu 的题 ━━━

kyu 是难度，**数字越大越简单**。8kyu 最简单，1kyu 最难。
你现在就做 8kyu，不要挑战自己，今天是轻松日。

    菜单 Kata → Search
    左侧筛选：Difficulty 勾 8 kyu，Language 勾 Python
    Sort by 选 Most Completed（做的人最多的，题目质量和翻译都最好）

从最上面开始往下做，做 5 道。8kyu 的题一般 3-10 分钟一道。

━━━ 界面怎么用 ━━━

    左边是题目描述，右边上半是你写代码的地方，下半是测试
    TEST      跑给你看的几个例子（跑通不代表过）
    ATTEMPT   跑完整测试（有隐藏用例，这个过了才算过）
    SUBMIT    提交，通过后才解锁"看别人的解法"

注意：Codewars 只让你**填一个函数**，不用自己写 input()。
     函数名和参数是题目给定的，别改。
     它要的是 return，不是 print —— 这刚好是你的弱项，正好练。

━━━ ⭐ 今天最重要的动作 ⭐ ━━━

**每道题 SUBMIT 之后，一定要点 Solutions 标签页看别人怎么写的。**

上面按赞数排序，第一个通常是最"Python"的写法。
你会经常看到自己写 8 行的东西人家 1 行。

看到看不懂的写法，两个选择：
    看得出大概意思 → 记到 Part 3，试着理解
    完全不懂       → 跳过，别纠结。有些是很偏的技巧，不值得现在学

⚠️ 一个提醒：**别为了"像高赞那样"去硬凑一行。**
   能读懂的 5 行 > 看不懂的 1 行。你现在的目标是认得出这些写法，不是马上会用。

━━━ 卡住了怎么办 ━━━

8kyu 卡住 10 分钟以上，八成是题目没读懂（英文题面），不是不会写。
把题目描述丢进翻译，或者直接看它给的测试用例 —— 用例比描述清楚。
"""


# ============================================================
# Part 3  抄回来（30 分钟）
# ============================================================
#
# 做完 5 道题，把每道题记在下面。格式：
#     题目名
#     你的解法
#     最高赞的解法
#     它比你的好在哪（如果确实更好）
#
# 这一段是今天唯一会留下来的东西，别省。
# 一个月后回头看这里，你能看出自己变了多少。


# --- 第 1 道 ---
# 题目名：
# 我的解法：
# TODO
#
# 高赞解法：
#
# 学到了：


# --- 第 2 道 ---
# 题目名：
# 我的解法：
# TODO
#
# 高赞解法：
#
# 学到了：


# --- 第 3 道 ---
# 题目名：
# 我的解法：
# TODO
#
# 高赞解法：
#
# 学到了：


# --- 第 4 道 ---
# 题目名：
# 我的解法：
# TODO
#
# 高赞解法：
#
# 学到了：


# --- 第 5 道 ---
# 题目名：
# 我的解法：
# TODO
#
# 高赞解法：
#
# 学到了：


# ============================================================
# 附录：高赞解法里常见的几个写法
# ============================================================
# 今天的目标是**认得出**，不是背下来。看到了能反应过来"哦这个我见过"就够了。
# 下面每一条都跑一遍，看输出。

nums = [3, 8, 1, 9, 4]
words = ["python", "go", "rust"]

# 1) 三元表达式 —— 你在 Day 5 用过 "✓" if done else "○"
n = 7
print("偶数" if n % 2 == 0 else "奇数")

# 2) 列表推导式带筛选 —— 8kyu 高赞解法里出现频率最高的东西
print([x for x in nums if x > 3])
print([x * 2 for x in nums if x % 2 == 1])

# 3) sum() 配生成器表达式 —— 不用先建列表，一步算完
print(sum(x for x in nums if x % 2 == 0))
print(sum(len(w) for w in words))

# 4) any() / all() —— "有没有一个" / "是不是全都"
print(any(x > 8 for x in nums))        # 有超过 8 的吗
print(all(x > 0 for x in nums))        # 全都是正数吗
# 这两个能把 5 行的 for + flag + break 变成 1 行，很值得会

# 5) 布尔值能当数字用（True 是 1，False 是 0）
print(sum(x > 3 for x in nums))        # 有几个大于 3 —— 数个数的常用技巧
print(True + True)                     # 2   有点怪，但确实是这样

# 6) 内置函数直接怼 —— 很多 8kyu 题的高赞答案就是一个内置函数
print(sum(nums), max(nums), min(nums), len(nums), sorted(nums))
print(abs(-5), round(3.7), sorted(words, key=len))

# 7) 字符串方法链着写
print("  Hello World  ".strip().lower().replace(" ", "-"))

# 8) 解包（unpacking）
a, b = 1, 2
a, b = b, a                            # 交换两个变量，不用临时变量
print(a, b)
first, *rest = nums                    # * 收走剩下所有的
print(first, rest)

# 9) enumerate / zip
for i, w in enumerate(words, start=1):
    print(f"{i}. {w}")

names = ["小明", "小红"]
scores = [90, 88]
for name, score in zip(names, scores):     # 两个列表一起遍历
    print(f"{name}: {score}")

# 10) in 判断，比一串 or 干净得多
ch = "e"
print(ch in "aeiou")                   # 判断元音，8kyu 常考
print(ch in ["a", "e", "i", "o", "u"])

# 顺便：这十条里你已经会 1、2、9 的一部分。
# 剩下的看眼熟就行，之后自然会用上。


# ============================================================
# 收工前（今天有交付物，别跳）
# ============================================================
#
# 1. 回到 Part 1，数一下几个"顺"、几个"卡"、几个"漏"
#
# 2. 写 week2/day9_summary.md，就四行，但要写具体：
#
#        顺 X 个 / 卡 X 个 / 漏 X 个
#        漏的是：（列出题号和知识点，比如"第 3 题，列表推导式"）
#        Part 0 重写：哪个函数比上周快了？哪个还是卡住了？
#        Codewars 哪个高赞解法最让你意外？（贴那行代码）
#
#    「漏」的那几项，回去翻对应那天的文件补 10 分钟。这是今天唯一的作业。
#
# 3. 提交今天的东西（这个习惯从今天开始）：
#
#        cd /Users/tian/Downloads/Study
#        git add python/
#        git commit -m "week2 day9: 自测 + 重写 day7 三个函数 + Codewars 5 道"
#
#    你从 Day 7 之后就没提交过了，week2 全部还没进 git。
#
# 明天开始文件读写，第 2 周后半段比前半段硬。
