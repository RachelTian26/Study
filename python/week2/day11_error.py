"""
Day 11 (08-11)  异常处理 try / except

今天的目标：会写 try/except，知道该捕获什么、更重要的是知道不该捕获什么。
教程：https://liaoxuefeng.com/books/python/function/error/index.html

前 10 天你见过的报错，今天开始能"接住"它们了。

但今天最重要的一句话是：**异常处理不是用来让报错消失的。**
它是用来"预料到的意外，给出体面的处理"。
不该接的错你接了，bug 会藏起来，之后debug会难十倍。
"""

from pathlib import Path

HERE = Path(__file__).parent
DATA = HERE / "data"

# ============================================================
# 读一读
# ============================================================

# --- 最基本的形状 ---
try:
    n = int("abc")            # 这行会炸
    print("这行永远不会执行")
except ValueError:
    print("转换失败，接住了")

print("程序还活着 ←重点在这")

# 没有 try 的话，程序会在报错那行直接终止，后面全都不执行。
# 有了 try，报错被接住，程序继续往下走。


# --- 认识常见的几种错，第 1 周你应该都见过 ---

# ValueError：类型对但值不对
try:
    int("12.5")
except ValueError as e:
    print("ValueError:", e)      # as e 把异常对象接下来，print 出来就是报错信息

# TypeError：类型不对
try:
    print("我今年" + 15 + "岁")   # Day 1 第 5 题那个错
except TypeError as e:
    print("TypeError:", e)

# KeyError：字典没这个键（Day 5 见过）
try:
    student = {"name": "小明"}
    print(student["phone"])
except KeyError as e:
    print("KeyError:", e)        # 注意打出来的是键名

# IndexError：列表越界
try:
    nums = [1, 2, 3]
    print(nums[10])
except IndexError as e:
    print("IndexError:", e)

# ZeroDivisionError：除以 0
try:
    print(10 / 0)
except ZeroDivisionError as e:
    print("ZeroDivisionError:", e)

# FileNotFoundError：文件不存在（Day 10 见过）
try:
    with open(DATA / "不存在.txt", encoding="utf-8") as f:
        f.read()
except FileNotFoundError as e:
    print("FileNotFoundError:", e)


# --- 一次接多种 ---
def safe_div(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("不能除以 0")
        return None
    except TypeError:
        print("参数得是数字")
        return None

print(safe_div(10, 2))
print(safe_div(10, 0))
print(safe_div(10, "x"))

# 几种错处理方式一样的话，写成元组：
try:
    value = int("abc")
except (ValueError, TypeError) as e:
    print("反正是转换问题：", e)


# --- 完整形状：try / except / else / finally ---
try:
    x = int("42")
except ValueError:
    print("except: 出错了才走这里")
else:
    print("else: 没出错才走这里，x =", x)
finally:
    print("finally: 不管出没出错都走这里")

# else 的用处：把"可能出错的那一句"和"成功之后要做的事"分开，
#   这样 try 里只放最小范围的代码，不会误接到别的错。
# finally 的用处：收尾（关文件、断开连接）。
#   with open() 其实就是帮你写好了 finally: f.close()


# --- ⚠️ 三个必须避免的写法 ---

# 反面教材 1：裸 except，什么都接
# try:
#     do_something()
# except:                        ← 千万别这么写
#     pass
# 为什么坏：连你打错变量名的 NameError、Ctrl+C 的 KeyboardInterrupt 都接了。
# 程序会"看起来在跑但什么都不对"，这是最难查的一类 bug。

# 反面教材 2：except Exception 然后 pass
# try:
#     risky()
# except Exception:
#     pass                       ← 错被吃掉了，一点痕迹都没留
# 至少要 print 一句，让你知道发生了什么。

# 反面教材 3：try 包得太大
# try:
#     data = load_file()          ← 想接的是这句的错
#     result = compute(data)      ← 但这句的 bug 也被接了，你会以为是文件问题
#     save(result)
# except Exception:
#     print("文件读取失败")        ← 提示信息还是错的，debug 时被彻底带偏
# 正确做法：try 里只放你真正预料会出错的那一两行。

# 那什么时候可以 except Exception？
#   写一个长时间运行的循环（比如菜单程序、服务器），不希望任何单次意外让整个程序退出。
#   但即使这种情况，也必须把错打出来：
def robust_loop_demo():
    for item in ["1", "2", "x", "4"]:
        try:
            print(int(item) * 10)
        except Exception as e:
            print(f"  处理 {item!r} 时出错（{type(e).__name__}: {e}），跳过继续")
            # {e!r} 里的 !r 是用 repr() 显示，字符串会带引号，看得更清楚
            # type(e).__name__ 拿到错误类型的名字，排查时很有用

robust_loop_demo()


# --- 主动抛错：raise ---
# 不是只有 Python 能抛错，你自己也能。
# 什么时候用：函数收到明显不合理的参数，早点炸掉比带着错误数据往下跑好得多。

def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"age 得是整数，你给的是 {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"age 得在 0-150 之间，你给的是 {age}")
    print(f"年龄设为 {age}")

set_age(15)

try:
    set_age(-5)
except ValueError as e:
    print("接住了：", e)

# 这叫 "fail fast"（尽早失败）。
# 你在 calendar-app 后端做的参数校验就是这个思路，只是那时候用的是返回 400。


# --- 自定义异常（够用就行）---
class ScoreError(Exception):
    """分数不合法。继承 Exception，一行就够，pass 或 docstring 都行。"""

def check_score(score):
    if not 0 <= score <= 100:
        raise ScoreError(f"分数 {score} 不在 0-100")
    return score

try:
    check_score(200)
except ScoreError as e:
    print("自定义异常：", e)

# 好处：调用方能精确地只接你这个错，不会跟别的 ValueError 混在一起。
# 什么时候值得写：项目变大、错误种类变多的时候。现在知道有这回事就行。


# --- EAFP：Python 的风格 ---
# 两种思路，Python 更偏爱后者：
#
#   LBYL (Look Before You Leap)  先检查再动手
#       if key in d and d[key] != 0 and ...:
#
#   EAFP (Easier to Ask Forgiveness than Permission)  先动手，错了再说
#       try: use(d[key])
#       except KeyError: ...
#
# 为什么 EAFP 常常更好：检查和使用之间状态可能变（文件被删了、别的线程改了），
# 而且条件多的时候 if 会写得又长又漏。
#
# 但也别过头 —— d.get(key, default) 明明更简单的地方就别上 try。

d = {"a": 1}
print(d.get("b", "默认值"))         # 这种场合用 .get() 就好，别写 try


# --- 今天最实用的一段：把 Day 7 的 get_score 升级 ---
#
# Day 7 你是这么写的：
#     if score.isdigit() and 0 <= int(score) <= 100:
#
# .isdigit() 的问题：
#     "12.5"  → False，但用户可能真想输 12.5
#     "-3"    → False，负号被当成非数字，错误提示会很莫名
#     " 90 "  → False，带空格就废了
#     全角"９０" → 居然是 True，然后 int() 会炸
#
# try/except 版本：

def get_number(prompt, low=0, high=100):
    """读一个 low~high 之间的数字，直到合法。返回 float。"""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)            # 用 float 就能接受 12.5
        except ValueError:
            print(f"  {raw!r} 不是数字，再来一次")
            continue
        if not low <= value <= high:
            print(f"  要在 {low}-{high} 之间")
            continue
        return value

# 想试的话取消下面这行的注释（会等你输入）：
# print(get_number("输入分数："))

# 对比一下就能看出 try/except 的价值：
#   它不问"这个字符串长得像数字吗"，而是直接问"能不能转成数字"。
#   后者才是你真正关心的问题。


# ============================================================
# 练一练
# ============================================================

# --- 第 1 题 ---
# 写一个函数 safe_int(text, default=0)：
#   能转成整数就返回整数，不能就返回 default，不要让程序崩
# 用这个列表测试，把能转的都转出来：
raw_data = ["12", "abc", "", "  34  ", "5.6", "-7", None, "0"]
# 注意 None 会引发 TypeError 而不是 ValueError，两个都要接
# TODO


# --- 第 2 题 ---
# 把 Day 7 的 get_score() 用 try/except 重写一遍，要求：
#   接受小数（89.5 是合法分数）
#   接受前后有空格的输入
#   拒绝 0-100 之外的数，并说清是为什么被拒
#   用户按 Ctrl+C 时打印「已取消」而不是吐出一大堆红字
# 提示：Ctrl+C 的异常叫 KeyboardInterrupt
# TODO


# --- 第 3 题 ---
# 写一个函数 read_file_safe(path)：
#   文件存在就返回内容，不存在就打印提示并返回空字符串
# 分别用 data/notes.txt 和一个不存在的文件名测试
# 想一想：这里用 try/except 好，还是用 Day 10 的 path.exists() 好？为什么？
# TODO


# --- 第 4 题 ---
# 下面是一批"脏"用户数据，有的缺键、有的类型不对
users = [
    {"name": "小明", "age": 15},
    {"name": "小红"},                    # 没有 age
    {"name": "小刚", "age": "十六"},      # age 是中文
    {"age": 14},                         # 没有 name
    {"name": "小美", "age": 15.9},
]
# 请遍历输出「姓名 - 年龄」，缺失或非法的用默认值补上（姓名"未知"，年龄 0），
# 并统计一共有几条数据有问题
# 提示：缺键用 .get() 就够，不用 try；age 转数字才需要 try
# TODO


# --- 第 5 题 ---
# 回到 Day 10 第 4 题的 data/scores.csv，这次用 try/except 重写解析：
#   "小美" 那行的 abc     → 接住 ValueError，跳过并说明原因
#   "小强" 那行只有 3 段  → 接住 IndexError（或先判断长度），跳过并说明原因
#   空行                  → 跳过
# 最后输出成功解析了几行、跳过了几行，以及各科平均分。
#
# 对比一下 Day 10 用 .isdigit() 的版本，哪个写起来更顺、更不容易漏情况？
# TODO


# --- 第 6 题（挑战）---
# 写一个函数 parse_event(line)，把一行文本解析成事项字典：
#   输入 "2026-08-12|写作业|16:00|60"
#   输出 {"date": "2026-08-12", "title": "写作业", "startTime": "16:00", "duration": 60}
# 要求（用 raise 主动抛错，不要静悄悄返回 None）：
#   段数不对        → raise ValueError("字段数不对，需要 4 段")
#   duration 非数字 → raise ValueError("duration 必须是数字")
#   日期不是 3 段   → raise ValueError("日期格式应为 YYYY-MM-DD")
# 然后写一个循环，用下面这批数据测试，把成功的收集起来，失败的打印原因：
test_lines = [
    "2026-08-12|写作业|16:00|60",
    "2026-08-12|背单词|19:30",              # 缺一段
    "2026-08-13|打球|20:30|九十",            # duration 非数字
    "2026/08/13|物理实验|14:00|120",         # 日期分隔符不对
    "2026-08-14|整理房间||40",               # 没时间，这个应该算合法
]
# 这题是 Day 12 和 Day 14 的直接铺垫，认真做
# TODO


# ============================================================
# 自检
# ============================================================
# [ ] try/except/else/finally 各自什么时候执行？
# [ ] 为什么裸 except: 是坏写法？举一个它会害到你的例子
# [ ] except Exception as e 里的 e 是什么？怎么打出错误类型的名字？
# [ ] 什么时候该自己 raise，而不是返回 None 或 False？
# [ ] 为什么 try/except 比 .isdigit() 更适合验证数字输入？
# [ ] d[key] 和 d.get(key) 你什么时候会选 try/except 而不是 .get()？
