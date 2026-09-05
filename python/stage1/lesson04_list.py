"""
Day 4 (08-04)  列表 list

今天的目标：增删改查 + 切片 + 遍历，全部不用查。
教程：https://liaoxuefeng.com/books/python/basic/list-tuple/index.html

list 就是 JavaScript 里的数组，方法名不同而已。对照着记会很快：
    JS push()    → Python append()
    JS length    → Python len()
    JS indexOf() → Python index()
    JS slice()   → Python [a:b]
"""

# ============================================================
# 读一读
# ============================================================

fruits = ["苹果", "香蕉", "橙子"]
print(fruits)
print(len(fruits))       # 3，长度是函数不是属性

# 取值：从 0 开始数
print(fruits[-3])         # 苹果
print(fruits[-1])        # 橙子 ← 负数从后往前数，-1 是最后一个（Python 特色，很好用）
print(fruits[-2])        # 香蕉

# 改值
fruits[1] = "葡萄"
print(fruits)            # ['苹果', '葡萄', '橙子']

# 加元素
fruits.append("西瓜")             # 加到末尾
fruits.insert(0, "草莓")          # 插到指定位置
print(fruits)

# 删元素
fruits.remove("葡萄")             # 按值删
last = fruits.pop()               # 删最后一个，并把它返回给你
del fruits[0]                     # 按位置删
print(fruits, "被pop出来的是:", last)

# 判断在不在
print("苹果" in fruits)           # True / False

# 切片 [起点:终点]，包含起点不含终点
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])      # [2, 3, 4]
print(nums[:3])       # [0, 1, 2]      省略起点 = 从头
print(nums[7:])       # [7, 8, 9]      省略终点 = 到尾
print(nums[::2])      # [0,2,4,6,8]    步长 2
print(nums[::-1])     # 整个倒过来 ← 记住这个，反转列表最快的写法

# 常用函数
print(len(nums), max(nums), min(nums), sum(nums))

# 排序：两种，区别很重要
scores = [88, 95, 70, 100, 63]
print(sorted(scores))         # 返回新的排好的列表，原来的不动
print(scores)                 # 还是原样
scores.sort()                 # 直接改原列表，不返回东西
print(scores)
scores.sort(reverse=True)     # 从大到小
print(scores)

# 遍历
for f in fruits:
    print(f)

# 要同时拿到位置和值，用 enumerate（很常用）
for i, f in enumerate(fruits):
    print(f"第 {i} 个是 {f}")

# 列表推导式：Python 的招牌写法，一行生成列表
squares = [x ** 2 for x in range(1, 6)]
print(squares)                # [1, 4, 9, 16, 25]

evens = [x for x in range(20) if x % 2 == 0]
print(evens)                  # 带筛选条件


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 建一个列表存 5 个你喜欢的东西，然后：
#   输出总共几个、第一个、最后一个
#   在中间插一个新的，再输出整个列表
# TODO
list = ["a", "b", "c", "d", "e"]
print(len(list), list[0], list[-1])

# --- 第 2 题 ---
nums2 = [23, 5, 78, 12, 90, 45, 3]
# 不用 max() / min() / sum()，用循环自己找出最大值、最小值、总和
# （能用现成函数当然更好，但自己写一遍才知道原理）
# TODO
max_num = float("-inf")
min_num = float("inf")
sum_num = 0
for num in nums2:
    if num > max_num:
        max_num = num
    if num < min_num:
        min_num = num
    sum_num += num
print(f"最大值是{max_num}, 最小值是{min_num}, 总和是{sum_num}")

# --- 第 3 题 ---
# 让用户输入 5 个数字存进列表，然后输出：
#   排序后的列表、平均分、比平均分高的有哪些
# TODO
text = input("请输入5个数字，用逗号分开: ")
parts = text.split(",")
print(parts)
numbers = [int(x) for x in parts]
numbers.sort()
avg = sum(numbers) / len(numbers)
above_avg = [x for x in numbers if x > avg]
print(f"排序后的列表: {numbers}, 平均分: {avg:.2f}, 比平均分高的有: {above_avg}")





# --- 第 4 题 ---
words = ["python", "java", "go", "rust", "javascript"]
# 用列表推导式做出：所有长度大于 3 的单词，并且全部转成大写
# 提示：字符串的 .upper() 方法
# TODO
upper_words = []
for word in words:
    if len(word) > 3:
        upper_words.append(word.upper())
print(upper_words)

# --- 第 5 题 ---
messy = [3, 7, 3, 1, 7, 9, 1, 3]
# 去掉重复的，得到 [3, 7, 1, 9]（顺序保持第一次出现的顺序）
# 提示：新建一个空列表，遍历原列表，用 in 判断要不要加进去
# TODO
non_duplicate = []
for num in messy:
    if num not in non_duplicate:
        non_duplicate.append(num)
print(non_duplicate)

# --- 第 6 题（挑战）---
# 把一个列表里的元素向右转一位：[1,2,3,4,5] → [5,1,2,3,4]
# 至少想出两种做法（切片能一行搞定，pop+insert 也行）
# TODO
lists = [1,2,3,4,5]
last = lists.pop()
lists.insert(0, last)
print(lists)

# ============================================================
# 自检
# ============================================================
# [ ] 取最后一个元素最简单的写法？last = nums[-1]
# [ ] nums[1:4] 包含第 4 个元素吗？nop
# [ ] sorted(x) 和 x.sort() 区别是什么？一个是返回新列表，一个是直接改原列表
# [ ] 怎么把列表反转？lists[::-1] 或者 lists.reverse()
# [ ] enumerate 是干什么的？用来同时获取列表元素的索引和值
