"""
第 21 课  让电脑开口说话

今天你会做出三件事：
    1. 让电脑念出你的名字
    2. 换一个中文声音（婷婷）说一句话
    3. 把声音存成文件，双击就能听

这个阶段要拍一部科普小片。今天给剧组招第一个人：配音演员。
配音演员 = Mac 自带的 say 命令；Python = 导演，负责喊它干活。

标 🔊 的只有 2 处会出声；其它地方都存成文件，不会一直吵。
"""

import subprocess
from pathlib import Path

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】
    以前你的 Python 都是自己干活。
    今天开始，它能叫电脑里的其它程序干活，比如 say 配音、ffmpeg 剪视频。
    Python 不用真的会配音，会喊人就行。

【对用好 AI 的意义】
    以后让 AI 写“叫别的程序干活”的代码，你会经常看到 subprocess.run。
    学完今天，你能一眼看出命令有没有写对：要写成列表，不能拼成一长串文字。
    一长串文字遇到台词里的引号会坏，5.1 有真实例子。

【不学会的后果】
    第 22～27 课全都要用 subprocess.run 喊 say、ffprobe、ffmpeg。
    这一课不会，后面每一课都卡。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【用拍片来记】

    Python 不自己配音。它会像导演一样拿对讲机喊：
        "配音演员！用婷婷的声音！念：你好！"
    演员念完，回答："收到，没问题。"

    | 生活里（拍片剧组）            | 代码里                                     |
    |-------------------------------|--------------------------------------------|
    | 配音演员                     | Mac 自带的 say 命令                        |
    | 导演拿对讲机喊话             | subprocess.run(...)                         |
    | 一句话写成一格               | 列表：["say", "台词"]                      |
    | 演员交回成绩单               | returncode（0 = 没事，不是 0 = 出错）     |
    | 规定“出错必须大声报告”       | check=True                                  |

    两个名称先认识一下：
        subprocess   让 Python 启动另一个程序的工具。
        返回码       程序干完活交回的成绩单：0 是没事，不是 0 是出错了。

【哪里不像】
    真的对讲机，演员没听清还能再问一句。
    say 不会问。你喊错了，它要么报错，要么照着错的意思闷头做。
"""


# ============================================================
# 三、读一读
# ============================================================

NAME = "Rachel"           # ← 换成你的名字
HERE = Path(__file__).parent

# ---------- 3.1 先玩一下：让电脑念出你的名字 ----------

# subprocess.run(列表)：让 Python 叫另一个程序干活，干完再往下走
subprocess.run(["say", f"Hello, my name is {NAME}."])
print("配音演员说完了")
# 🔊 你会听到：Hello, my name is Rachel.
# 输出：配音演员说完了
#
# 这一行等于你在终端里敲：say "Hello, my name is Rachel."
# 注意：电脑说完这句后，才会出现下面的"配音演员说完了"。
# run 会一直等 say 说完，再继续运行。


# ---------- 3.2 命令写成列表：换声音、改语速、存成文件 ----------

# 一条命令要写成一个列表：每个词占一格。
#     终端里写：say  -v  Tingting  你好，我是婷婷。
#     列表里写：["say", "-v", "Tingting", "你好，我是婷婷。"]
cmd = ["say", "-v", "Tingting", "你好，我是婷婷。"]
print(cmd)
print("一共", len(cmd), "格")
# 输出：['say', '-v', 'Tingting', '你好，我是婷婷。']
# 输出：一共 4 格

subprocess.run(cmd)
# 🔊 你会听到：婷婷用中文说"你好，我是婷婷。"（这是全课最后一次出声）

# 台词里有空格也没关系，因为它整句放在同一格里。
#
# say 常用的三个开关（开关就是命令里带 - 的小选项）：
#     | 开关          | 意思                       | 例子             |
#     |---------------|----------------------------|------------------|
#     | -v 声音名     | 换哪个配音演员             | -v Tingting      |
#     | -r 数字       | 语速，数字越大念得越快     | -r 150           |
#     | -o 文件路径   | 不出声，把声音存成文件     | -o hello.aiff    |
#
# 开关和它的值要分两格："-v", "Tingting"，不能写成 "-v Tingting"。
# 想换声音，先在终端里查名单：say -v '?'
# -v 后面只写一个名字；带空格的名字要整格写，比如 ["-v", "Bad News"]。

# 先准备一个放文件的文件夹。这两行先照抄，第 22 课细讲。
OUT = HERE / "lesson_out" / "lesson21"
OUT.mkdir(parents=True, exist_ok=True)

hello_file = OUT / "hello.aiff"
subprocess.run(["say", "-v", "Tingting", "爸爸是坏人"])
subprocess.run(["say", "-v", "Tingting", "-r", "150", "-o", str(hello_file),
                "爸爸去吃饭不愿意教我了"])
print(hello_file.name, "存好了吗？", hello_file.exists())
# 输出：hello.aiff 存好了吗？ True

zh_file = OUT / "tingting.aiff"
subprocess.run(["say", "-v", "Tingting", "-o", str(zh_file), "今天是个好天气"])
print(zh_file.name, "存好了吗？", zh_file.exists())
# 输出：tingting.aiff 存好了吗？ True
#
# 去 stage4/lesson_out/lesson21/ 里双击这两个文件，就能听到。
# str(hello_file) 把路径变成文字，放进列表里才整齐。


# ---------- 3.3 返回码：演员交回来的成绩单 ----------

# run 干完会交回一张成绩单：returncode
# 0 = 没事，不是 0 = 出事了。
r = subprocess.run(["say", "-o", str(OUT / "ok.aiff"), "Everything is fine."])
print("正常的返回码:", r.returncode)
# 输出：正常的返回码: 0

# 故意把文件塞进一个不存在的文件夹，看看成绩单变成什么。
bad_file = OUT / "没有这个文件夹" / "bad.aiff"
r = subprocess.run(["say", "-o", str(bad_file), "This will fail."])
print("出错的返回码:", r.returncode)
# 屏幕上先冒出 say 自己的抱怨：Opening output file failed: wht?
# 输出：出错的返回码: 1
#
# 注意：出错了，Python 却没马上停。
# 默认情况下，导演（Python）没看成绩单，还以为一切正常。

# 一个意外：声音名写错（比如 "aaaa" 根本不在名单里），say 不报错，
# 自己悄悄换了一个声音去念。
r = subprocess.run(["say", "-v", "NoSuchVoice", "-o", str(OUT / "wrong_voice.aiff"), "Hello"])
print("声音名写错的返回码:", r.returncode)
# 输出：声音名写错的返回码: 0
#
# ★ 所以成绩单是 0，只代表"没报错"，不代表"做对了"。
#   想确认声音对不对，要自己听，或者到终端里查 say -v '?'。


# ---------- 3.4 check=True：出错必须大声报告 ----------

# check=True 就像导演加一条规定：
#     "成绩单不是 0，就马上停下来报错！"
# 错误的名字是 subprocess.CalledProcessError。
#
# 用第 11 课学过的 try/except 把错误接住，再打印一句人话：
try:
    subprocess.run(["say", "-o", str(bad_file), "This will fail."], check=True)
    print("存好了")
except subprocess.CalledProcessError as e:
    print(f"配音失败了，返回码是 {e.returncode}。先检查要存的文件夹在不在。")
# 屏幕上先冒出：Opening output file failed: wht?
# 输出：配音失败了，返回码是 1。先检查要存的文件夹在不在。
#
# 对比 3.3：
#   不加 check=True → 出错了也继续往后走，像什么事都没有。
#   加了 check=True → 出错就停下，交给 except 处理。
# 拍片时我们必须用后者：配音坏了还把后面的流程跑完，只会得到一段哑巴视频。


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题：念你想念的话（5 分钟） ---
# 改 3.1 那一行：让电脑念"Hello, I am 你的名字, and I am learning Python."
# 再换一个英文声音试试（比如 Daniel，英国口音）。
# 做完的样子：运行后听到你写的那句话，口音变了。
# 卡住了看这里：只要改列表里的台词那一格；换声音就在 "say" 后面加 "-v" 和声音名两格。
# TODO


# --- 第 2 题：认识剧组里的配音演员 ---
# 在终端（不是 Python）里敲：say -v '?'
# 它会列出这台电脑上所有声音。挑两个英文声音（en_US 或 en_GB）和一个中文声音（zh_CN），
# 在终端里各让它们说一句。把你最喜欢的那个声音名写在这里：
# 做完的样子：你能说出三个声音的名字，并且听过它们各自说话。
# 卡住了看这里：照着 3.2 开头那行注释的写法：say -v 声音名 台词
# 我最喜欢的声音：


# --- 第 3 题：新建 audio.py，写 speak() ---
# 在 stage4/ 下新建 audio.py，写一个函数：
#     speak(text, out_path, voice="Samantha")
#       text      要念的台词
#       out_path  存成哪个文件
#       voice     用哪个声音；不写就用 Samantha
# 要求：不出声、存成文件、用 check=True。
# 在 audio.py 底部试一次：存到 video_out/test.aiff。
# 做完的样子：stage4/video_out/ 里出现 test.aiff，双击能听到。
# 卡住了看这里：
#   · 把 3.2 存文件那一行里的台词、路径、声音名换成参数。
#   · video_out 要先存在：把 3.2 准备文件夹的两行抄过去，改个名。
#   · 路径用 HERE 拼，从哪个目录运行都不会找错。
# TODO（写在 audio.py 里，不是这里）


# --- 第 4 题：一次配 3 句 ---
# 在 audio.py 底部写 3 句你自己编的台词，用 for 循环调用 speak()，
# 存成 video_out/line1.aiff、line2.aiff、line3.aiff。
# 做完的样子：video_out/ 里多出 3 个文件，双击能听到三种台词。
# 卡住了看这里：文件名要跟着循环变。range(1, 4) 会给你 1、2、3，
#   再用 f-string 把数字拼进文件名。
# TODO（写在 audio.py 里）


# --- 第 5 题（挑战，可跳过）：出错时说人话 ---
# 故意把 out_path 指到一个不存在的文件夹，运行 speak()。
# 现在你会看到一屏红字。改 speak()，让它出错时只打印一句人话，比如：
#     ❌ 配音失败：存不进 xxx，检查文件夹在不在
# 做完的样子：没有红字，只有一句你写的提示。
# 卡住了看这里：3.4 就是答案的样子。想想 try 应该包住哪一行。
# 注意：别用"写错声音名"来制造错误，3.3 演示过，这台 Mac 上 say 不会报错。
# TODO（写在 audio.py 里）


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑：台词里有个撇号 ----------
"""
    命令还有一种偷懒写法：把整条命令拼成一长串文字，再加 shell=True。
    shell 像终端背后的"传话员"，它要先把这串文字按空格和引号拆开，再交给 say。

    很多 AI 和旧代码爱这样写，因为看起来跟终端里敲的一样。
    可台词里一旦有撇号（'），比如 It's，传话员就会以为"引号开始了"，
    一直找配对的那个引号，找不到，就罢工。
"""

line = "It's fine"
trap_file = OUT / "trap.aiff"

r = subprocess.run("say -o " + str(trap_file) + " " + line, shell=True)
print("字符串 + shell=True 的返回码:", r.returncode)
# 屏幕上先冒出两行：
#     /bin/sh: -c: line 0: unexpected EOF while looking for matching `''
#     /bin/sh: -c: line 1: syntax error: unexpected end of file
# 输出：字符串 + shell=True 的返回码: 2
#
# 人话：传话员说"我找不到跟 ' 配对的另一个引号"。

r = subprocess.run(["say", "-o", str(trap_file), line])
print("列表写法的返回码:", r.returncode)
# 输出：列表写法的返回码: 0

"""
    为什么列表就没事？
        列表         = 已经填好的点菜单：台词这一格写什么就是什么，没人再拆。
        字符串+shell = 口头传话，传话员重新拆句子，碰到引号、空格就可能拆错。

    ★ 记住：以后叫别的程序干活，一律用列表。
      看到 AI 写 shell=True，先想一句："它能改成列表吗？"
"""

# ---------- 5.2 去问 ----------
"""
【模板 1】
    我用 subprocess.run 传列表，和传字符串加 shell=True，区别是什么？
    用一个台词里有引号的例子说明，不要给我完整代码。

    ↑ 好在哪：给了一个具体例子（台词里有引号），AI 就不会只背定义；
      "不要给我完整代码"让它讲原理，代码你自己写。

【模板 2】
    我的 Python 用 subprocess.run(["say", "-o", 路径, 台词], check=True) 存音频，
    报错 CalledProcessError，returncode 是 1。可能是哪些原因？按可能性从大到小排，
    每条告诉我怎么在终端里单独验证。

    ↑ 好在哪：贴出了你的命令和返回码，还要它教你"怎么自己验证"，
      而不是直接猜一个答案让你去改。
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] 用剧组的话说：say 是谁？Python 是谁？subprocess.run 像什么？
# [ ] 把 say -v Daniel -o hi.aiff Hello there 写成列表：一共几格？每格是什么？
# [ ] 返回码 0 是什么意思？为什么声音名写错了，返回码还是 0？
# [ ] 不加 check=True，配音失败会怎样？加了 check=True 又会怎样？
# [ ] 用自己的话说：为什么 It's fine 用一长串文字会坏，用列表就没事？


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("第 21 课「读一读」跑完了。")
    print(f"今天你做到了：让电脑念出 {NAME}，换了婷婷的声音，还把声音存成了文件。")
    print("去 stage4/lesson_out/lesson21/ 双击 hello.aiff 听听看。")
    print("下一课：一次给整个剧本配音，再请场记拿秒表量出每句话有多长。")
