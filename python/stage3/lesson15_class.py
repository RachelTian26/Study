"""
第 15 课  类和对象

教程：https://liaoxuefeng.com/books/python/oop/index.html

这个文件里「读一读」的输出注释，全部是在你这台电脑上真跑出来的。
你敲完对不上，就是敲错了 —— 不用怀疑注释。
"""

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】

    字典能装数据，但装不了"规矩"。

    你用字典存一节课的信息：
        {"num": 8, "title": "字符串处理", "stuck": "split 的参数忘了"}

    问题来了 —— 谁保证每个字典都有 "stuck" 这个键？
    你在 100 行外写 lesson["stuk"]（少个 c），Python 不会拦你，
    它会在运行到那一行时才报 KeyError。

    类把"数据"和"关于这份数据的规矩"绑在一起：必须有哪些字段、
    字段怎么算出来、能对它做什么操作。规矩写在一个地方，不散落在 100 行里。

【对用好 AI 的意义】★ 这条更重要

    AI 写的 Python，只要超过 50 行，几乎一定会用类。

    也就是说：你读不懂类，就读不懂 AI 给你的任何一段像样的代码。
    你只能"看它跑起来了就行"，那正是你现在的天花板。

    而且类是 AI 最容易埋坑的地方 —— 本节「找坑」环节里那个可变默认参数，
    是 AI 生成代码里最经典的一个错，它写得又自然又好看，但是错的。

【不学会的后果】

    第 19 课的工具要同时处理三种东西：课、题目、答题记录。
    全用字典写，你的代码会长成这样：

        data["records"][3]["questions"][0]["user_answer"]

    这一行你三天后就看不懂了，改一个字段名要全文搜索。
    用类写，它长这样：

        record.questions[0].user_answer

    看起来只是好看一点。真正的区别是：打错字时，第一种要等到运行才炸，
    第二种编辑器当场就给你划红线。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【一句话】

    类 = 表格的模板     对象（实例）= 填好的一张表

【生活里的例子】

    学校发学生登记表。

    那张空白模板规定了：
        · 有哪几栏          → 姓名、学号、班级
        · 哪些必须填        → 姓名不能空
        · 有些栏是算出来的  → 年龄从出生日期算，不用手填
        · 能对它做什么      → 盖章、归档、打印

    模板只有一张，这就是「类」。
    全班 40 个人各填一张，这 40 张就是 40 个「对象」。

    每张表内容不同（张三 / 李四），但格式和规矩完全一样。
    这就是类的全部意义：**规矩写一次，用很多次。**

【self 是什么】

    最让人懵的就是 self。它其实特别简单：

        self = "这一张表"

    你在模板上写规则的时候，得有个词指代"正在填的这一张"。
    Python 用 self，JS 用 this，是同一件事。

        def 打印(self):
            print(self.姓名)      # 打印"这一张表"上的姓名

【跟 JS 对照】

    你在 JS 里见过 class，语法几乎一一对应：

        JavaScript                      Python
        class Dog {                     class Dog:
          constructor(name) {             def __init__(self, name):
            this.name = name;                 self.name = name
          }
          bark() {                        def bark(self):
            console.log(this.name);           print(self.name)
          }
        }
        const d = new Dog("旺财");      d = Dog("旺财")

    三个区别，记住就够了：
        1. Python 的构造函数叫 __init__，不叫 constructor
        2. this → self，而且 **必须手写成第一个参数**（这是 Python 最反直觉的一点）
        3. 不需要 new，直接 Dog("旺财")
"""


# ============================================================
# 三、读一读
# ============================================================

# ---------- 3.1 先看看不用类是什么样 ----------

# 用字典存两节课的信息
lesson_a = {"num": 8, "title": "字符串处理", "stuck": "split 的参数忘了"}
lesson_b = {"num": 12, "title": "JSON 读写", "stuck": ""}

print(lesson_a["title"])
# 输出：字符串处理

# 想知道"这节课我卡住了吗"，得每次都写一遍判断
print(bool(lesson_a["stuck"]), bool(lesson_b["stuck"]))
# 输出：True False

# 问题 1：打错键名，要等运行到这行才报错
# print(lesson_a["titel"])     ← KeyError: 'titel'

# 问题 2：新建一个字典时忘了某个键，也没人拦你
lesson_c = {"num": 5, "title": "字典"}       # 忘了 stuck
# print(lesson_c["stuck"])     ← KeyError: 'stuck'


# ---------- 3.2 最小的类 ----------

class Lesson:
    def __init__(self, num, title, stuck=""):
        # __init__ 在 Lesson(...) 被调用时自动执行
        # self 就是"正在创建的这一个对象"
        self.num = num
        self.title = title
        self.stuck = stuck


a = Lesson(8, "字符串处理", "split 的参数忘了")
b = Lesson(12, "JSON 读写")            # stuck 用默认值 ""

print(a.title)
# 输出：字符串处理

print(b.stuck == "")
# 输出：True

# 注意：调用时不用传 self，Python 自动把 a 塞进去
# 你写 Lesson(8, "字符串处理")，Python 执行的是 __init__(新对象, 8, "字符串处理")


# ---------- 3.3 方法：能对这份数据做什么 ----------

class Lesson2:
    def __init__(self, num, title, stuck=""):
        self.num = num
        self.title = title
        self.stuck = stuck

    def is_stuck(self):
        """这节课有没有卡住的地方。"""
        return self.stuck != ""

    def label(self):
        """给人看的一行标题。"""
        mark = "⚠" if self.is_stuck() else "✓"
        return f"{mark} 第 {self.num} 课 {self.title}"


a2 = Lesson2(8, "字符串处理", "split 的参数忘了")
b2 = Lesson2(12, "JSON 读写")

print(a2.is_stuck())
# 输出：True

print(a2.label())
# 输出：⚠ 第 8 课 字符串处理

print(b2.label())
# 输出：✓ 第 12 课 JSON 读写

# ★ 注意 label() 里面调用了 self.is_stuck()
#   方法之间可以互相调用，都要带 self.
#   忘了写 self. 会报 NameError: name 'is_stuck' is not defined

# ★★ 还债提醒：第 6 课你写 fizzbuzz 时 print 和 return 混用了。
#    这里再说一遍这条规矩：
#        label()     负责"算出"一个字符串 → 用 return
#        谁要显示它   谁自己去 print
#    如果 label 里面直接 print，那你就永远没法把这个字符串写进文件了。


# ---------- 3.4 __repr__：让 print(对象) 好看 ----------

# 直接打印对象，默认长这样：
print(a2)
# 输出：<__main__.Lesson2 object at 0x102f3c710>
#       （后面那串地址每次运行都不一样，别对着抄）

# 加一个 __repr__ 就能自己决定它长什么样：

class Lesson3:
    def __init__(self, num, title, stuck=""):
        self.num = num
        self.title = title
        self.stuck = stuck

    def __repr__(self):
        return f"Lesson3(num={self.num}, title={self.title!r})"


c3 = Lesson3(8, "字符串处理")
print(c3)
# 输出：Lesson3(num=8, title='字符串处理')

# 放在列表里打印也自动变好看了：
print([Lesson3(8, "字符串"), Lesson3(12, "JSON")])
# 输出：[Lesson3(num=8, title='字符串'), Lesson3(num=12, title='JSON')]

# 前后带下划线的方法（__init__、__repr__）叫「魔术方法」，
# 特点是你不直接调用它，Python 在特定时刻自动调用。
# __repr__ 在 print(对象) 和在交互式命令行里显示时被调用。
#
# {self.title!r} 里的 !r 表示"用 repr 的方式显示"，
# 对字符串来说就是带上引号 —— 调试时能一眼看出这是个字符串。


# ---------- 3.5 类属性 vs 实例属性 ----------

class Question:
    # 类属性：写在 class 里、__init__ 外。所有对象共享同一份
    total = 0

    def __init__(self, text, answer):
        self.text = text            # 实例属性：每个对象自己一份
        self.answer = answer
        Question.total += 1         # 每造一个就加一


q1 = Question("strip() 干什么？", "去掉两头空白")
q2 = Question("split() 返回什么？", "列表")

print(q1.text)
# 输出：strip() 干什么？

print(Question.total)
# 输出：2

# 两个对象看到的是同一个 total
print(q1.total, q2.total)
# 输出：2 2


# ---------- 3.6 ★ 最重要的一个坑：可变默认参数 ----------

# 这是 AI 生成代码时最爱犯的错，也是本节「找坑」的主角。先自己看：

class BadRecord:
    def __init__(self, name, tags=[]):        # ← 这里有问题
        self.name = name
        self.tags = tags


r1 = BadRecord("第一条")
r1.tags.append("难")

r2 = BadRecord("第二条")        # 全新的对象，tags 应该是空的吧？
print(r2.tags)
# 输出：['难']
#       ↑ 第二个对象凭空多了一个标签！

print(r1.tags is r2.tags)
# 输出：True        ← 两个对象共用了同一个列表

# 【为什么】
#   默认值 [] 在「函数定义的那一刻」只创建一次，之后所有调用共用它。
#   不是每次调用都新建一个空列表 —— 这跟绝大多数人的直觉相反。
#
# 【正确写法】
class GoodRecord:
    def __init__(self, name, tags=None):
        self.name = name
        self.tags = tags if tags is not None else []


g1 = GoodRecord("第一条")
g1.tags.append("难")
g2 = GoodRecord("第二条")
print(g2.tags)
# 输出：[]

print(g1.tags is g2.tags)
# 输出：False

# 【记法】默认参数只能用不可变的东西：数字、字符串、True/False、None。
#        看到 =[] 或 ={} 出现在参数里，就是错的。没有例外。
#
# ruff 能抓这个（规则 B006）。装了 Ruff 扩展的话它会直接画波浪线。


# ---------- 3.7 什么时候用类，什么时候字典就够 ----------
"""
不是所有数据都值得写成类。判断标准就一条：

    这份数据有没有「行为」和「规矩」？

    只是搬运一下 → 用字典
        比如 json.load() 读进来直接又 dump 出去，中间不碰。

    有规矩、有算出来的字段、有操作 → 用类
        比如"这节课卡住了吗"、"该复习了吗"、"生成一行标题"。

第 19 课的三个类都属于后者：
    Lesson    要算"学了多少天了""该不该复习"
    Question  要算"答对没有"（不是简单的字符串相等）
    Record    要算"这次得分多少"

而从 AI 拿回来的原始 JSON，在转成 Question 对象之前，就是普通字典。
"字典进来 → 转成对象干活 → 转回字典存出去"是最常见的流程，第 19 课会写。
"""


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题（热身）---
# 写一个 Student 类：
#   __init__(self, name, scores)     scores 是一个分数列表
#   average(self)                    返回平均分，空列表返回 0（别让它崩）
#   best(self)                       返回最高分，空列表返回 None
#   __repr__(self)                   显示成 Student('小明', 平均 88.5)
# 造两个对象测试，其中一个 scores 传空列表。
# 提示：average 可以直接用 sum()/len()，但记得先判断空
# TODO

class Student2:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores

    def average(self):
        if not self.scores:
            return 0
        return sum(self.scores) / len(self.scores)

    def best(self):
        if not self.scores:
            return None
        return max(self.scores)

    def __repr__(self):
        return f"Student('{self.name}', 平均 {self.average()})"


s1 = Student2("小明", [90, 85, 88])
s2 = Student2("小红", [])

print(s1)
print(s1.average())
print(s1.best())
print(s2)
print(s2.average())
print(s2.best())

# 输出：
# Student('小明', 平均 87.66666666666667)
# 87.66666666666667
# 90
# Student('小红', 平均 0)
# 0
# None

# --- 第 2 题 ---
# 上一题的 __init__ 如果写成 def __init__(self, name, scores=[]) 会有什么后果？
# 不要只回答"会共享"——动手证明：
#   造 3 个不传 scores 的 Student，给第一个 append 一个分数，
#   然后打印另外两个的 scores。把你看到的结果写在下面注释里。
# TODO
# 我看到的结果：

class Student2:
    def __init__(self, name, scores=None):
        self.name = name
        self.scores = scores


s1 = Student2("小明", [90, 85, 88])
s2 = Student2("小红", [])
s3 = Student2("小华", [])
s4 = Student2("小李", [])

s1.scores.append(95)
print(s2.scores)
print(s3.scores)
print(s4.scores)

# --- 第 3 题（开始造工具了）---
# 写工具要用的 Lesson 类。这个类第 19 课会真的用上，认真写：
#
#   __init__(self, num, title, stuck="", path=None)
#       num    课号，整数
#       title  课的标题
#       stuck  「卡在哪」那段文字，可能是空字符串
#       path   这篇 summary 文件的路径，可能是 None
#
#   is_stuck(self)      stuck 非空返回 True
#   stage(self)         根据 num 返回 1/2/3/4
#                       1-7 → 1，8-14 → 2，15-20 → 3，21 以上 → 4
#   __repr__(self)      自己设计，要能一眼看出是第几课、叫什么
#
# 造 3 个对象测试，其中一个 num=15，确认 stage() 返回 3。
# TODO
class Lesson:
    def __init__(self, num, title, stuck="", path=None):
        self.num = num
        self.title = title
        self.stuck = stuck
        self.path = path

    def is_stuck(self):
        return self.stuck != ""

    def stage11(self):
        if 1 <= self.num <= 7:
            return 1
        elif 8 <= self.num <= 14:
            return 2
        elif 15 <= self.num <= 20:
            return 3
        else:
            return 4

    def __repr__(self):
        return f"Lesson(num={self.num}, title={self.title!r})"

print(Lesson(5, "字典"))
print(Lesson(15, "类和对象").stage11())


# --- 第 4 题 ---
# 写 Question 类：
#   __init__(self, text, answer, source_lesson)
#       text           题目
#       answer         参考答案
#       source_lesson  这题出自第几课
#
#   check(self, user_input)
#       判断用户答得对不对，返回 True / False
#       要求：忽略大小写、忽略两头空格
#       （提示：第 8 课的 strip() 和 lower()）
#
# 测试：答案是 "列表"，用户输入 "  列表  " 要判对。
#      答案是 "True"，用户输入 "true" 要判对。
# TODO

class Question:
    def __init__(self, text, answer, source_lesson):
        self.text = text
        self.answer = answer
        self.source_lesson = source_lesson

    def check(self, user_input):
        cleaned_user = str(user_input).strip().lower()
        cleaned_answer = str(self.answer).strip().lower()
        return cleaned_user == cleaned_answer


q1 = Question("什么是列表？", "列表", 8)
q2 = Question("Python 里布尔值怎么写？", "True", 8)

print(q1.check("  列表  "))
print(q2.check("true"))

# 输出：
# True
# True


# --- 第 5 题 ---
# 上一题的 check() 有个明显的局限：它只能判"一字不差"。
# 但实际上参考答案是"去掉两头空白"，用户答"删除首尾空格"，意思完全对。
#
# 不用写代码，回答两个问题（写在注释里）：
#   1. 你能想到哪些办法让判断更宽松？至少写两种
#   2. 这三种办法各有什么代价：关键词匹配 / 让 AI 判 / 改成选择题
# TODO
# 我的答案：
# 1. 让判断更宽松的方法：
#    - 关键词匹配：把“去掉两头空白”和“删除首尾空格”都视为同一类意思，
#      先把答案和用户输入都转成小写、去空格，再做词表匹配。比如把“删除”“去掉”“strip”“trim”
#      这些词看成近义词；还可以把“首尾”“两头”也归一。优点是快、简单；代价是会误判，
#      也需要维护很多同义词表。
#    - 让 AI 判：把用户答案和参考答案发给 AI，让它判断“意思是否一致”。优点是语义更灵活，
#      能理解“删除首尾空格”和“去掉两头空白”其实是一回事；代价是速度慢、成本高，
#      还可能风格化地“看人下菜”——有时候会过于宽松，或者胡乱放大解释。
#    - 改成选择题：题目直接给几个选项，用户选“去掉首尾空白”之类的选项，程序只需要比选项编号。
#      优点是最稳定、最容易判；代价是题目不够开放，减弱了“口头回答”的灵活性，
#      也更像考试而不是真实交流。
#
# 2. 三种办法的代价：
#    - 关键词匹配：最省资源，代码简单，但容易“看词不看意”，
#      例子：用户写“去掉前后空格”，如果词表没覆盖，可能判错。
#    - 让 AI 判：理解能力强，能看语义，但依赖模型、网络和成本，
#      也容易出现“看起来像对，但不是对”的边界问题。
#    - 改成选择题：最准确、最稳定，但灵活度最差，用户不能自由表达，
#      也不适合用来考“解释题”的语义理解。
#
# 结论：
#    如果是课堂练习，最实用的是“先做标准化清洗 + 关键词/同义词归一”；
#    如果是更真实的问答系统，才考虑让 AI 判断语义；
#    如果要绝对稳定，就改成选择题。


# --- 第 6 题（挑战）---
# 写 Record 类，记录一次答题：
#   __init__(self, lesson_num, questions)     questions 是 Question 对象的列表
#   add_answer(self, index, user_input)       记下第 index 题用户答了什么
#   score(self)                               返回 (答对数, 总题数)
#   summary(self)                             返回一行人话，比如 "第 8 课：2/3 对"
#
# 注意：用户的答案要存在哪？
#   存进 Question 对象里，还是 Record 自己开一个列表？
# 两种都能跑。选一种，并在注释里写清楚你为什么这么选 —— 这题考的是设计判断，不是语法。
# TODO
# 我的选择和理由：


# --- 第 7 题（挑战，为第 19 课热身）---
# 给 Lesson 类加一个方法 to_dict(self)，返回一个普通字典。
# 再加一个 from_dict，让它能从字典还原成 Lesson 对象。
#
# from_dict 有点特别，它要写成这样：
#
#     @classmethod
#     def from_dict(cls, d):
#         return cls(d["num"], d["title"], d.get("stuck", ""))
#
# 三个问题（查文档或问 AI，答案写注释里）：
#   1. @classmethod 是什么意思？它跟普通方法差在哪？
#   2. 为什么第一个参数是 cls 不是 self？
#   3. 为什么用 d.get("stuck", "") 而不是 d["stuck"]？
#
# 这一对方法是第 19 课存 JSON 的关键：对象不能直接 json.dump，字典可以。
# TODO


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑 ----------
"""
下面这段是典型的 AI 生成代码。它能跑，看起来还挺专业。
但里面有 4 个问题，找出来，写在下面的空里。

    class TodoItem:
        def __init__(self, title, tags=[], done=False):
            self.title = title
            self.tags = tags
            self.done = done

        def add_tag(self, tag):
            self.tags.append(tag)
            print(f"已添加标签 {tag}")

        def complete(self):
            self.done = True

        def get_info(self):
            print(f"{self.title} - {self.tags}")

提示，四个坑分别在这些方向：
    · 参数默认值（3.6 讲过，最严重的一个）
    · 有个方法该 return 却 print 了（第 6 课的老毛病）
    · 有个方法混了两件不该混的事
    · 少了一个 3.4 讲过的方法，导致调试时看不清对象

写下你找到的（找到几个写几个，找不全没关系，重要的是自己找）：
    1.
    2.
    3.
    4.

【找完再往下看】
把这段代码原样发给 AI，问："这段代码有什么问题？"
然后对比：
    · AI 找到的，你漏了哪些？
    · 你找到的，AI 漏了哪些？        ← 这个更有意思

我的经验是：AI 大概率能抓到 tags=[]，但经常不提 print/return 混用，
因为那不是"错误"，只是设计不好 —— AI 倾向于只报"错"，不报"不好"。
**它漏掉的那部分，就是你的价值。**
"""

# ---------- 5.2 去问 ----------
"""
今天用这三个模板去问 AI（网页版就行）。规则：**不许让它写代码。**

【模板 1 —— 要解释，不要答案】

    我在学 Python 的类。不要给我代码。
    用一个生活里的例子解释：为什么 self 必须手写成第一个参数，
    而 JavaScript 的 this 不用？
    解释完出一道判断题考我，先别给答案。

【模板 2 —— 让它反驳你】

    我的理解是："类就是能装函数的字典"。
    这个理解在什么情况下会让我犯错？举一个具体的例子。

    ↑ 这个模板很好用。AI 默认会顺着你说，你得主动要求它挑刺。

【模板 3 —— 挖它的边界】

    Python 里什么时候**不**应该用类？
    给我两个用字典更好的具体场景，并说明判断标准。

【做完记在 summary 里】
    · 哪个回答让你有"哦原来如此"的感觉
    · 有没有哪句你觉得 AI 在瞎编？去验证一下 —— 直接写代码跑
      （这一条最重要。AI 编起来非常自然，唯一的解药是你亲手跑一遍。）
"""


# ============================================================
# 六、自检
# ============================================================
# 答不上来就回去重读对应小节，别急着做第 16 课。
#
# [ ] self 是什么？为什么调用方法时不用传它，定义时却要写？
# [ ] __init__ 什么时候被调用？谁调用它？
# [ ] 类属性和实例属性的区别？举一个该用类属性的例子
# [ ] def __init__(self, tags=[]) 为什么是错的？错误会在什么时候暴露出来？
# [ ] __repr__ 有什么用？不写它会怎样？
# [ ] 什么时候该用类，什么时候字典就够了？说出你的判断标准
# [ ] 方法里调用同一个类的另一个方法，要怎么写？漏了会报什么错？


if __name__ == "__main__":
    print("\n第 15 课「读一读」全部跑完。")
    print("现在往上翻到「练一练」，那部分要你自己写。")
