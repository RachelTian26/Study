"""
Day 5 (08-05)  字典 dict · 集合 set

今天的目标：会遍历 .items()，说清 .get() 和 [] 的区别。
教程：https://liaoxuefeng.com/books/python/basic/dict-set/index.html

dict 就是你在 calendar-app 里天天写的 JS 对象 / JSON。差别：
    JS   { name: "小明", age: 15 }
    Py   { "name": "小明", "age": 15 }   ← 键要加引号
"""

# ============================================================
# 读一读
# ============================================================

student = {
    "name": "小明",
    "age": 15,
    "grade": 9,
    "subjects": ["数学", "物理", "英语"]     # 值可以是任何东西，包括列表
}

# 取值
print(student["name"])

# 取不存在的键会直接报 KeyError 让程序崩掉
# print(student["phone"])        ← 取消注释试试，认识这个错误

# .get() 取不到不会崩，返回 None，还能指定默认值 ← 实际项目里用得更多
print(student.get("phone"))              # None
print(student.get("phone", "没填"))       # 没填

# 增 / 改：一样的写法，键不存在就是增，存在就是改
student["phone"] = "13800138000"
student["age"] = 16
print(student)

# 删
del student["phone"]
removed = student.pop("grade")        # 删掉并返回值
print(student, "删掉的是:", removed)

# 判断键在不在
print("name" in student)             # True（注意：查的是键，不是值）

# 三种遍历，都要会
for key in student:                          # 只要键
    print(key)

print("---")
for value in student.values():               # 只要值
    print(value)

print("---")
for key, value in student.items():           # 键值都要 ← 最常用
    print(f"{key} = {value}")

# 字典套列表套字典：真实数据长这样（跟你 calendar-app 的事项数据结构很像）
events = [
    {"title": "数学作业", "done": False, "minutes": 30},
    {"title": "背单词",   "done": True,  "minutes": 20},
    {"title": "物理实验", "done": False, "minutes": 60},
]

for e in events:
    mark = "✓" if e["done"] else "○"        # 三元表达式，JS 是 cond ? a : b
    print(f"{mark} {e['title']} ({e['minutes']}分钟)")
    # 注意：f-string 外面用双引号，里面就用单引号，别打架

# set 集合：不重复、无顺序。主要用来去重和判断存在
nums = [3, 7, 3, 1, 7, 9]
print(set(nums))            # {1, 3, 7, 9} 自动去重
print(list(set(nums)))      # 转回列表（顺序可能变，别依赖顺序）

a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a & b)     # {3, 4}          交集：都有的
print(a | b)     # {1,2,3,4,5,6}   并集：合起来
print(a - b)     # {1, 2}          差集：a 有 b 没有的
print(b - a)     # {5, 6}          差集：b 有 a 没有的
print(a ^ b)     # {1, 2, 5, 6}   对称差集：只在 a 或 b 的



# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 做一个字典存你自己的信息：名字、年级、身高、喜欢的科目（用列表）
# 然后用 .items() 遍历输出，每行一条
# TODO
Rachel = {
    "name": "Rachel",
    "grade": 9,
    "height": 1.65,
    "subjects": ["math", "english", "physics"]
}
for key, value in Rachel.items():
    print(f"{key} = {value}")

# --- 第 2 题 ---
scores = {"数学": 92, "语文": 78, "英语": 85, "物理": 96, "化学": 60}
# 输出：总分、平均分、最高的科目名字、所有低于 80 分的科目
# 提示：找最高科目可以先假设第一个是最高的，再遍历比较
# TODO
sum_scores = sum(scores.values())
avg = sum_scores / len(scores)
for subject, score in scores.items():
    if score == max(scores.values()):
        highest_subject = subject
    if score < 80:
        print(f"{subject}低于80分")
print(f"总分: {sum_scores}, 平均分: {avg:.2f}, 最高科目: {highest_subject}, 最低科目: {f'{subject}低于80分'}")



# --- 第 3 题 ---
text = "hello world hello python world hello"
# 统计每个单词出现了几次，输出成 {"hello": 3, "world": 2, "python": 1}
# 提示：text.split() 按空格切成列表；用 .get(词, 0) + 1 来计数
# 这是超经典的一道题，值得多花点时间
# TODO
words = text.split()
print(words)
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)

# --- 第 4 题 ---
# 用上面「读一读」里的 events 列表：
#   输出还没完成的事项有几个
#   输出所有事项的总时长
#   把"数学作业"标记成已完成，然后重新输出整个列表
# TODO
events = [
    {"title": "数学作业", "done": False, "minutes": 30},
    {"title": "背单词",   "done": True,  "minutes": 20},
    {"title": "物理实验", "done": False, "minutes": 60},
]
for e in events:
    if not e["done"]:
        print(f"未完成事项: {e['title']}")

total_minutes = 0
for e in events:    
    minutes = e["minutes"]
    total_minutes += minutes
print(f"总时长: {total_minutes}分钟")


for e in events:    
    if e["title"] == "数学作业":
        e["done"] = True    

print("更新后的事项列表:")
for e in events:
    mark = "✓" if e["done"] else "○"
    print(f"{mark} {e['title']} ({e['minutes']}分钟)")


# --- 第 5 题 ---
class_a = {"小明", "小红", "小刚", "小美"}
class_b = {"小刚", "小美", "小强", "小丽"}
# 用集合运算求出：
#   两个班都有的人
#   只在 A 班的人
#   两个班一共有多少不同的人
# TODO
print (class_a & class_b)
print (class_a - class_b)
different_people = class_a | class_b
print (len(different_people))


# --- 第 6 题（挑战）---
# 做一个简单通讯录（先存在内存里，下周学了文件就能存硬盘）：
#   用字典存 {名字: 电话}
#   写一个 while 循环菜单：1-添加 2-查询 3-删除 4-显示全部 5-退出
#   查询不到要友好提示，不要让程序崩
# 提示：这题是 Day 14 项目的预演，认真做
# TODO
contacts = []
contact = {"name": "Rachel", "phone": "13800138000"}
contacts.append(contact)
while True:
    print("1-添加 2-查询 3-删除 4-显示全部 5-退出")
    choice = input("请输入选项: ")
    if choice == "1":
        name = input("请输入名字: ")
        phone = input("请输入电话: ")
        contacts.append({name: phone})
        print(f"已添加联系人: {name} - {phone}")
    elif choice == "2":
        name = input("请输入要查询的名字: ")
        found = False
        for contact in contacts:
            if name in contact:
                print(f"{name} 的电话是: {contact[name]}")
                found = True
                break
        if not found:
            print(f"未找到联系人: {name}")
    elif choice == "3":
        name = input("请输入要删除的名字: ")
        found = False
        for contact in contacts:
            if name in contact:
                contacts.remove(contact)
                print(f"已删除联系人: {name}")
                found = True
                break
        if not found:
            print(f"未找到联系人: {name}")
    elif choice == "4":
        print("通讯录:")
        for contact in contacts:
            for name, phone in contact.items():
                print(f"{name} - {phone}")
    elif choice == "5":
        print("退出程序")
        break
    else:
        print("无效选项，请重新输入")

# ============================================================
# 自检
# ============================================================
# [ ] student["xxx"] 和 student.get("xxx") 键不存在时分别怎样？
# [ ] 同时拿键和值要用哪个方法？
# [ ] "name" in student 检查的是键还是值？
# [ ] 列表去重最快的写法？
# [ ] f-string 里面想用引号怎么办？
