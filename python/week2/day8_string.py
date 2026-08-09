"""
Day 8 (08-08)  字符串处理 · 格式化

今天的目标：split / join / strip / replace 用熟，f-string 的对齐和数字格式会查会用。
教程：https://liaoxuefeng.com/books/python/basic/str/index.html

为什么第 2 周从字符串开始：
    因为从明天起你要读文件、解析 JSON、处理用户输入 —— 拿到手的全是字符串。
    "把一坨字符串切成有用的数据"，这是后面每一天的地基。

第 1 周你已经用过 .split() 和 .isdigit()，今天把这一族方法补全。
"""

# ============================================================
# 读一读
# ============================================================

s = "Hello, Python"

# 字符串能当列表用：索引、切片、len，全都一样
print(s[0])         # H
print(s[-1])        # n
print(s[7:])        # Python
print(s[::-1])      # nohtyP ,olleH   反转
print(len(s))       # 13

# 但有一点根本不同：字符串不可变（immutable）
# s[0] = "h"        ← 取消注释会报 TypeError，认识这个错
# 想"改"字符串，只能生成一个新的：
s2 = "h" + s[1:]
print(s2)

# 这条规则贯穿今天所有方法：**它们都返回新字符串，不动原来的。**
name = "  Rachel  "
name.strip()                 # 这行等于白写，结果没人接
print(name)                  # 还是 "  Rachel  "
cleaned = name.strip()       # 要这样接住
print(f"[{cleaned}]")        # [Rachel]

# 对比一下 Day 4 的列表：
#     list.append() / list.sort()  → 直接改原列表，不返回
#     str.strip() / str.replace()  → 返回新的，原来的不变
# 这个区别很容易踩，记住"字符串方法必须接返回值"。


# --- strip：去两头的空白 ---
print(f"[{'  空格  '.strip()}]")        # [空格]
print(f"[{'xxhelloxx'.strip('x')}]")    # [hello]   也能指定去掉什么字符
print(f"[{'  左  '.lstrip()}]")         # 只去左边，rstrip 只去右边
# 最常用的场合：input() 和读文件，用户/文件里到处是多余空格和换行

# --- split：切成列表 ---
print("a,b,c".split(","))               # ['a', 'b', 'c']
print("2026-08-08".split("-"))          # ['2026', '08', '08']
print("hello world  hi".split())        # ['hello', 'world', 'hi']
#   ↑ 不给参数 = 按任意多个空白切，还会自动忽略首尾空白，读文本时最省事
print("a,b,c".split(",", 1))            # ['a', 'b,c']   只切第 1 个

# --- join：列表拼成字符串（split 的反操作）---
parts = ["2026", "08", "08"]
print("-".join(parts))                  # 2026-08-08
#   ↑ 写法有点反直觉：是"分隔符".join(列表)，不是列表.join(分隔符)
print(", ".join(["小明", "小红", "小刚"]))

# join 只能拼字符串，列表里有数字会报错：
nums = [1, 2, 3]
# print("-".join(nums))                 ← TypeError
print("-".join(str(n) for n in nums))   # 先转成字符串。这叫生成器表达式，跟列表推导式一个意思

# --- replace：替换 ---
print("我爱Java".replace("Java", "Python"))
print("a-b-c-d".replace("-", ""))        # 替换成空字符串 = 删掉
print("a-b-c-d".replace("-", "", 2))     # 只替换前 2 个

# --- 大小写 ---
print("Python".upper(), "Python".lower(), "hello world".title())
# .lower() 的经典用途：比较时忽略大小写
answer = "Yes"
print(answer.lower() == "yes")           # 用户输 Yes/YES/yes 都算对

# --- 查找和判断 ---
text = "今天要写数学作业"
print("数学" in text)                    # True    最常用，判断包含就用 in
print(text.find("数学"))                 # 4       找不到返回 -1
print(text.index("数学"))                # 4       找不到直接报错（Day 11 会用上这个区别）
print(text.count("作"))                  # 1
print("day8.py".startswith("day"))       # True
print("day8.py".endswith(".py"))         # True

# --- is 系列：判断字符串"长什么样" ---
print("123".isdigit())        # True
print("12.5".isdigit())       # False  ← 小数点不算数字！
print("-3".isdigit())         # False  ← 负号也不算！
print("abc".isalpha())        # True
print("   ".isspace())        # True
# Day 7 你用 .isdigit() 检查分数，它挡不住 "12.5" 和 "-3"。
# Day 11 学了 try/except 就有更好的办法了，今天先知道它的边界在哪。


# --- f-string 进阶：对齐和数字格式 ---
# Day 7 你已经用过 :>5 和 :.1f，把这一族补齐

print(f"[{'左':<8}]")         # 左对齐占 8 格
print(f"[{'右':>8}]")         # 右对齐
print(f"[{'中':^8}]")         # 居中
print(f"[{'填':*^8}]")        # 用 * 填充空位

print(f"{3.14159:.2f}")       # 3.14      保留 2 位小数
print(f"{1234567:,}")         # 1,234,567 千位分隔符
print(f"{0.856:.1%}")         # 85.6%     百分比
print(f"{255:b} {255:x}")     # 11111111 ff   二进制/十六进制
print(f"{42:>8.2f}")          # 宽度和小数位可以一起写

# 宽度也能用变量，写在 {} 里：
w = 10
print(f"[{'动态宽度':>{w}}]")

# 调试神器 =：把表达式原样打出来，比 print("x =", x) 省事
x = 42
print(f"{x = }")              # x = 42
print(f"{x * 2 = }")          # x * 2 = 84

# ⚠️ 中文对齐的坑（Day 7 你的成绩表就歪了）
# 终端里一个中文字占两格宽，但 Python 数的是"字符个数"，不是"显示宽度"
print(f"|{'姓名':<6}|{'分数':>6}|")
print(f"|{'小明':<6}|{'90':>6}|")
print(f"|{'abcd':<6}|{'90':>6}|")
# ↑ 三行的竖线对不齐。这不是你写错了，是终端的中文宽度问题。
# 解决办法（今天不用深究，知道有这回事就行）：
#   1. 表头也用中文，让每列中文字数一样，看起来就齐了
#   2. 或者装 wcwidth 库来算真实宽度
#   3. 或者干脆表头用英文

# --- 转义字符 ---
print("换\n行")                # \n 换行
print("制表\t符")              # \t 制表符（对齐用，但不如 f-string 可控）
print("双引号 \" 和反斜杠 \\")
print(r"原样输出 C:\new\table")  # 前面加 r = raw，\n \t 都不转义。写路径和正则时用

# --- 三引号：多行字符串 ---
menu = """
1 - 添加
2 - 查询
3 - 退出
"""
print(menu)
# 文件顶上的说明（docstring）就是三引号字符串，只是没人接收它

# --- 中文和编码（知道就行，不用背）---
zh = "你好"
b = zh.encode("utf-8")        # 字符串 → 字节
print(b)                      # b'\xe4\xbd\xa0\xe5\xa5\xbd'  一个中文占 3 字节
print(b.decode("utf-8"))      # 字节 → 字符串
print(len(zh), len(b))        # 2 6   len 数字符，字节数不一样
# 明天 open() 里要写 encoding="utf-8"，原因就在这。
# 不写的话，在有些电脑上读中文文件会变成乱码。


# --- 真实场景：解析一行文本 ---
# 这就是明天读文件时你要反复做的事
line = "  小明 , 90 , 85 , 78  \n"

parts = line.strip().split(",")              # 先去两头空白（含 \n），再切
print(parts)                                 # ['小明 ', ' 90 ', ' 85 ', ' 78'] ← 中间几段还带空格
parts = [p.strip() for p in parts]           # 列表推导式，每段都 strip 一遍
print(parts)                                 # ['小明', '90', '85', '78']

student_name = parts[0]
scores = [int(p) for p in parts[1:]]         # 后三段转成 int
print(student_name, scores, sum(scores))

# 上面这四行，今天的练习会让你反复写。记住这个套路：
#     strip() → split() → 每段再 strip() → 该转数字的转数字


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 下面是一行学生记录，格式是「姓名|语文|数学|英语」
record = "小红|88|92|95"
# 请解析它，输出：「小红 三科总分 275，平均 91.7」
# 要求：三科分数用列表推导式转成 int，不要写三次 int()
# TODO
records = record.split("|")
name = records[0]
ch = int(records[1])
math = int(records[2])
eng = int(records[3])
total = ch + math + eng
avg = total / 3
print(f"{name} 三科总分 {total}, 平均 {avg:.1f}")


# --- 第 2 题 ---
# 用户输入的名字乱七八糟，请统一成「首字母大写、没有多余空格」
messy_names = ["  rachel  ", "TOM", "  jerry", "aLiCe  "]
# 期望输出：['Rachel', 'Tom', 'Jerry', 'Alice']
# 提示：.strip() 和 .title() 可以连着写，一个列表推导式就够
# TODO
messy_names = ["  rachel  ", "TOM", "  jerry", "aLiCe  "]
cleaned_names = [name.strip().title() for name in messy_names]
print(cleaned_names)


# --- 第 3 题 ---
# 用「读一读」里的 menu 三引号字符串，或自己写一段英文文本，统计：
#   一共多少个单词、多少个不重复的单词、出现最多的单词是哪个
# 提示：单词统计的逻辑 Day 5/6 写过（用 .get(词, 0) + 1），这次先 .lower() 再统计
#      找"出现最多的"可以先假设第一个最多，再遍历比较
text = "Hello hello world hello Python is fun and fun is great"
words = text.lower().split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1

print("单词总数:", len(words))
print("不重复单词数:", len(counts))

most_word = ""
most_count = 0
for word, count in counts.items():
    if count > most_count:
        most_word = word
        most_count = count

print("出现最多的单词:", most_word, "次数:", most_count)


# --- 第 4 题 ---
# 手机号脱敏：把中间 4 位换成 ****
phone = "13800138000"
# 期望输出：138****8000
# 提示：切片取前 3 位和后 4 位，中间用字符串拼接
# 写成函数 mask_phone(phone)，这样任何号码都能用
# TODO
phone2 = "13912345678"
mask_phone = lambda phone: phone[:3] + "****" + phone[-4:]
print(mask_phone(phone))
print(mask_phone(phone2))

# --- 第 5 题 ---
# 打印一张对齐的小票，要求：
#   商品名左对齐，单价右对齐保留 2 位小数，数量右对齐
#   最后一行输出总价，用千位分隔符
items = [
    ("笔记本", 12.5, 3),
    ("钢笔", 45.0, 1),
    ("书包", 259.9, 1),
    ("橡皮", 1.5, 10),
]
# 期望大概长这样（数字对齐，商品名不用强求）：
#   笔记本        12.50 x  3 =    37.50
#   ...
#   合计: 375.40
# 提示：元组解包 for name, price, count in items
# TODO
items = [
    ("笔记本", 12.5, 3),
    ("钢笔", 45.0, 1),
    ("书包", 259.9, 1),
    ("橡皮", 1.5, 10),
]
total_price = 0
for name, price, count in items:
    item_total = price * count
    total_price += item_total
    print(f"{name:<10} {price:>6.2f} x {count:>3} = {item_total:>8.2f}")
print(f"合计: {total_price:,.2f}")

# --- 第 6 题（挑战）---
# 写两个函数：
#   to_slash_date(s)   把 "2026-08-08" 转成 "2026/08/08"
#   to_chinese_date(s) 把 "2026-08-08" 转成 "2026年8月8日"（注意月和日没有前导 0）
# 提示：split("-") 拆开，第二个函数要把 "08" 转成 8 再拼回去
# TODO
to_slash_date = "2026-08-08".replace("-", "/")
print(to_slash_date)
to_chinese_date = "2026-08-08".replace("-", "年", 1).replace("-", "月", 1) + "日"
print(to_chinese_date)

# --- 第 7 题（挑战）---
# 写一个函数 is_palindrome(s)，判断一句话是不是回文
#   要求：忽略大小写、忽略空格和标点
#   "A man, a plan, a canal: Panama"  → True
#   "hello"                            → False
# 提示：先过滤出字母（用 .isalpha() 配合列表推导式），转小写，再和自己的反转比
# TODO
example1 = "A man, a plan, a canal: Panama"
example2 = "hello"
def is_palindrome(s):
    filtered = ''.join([c.lower() for c in s if c.isalpha()])
    return filtered == filtered[::-1]

print(is_palindrome(example1))
print(is_palindrome(example2))

# ============================================================
# 自检
# ============================================================
# [ ] name.strip() 之后 name 变了吗？为什么？
# [ ] split() 不给参数和 split(" ") 有什么区别？
# [ ] 把 ["a","b"] 拼成 "a-b" 怎么写？列表里是数字怎么办？
# [ ] "12.5".isdigit() 是 True 还是 False？为什么这是个坑？
# [ ] {值:>8.2f} 里的 > 8 .2f 分别管什么？
# [ ] r"C:\new" 和 "C:\new" 打出来一样吗？
