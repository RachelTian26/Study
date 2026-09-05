"""
Day 1 (08-01)  变量 · 数据类型 · 输出

今天的目标：会用 f-string 输出，搞清楚 int / float / str / bool 的区别和转换。
教程：https://liaoxuefeng.com/books/python/basic/io/index.html

怎么用这个文件：
  1. 先看「读一读」，按运行键跑一遍，把输出和代码对上
  2. 再做「练一练」，把 TODO 换成你的代码
  3. 每写完一题就运行一次，别写完全部才跑
"""

# ============================================================
# 读一读（跑一遍，理解每行在干什么）
# ============================================================

# Python 不用 let / const，直接赋值。也不用分号。
name = "小明"
age = 15
height = 1.72
is_student = True

# type() 能告诉你一个值是什么类型
print(type(name))        # <class 'str'>   字符串
print(type(age))         # <class 'int'>   整数
print(type(height))      # <class 'float'> 小数
print(type(is_student))  # <class 'bool'>  布尔（注意 True/False 首字母大写！JS 里是小写）

# f-string：字符串前面加 f，然后用 {} 塞变量进去
# 这就是 JS 的模板字符串 `${name}`，只是符号不同
print(f"{name}今年{age}岁，身高{height}米")

# {} 里可以直接算
print(f"明年{name}就{age + 1}岁了")

# :.2f 表示保留 2 位小数（很常用，记住它）
print(f"身高保留两位小数：{height:.2f}")

# 类型转换：input 拿到的都是字符串，要算数就得转
text = "100"
print(text + text)              # 100100  ← 字符串拼接！不是加法
print(int(text) + int(text))    # 200     ← 转成 int 才是加法


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 定义三个变量：你的名字、你的年级、你最喜欢的科目
# 然后用一行 f-string 输出：「我叫XXX，读9年级，最喜欢的科目是XXX」
# TODO
my_name = "rachel"
my_grade = 9
my_fav_sbj = "math"
print (f"我叫{my_name}, 读{my_grade}年级, 最喜欢的科目是{my_fav_sbj}")

# --- 第 2 题 ---
half_circumference = 7.5
pi = 3.14159
print(f"circle with radius of {half_circumference} has the area of {pi * half_circumference * half_circumference}")
# 一个圆的半径是 7.5，圆周率用 3.14159
# 算出面积并输出，保留 2 位小数
# 输出格式：「半径 7.5 的圆，面积是 176.71」
# 提示：面积 = π × r × r
# TODO
cricle_radius = 7.5
pi = 3.14159
cricle_area = pi * cricle_radius * cricle_radius
print(f"半径{cricle_radius}的圆, 面积是{cricle_area:.2f}")

# --- 第 3 题 ---
# 下面这行是字符串，不是数字
price = "45"
count = "3"
# 请输出总价（应该是 135，不是 "45453"）
# TODO
print(f"总价是{int(price) * int(count)}")

# --- 第 4 题 ---
# 一个数是 3.78
# 分别输出：转成 int 是多少、转成 str 之后的类型是什么
# 猜一下 int(3.78) 是 4 还是 3？先猜，再运行看答案
# TODO
print(f"int(3.78) 是 {int(3.78)}")
print(f"str(3.78) 的类型是 {type(str(3.78))}")

# --- 第 5 题（想一想）---
# 运行下面这行，看看报什么错，然后把它修好
# print("我今年" + 15 + "岁")
# 提示：错误信息里的 "str" 和 "int" 就是线索。有两种改法，都试试
# TODO
print("我今年" + str(15) + "岁")

# ============================================================
# 自检（都能答上再收工）
# ============================================================
# [ ] f-string 怎么写？前面加什么字母？ f
# [ ] True 和 true，Python 里哪个对？ True
# [ ] "3" + "4" 结果是什么？3 + 4 呢？ 34， 7
# [ ] {值:.2f} 是干什么的？ 保留两位小数
