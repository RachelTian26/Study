"""
第 17 课  requests：让程序自己上网

文档：https://requests.readthedocs.io/zh_CN/latest/user/quickstart.html

这节课要真的联网，用的全是国内能直接访问的地址：
    百度                 https://www.baidu.com
    百度搜索建议          https://www.baidu.com/sugrec
    B 站视频信息          https://api.bilibili.com/x/web-interface/view
    Apifox 回声服务       https://echo.apifox.com     ← 你发什么它回什么，专门用来练手

「读一读」的输出我都实测过。但网络数据是活的：
    · 状态码、数据结构、字段名 —— 稳定，你会看到跟我一样的
    · 具体内容（搜索建议词、播放量）—— 每天都在变，不一样是正常的
我会标出哪些是会变的。

整个文件跑完大约 30 秒（十几个网络请求），别以为它卡住了。
"""

import requests

ECHO = "https://echo.apifox.com"

# 有些网站会拒绝"一看就是程序"的请求，得伪装成浏览器。3.3 会讲为什么
BROWSER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【对写 Python 的意义】

    到上一课为止，你的程序只能跟三样东西打交道：
    用户输入、自己电脑上的文件、代码里写死的数据。

    这一课之后，它能拿到**外面世界的数据**。

【对用好 AI 的意义】★ 这节的重点

    "接入 AI" 听起来很高级。今天你会看到它的真面目：

        **就是发一个 HTTP POST，把你的话放进 JSON 里，等它回一个 JSON。**

    跟查一个 B 站视频的播放量用的是同一套东西。没有魔法。

    想通这件事有个很实在的好处：以后 AI 调不通时，你会问对问题 ——
    是网络不通？key 错了（401）？调太频繁了（429）？还是我 JSON 拼错了（400）？
    不懂 HTTP 的人只能说"AI 用不了"，然后干等。

    另外，网络请求是 AI 写代码时最爱偷懒的地方：它写的 requests 调用，
    十次有八次不设 timeout。不设会怎样？**程序永远挂在那儿，不报错也不往下走。**
    这是本节「找坑」的主角。

【不学会的后果】

    第 18 课直接做不了。这两节是绑一起的：
    17 课学"怎么发请求"，18 课学"往哪发、发什么"。
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【一句话】

    requests 就是**程序版的浏览器地址栏**。
    你在浏览器敲网址回车，浏览器发一个请求、拿回一堆数据、画成页面。
    requests 做前两步，第三步交给你的代码。

【你已经会这个了，只是在 JS 里】

    calendar-app 里你写过 fetch。requests 是 Python 版，而且更省事：

        JavaScript                          Python
        ──────────────────────────────────────────────────────────
        const r = await fetch(url)          r = requests.get(url)
        const data = await r.json()         data = r.json()
        r.status                            r.status_code
        r.ok                                r.ok

        fetch(url, {                        requests.post(url,
          method: "POST",                       json={"a": 1},
          headers: {...},                       headers={...},
          body: JSON.stringify({a: 1})          timeout=10)
        })

    三个区别：
      1. **不用 await。** requests 是同步的 —— 代码停在那行等结果。
         简单很多，代价是等的时候程序干不了别的（现在不用管）。
      2. **不用两步。** fetch 要 await 两次（拿响应、解析 body），requests 一次到位。
      3. **不用手动 JSON.stringify。** 传 json={...}，它自动序列化并加好请求头。

【一个请求由四部分组成】

    点外卖的类比：

        URL      送到哪家店      https://api.bilibili.com/x/web-interface/view
        方法     干什么          GET = 我要看  /  POST = 我要交东西上去
        头       备注栏          "我是谁"（Authorization）、"我用的是啥浏览器"
        体       具体订单内容    只有 POST 才有，GET 没有体

【一个响应也有三部分】

        状态码   办成了没        200 成功 / 404 没这东西 / 401 你没权限
                                / 429 你太频繁 / 500 他们服务器崩了
        头       备注            返回的是什么格式、多大
        体       真正的数据      .text 拿原文，.json() 转成字典

【状态码只要记三档】

        2xx  成了
        4xx  **你**错了     （401 key 不对、404 地址不对、429 太频繁）
        5xx  **他们**错了   （服务器崩了，等一会重试往往就好）

    这个划分很实用：4xx 重试一万次也没用，得改代码；5xx 值得重试。
"""


# ============================================================
# 三、读一读
# ============================================================

# ---------- 3.1 最简单的 GET：访问百度 ----------

r = requests.get("https://www.baidu.com", timeout=10)

print(r.status_code)
# 输出：200

print(r.ok)
# 输出：True        ← status_code < 400 就是 True

print(r.headers["Content-Type"])
# 输出：text/html

# .text 是原始内容，这里是一整个网页的 HTML
print(r.text[:15])
# 输出：<!DOCTYPE html>

# ★ 百度首页返回的是网页，不是 JSON。所以 .json() 会炸：
try:
    r.json()
except requests.exceptions.JSONDecodeError as e:
    print("炸了:", str(e)[:38])
# 输出：炸了: Expecting value: line 1 column 1 (char

# 【记住这个报错长什么样】
#   "Expecting value: line 1 column 1" 的意思是"第一个字符就不对"。
#   90% 的情况不是数据坏了，而是**你请求到的压根不是 JSON** ——
#   可能是错误页、登录页、或者网址写错了。
#   遇到它，先 print(r.text[:200]) 看看到底拿回来了什么。


# ---------- 3.2 带参数的 GET：百度搜索建议 ----------

# 你在百度输入框打字时，下面弹出的联想词就是这个接口给的
r = requests.get(
    "https://www.baidu.com/sugrec",
    params={"prod": "pc", "wd": "python"},
    timeout=10,
)

print(r.status_code)
# 输出：200

data = r.json()
print(sorted(data.keys()))
# 输出：['g', 'p', 'q', 'queryid', 'slid']

print(data["q"])
# 输出：python        ← 回显你搜的词

# g 里面是联想出来的词
print([item["q"] for item in data["g"]][:3])
# 输出：['python怎么读', 'python干什么用的', 'python教程']
#       ⚠ 这三个词会随时间变，你看到的跟我不一样是正常的。
#         结构（有 g、每项有 q）是稳定的。

# ★ 顺手一提：这个接口的 Content-Type 是 text/plain，
#   但内容其实是 JSON。所以 **Content-Type 不能完全信**，
#   .json() 能不能成，得实际试。

# ❌ 别自己拼 URL：
#    url = "https://www.baidu.com/sugrec?wd=" + word     ← word 有空格或中文就坏

# ✅ 用 params，它自动转义。看看实际拼成了什么：
r2 = requests.get("https://www.baidu.com/sugrec",
                  params={"prod": "pc", "wd": "编程 入门"}, timeout=10)
print(r2.url)
# 输出：https://www.baidu.com/sugrec?prod=pc&wd=%E7%BC%96%E7%A8%8B+%E5%85%A5%E9%97%A8
#       ↑ 中文和空格都被转义了。这就是不能自己拼的原因


# ---------- 3.3 ★ 请求头：为什么有的网站不理你 ----------

# B 站的接口，不带任何头直接请求：
BILI = "https://api.bilibili.com/x/web-interface/view"

r = requests.get(BILI, params={"bvid": "BV1xx411c7mD"}, timeout=10)
print(r.status_code)
# 输出：412
#       ↑ 412 Precondition Failed。B 站看出你不是浏览器，直接拒绝

# 加上 User-Agent 伪装成 Chrome：
r = requests.get(BILI, params={"bvid": "BV1xx411c7mD"},
                 headers=BROWSER, timeout=10)
print(r.status_code)
# 输出：200

d = r.json()
print(d["data"]["title"], "|", d["data"]["owner"]["name"])
# 输出：字幕君交流场所 | 碧诗
#       （这是 B 站 av1，站上第一个视频。标题和 UP 主不会变，播放量会变）

print(type(d["data"]["stat"]["view"]).__name__)
# 输出：int        ← 播放量，具体数字每天都在涨

# 【User-Agent 是什么】
#   每个请求都会带的一个头，作用是"自我介绍"。
#   requests 默认报的是 "python-requests/2.34.2" —— 老实得过分，
#   很多网站看到就知道是程序，直接拦掉。
#
#   ⚠ 一句话提醒：伪装 UA 是为了正常读公开数据，不是为了绕过人家的限制。
#     接口有频率限制就老实等着，别写循环猛刷 —— IP 会被封，而且这是给别人添麻烦。


# ---------- 3.4 ★★ HTTP 200 不等于成功 ----------

# 查一个不存在的视频：
r = requests.get(BILI, params={"bvid": "BV1zzzzzzzzz"},
                 headers=BROWSER, timeout=10)

print(r.status_code)
# 输出：200        ← HTTP 层面"成功"了！

print(r.ok)
# 输出：True       ← requests 也认为没问题

print(r.json()["code"], r.json()["message"])
# 输出：-400 请求错误
#       ↑ 真正的错误藏在**返回内容里**，不在状态码里

# 【这是国内 API 的普遍套路】
#   B 站、微信、支付宝、大部分国产接口都这么设计：
#   HTTP 永远返回 200，业务是否成功看 body 里的 code 字段。
#
#   所以检查要做两层：
#       第一层  r.status_code / r.ok         → 请求有没有送到
#       第二层  data["code"] == 0            → 对方有没有真的办成
#
#   ★ 只查第一层是新手最常见的 bug，而且**AI 写代码时几乎从不查第二层** ——
#     因为它不知道你调的这个接口把 code 放在哪、成功值是 0 还是 200 还是 "ok"。
#     这一层永远只能你自己读文档补上。


# ---------- 3.5 POST：把数据交上去 ----------

# echo.apifox.com 是一个"回声服务"：你发什么它原样回什么，专门用来练手
r = requests.post(f"{ECHO}/post", json={"num": 17, "title": "requests"}, timeout=15)

print(r.status_code)
# 输出：200

print(r.json()["json"])
# 输出：{'num': 17, 'title': 'requests'}
#       ↑ 你发过去的东西被原样回显了

# ★ 用 json= 参数时，requests 自动做了两件事：
#     1. 把字典序列化成 JSON 字符串
#     2. 自动加上 Content-Type: application/json 请求头
print(r.json()["headers"]["Content-Type"])
# 输出：application/json

# GET 也可以对着它练，看参数收到没：
r = requests.get(f"{ECHO}/get", params={"lesson": "17", "name": "小明"}, timeout=15)
print(r.json()["args"])
# 输出：{'lesson': '17', 'name': '小明'}
#       ★ 注意 "17" 是字符串不是数字 —— URL 里的一切都是字符串，
#         跟第 2 课 input() 的道理一样

# 【别搞混 data= 和 json=】
#     json={"a": 1}   → 发 JSON，自动加头          ← 第 18 课调 AI 用这个
#     data={"a": 1}   → 发表单格式 a=1
#     data='{"a":1}'  → 发原始字符串，头要自己加
#
# 发错了对方通常返回 400，报错信息还很难懂。记住调 AI 用 json=。


# ---------- 3.6 ★★ timeout：这一节最重要的一行 ----------
"""
    requests 默认**没有超时**。

    没有超时意味着：对方不理你，你的程序就永远停在那一行。
    不报错，不继续，光标一直闪。你以为它在跑，其实它已经死了。

    这不是小概率事件 —— 网络抖一下、对方限流、WiFi 断了，都会触发。

    **规则：每一个 requests 调用都必须带 timeout。没有例外。**
    上面每个例子我都写了，你回头数一下。

    timeout=10 的意思是"10 秒还连不上/没数据就放弃"，然后抛异常。
    抛异常是好事 —— 至少你知道出事了。
"""

# /delay/5 会故意等 5 秒才回。我们只给它 2 秒：
try:
    requests.get(f"{ECHO}/delay/5", timeout=2)
except requests.Timeout:
    print("超时了，被 timeout=2 救下来了")
# 输出：超时了，被 timeout=2 救下来了

# 调 AI 时 timeout 要给大：大模型要"想"很久，10 秒经常不够，一般给 30-60 秒。


# ---------- 3.7 状态码检查 ----------

r = requests.get(f"{ECHO}/status/404", timeout=15)

print(r.status_code, r.ok)
# 输出：404 False

# ★★ 极其重要：请求失败时 requests **不会**自动抛异常。
#    上面这行平安跑过去了，r 只是一个 404 的空响应。
#    如果你接着 r.json()，那时才炸，而且报的是 JSON 解析错 ——
#    看着像"数据格式有问题"，实际是"压根没请求到数据"。误导性极强。

# 做法一：自己判断
if r.ok:
    print("成功")
else:
    print(f"请求失败，状态码 {r.status_code}")
# 输出：请求失败，状态码 404

# 做法二：raise_for_status()，4xx/5xx 直接抛异常
try:
    r.raise_for_status()
except requests.HTTPError as e:
    print("抓到了:", str(e)[:24])
# 输出：抓到了: 404 Client Error: NOT FO


# ---------- 3.8 该接哪些异常 ----------
"""
第 11 课讲过"该接什么、不该接什么"。requests 的异常长这样：

    requests.RequestException          总爹，下面全是它的子类
     ├── requests.ConnectionError      连不上（断网、域名不存在、DNS 挂了）
     ├── requests.Timeout              超时
     ├── requests.HTTPError            raise_for_status() 抛的
     └── requests.TooManyRedirects     跳转太多次

    还有一个**不在这一家**、特别容易漏的：

    requests.exceptions.JSONDecodeError    对方返回的不是合法 JSON
                                           （它是内置 ValueError 的子类）

规则跟第 11 课一样：**接你知道怎么处理的，别接你不认识的。**
兜底接 requests.RequestException 是合理的（网络问题都归它），
但别接 Exception —— 那会把你自己代码里的 bug 一起吞掉。
"""


def fetch_json(url, params=None, timeout=15):
    """一个写得比较周全的请求函数。第 18 课会照这个结构写。"""
    try:
        resp = requests.get(url, params=params, headers=BROWSER, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.Timeout:
        print(f"⏰ 超时了（{timeout} 秒）。网络慢，或者对方没响应")
    except requests.ConnectionError:
        print("🔌 连不上。检查网络，或者网址是不是打错了")
    except requests.HTTPError as e:
        print(f"❌ 对方返回了错误状态码：{e.response.status_code}")
    except ValueError:
        # JSONDecodeError 是 ValueError 的子类，这一条同时管住了它
        print("📄 返回的不是合法 JSON，可能是个错误页面")
    return None


print(fetch_json("https://www.baidu.com/sugrec",
                 params={"prod": "pc", "wd": "python"}) is not None)
# 输出：True

print(fetch_json(f"{ECHO}/status/500"))
# 输出：❌ 对方返回了错误状态码：500
#       None

print(fetch_json("https://这个域名根本不存在.xyz/abc"))
# 输出：🔌 连不上。检查网络，或者网址是不是打错了
#       None

print(fetch_json("https://www.baidu.com"))
# 输出：📄 返回的不是合法 JSON，可能是个错误页面
#       None

# ★ 注意每个 except 给的都是**人话提示**，不是一屏红字。
#   这就是本阶段验收标准里"断网时程序给出提示"那一条。


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题（热身）---
# 请求 https://echo.apifox.com/uuid，把返回的 uuid 打印出来。
# 要求：带 timeout、检查 status_code，再取数据。
# 提示：先 print(r.json()) 看结构，再决定怎么取
# TODO
print("第 1 题：")
r = requests.get(f"{ECHO}/uuid", timeout=10)

if r.status_code == 200:
    data = r.json()
    print(data["uuid"])
else:
    print(f"请求失败，状态码：{r.status_code}")

# --- 第 2 题 ---
# 用百度搜索建议接口（3.2 那个）写一个 suggest(word)：
#   传入一个词，返回联想词的列表（只要词，不要其他字段）
# 用 "python"、"初中" 各测一次。
# 提示：列表推导式。★ 这是第 4 课欠的债，这题必须用推导式写
# TODO
print("\n第 2 题：")
def suggest(word):
    r = requests.get(
        "https://www.baidu.com/sugrec",
        params={"prod": "pc", "wd": word},
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        return [item["q"] for item in data.get("g", [])]
    else:
        print(f"请求失败，状态码：{r.status_code}")
        return []

# --- 第 3 题 ---
# 写 bili_info(bvid)，查一个 B 站视频，返回 (标题, UP主, 播放量)。
# 要求：
#   [ ] 带 User-Agent，否则 412
#   [ ] 检查 HTTP 状态码
#   [ ] **还要检查 body 里的 code 字段**（3.4 讲的第二层）
#   [ ] 视频不存在时返回 None，不要崩
# 用一个真视频和一个假 bvid（比如 "BV1zzzzzzzzz"）各测一次。
# ★ 第三条是这题的重点。少了它，假 bvid 会让你的程序在取 data 时报 KeyError
# TODO
print("\n第 3 题：")
def bili_info(bvid):
    r = requests.get(
        "https://api.bilibili.com/x/web-interface/view",
        params={"bvid": bvid},
        headers=BROWSER,
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        if data.get("code") == 0:
            title = data["data"]["title"]
            owner = data["data"]["owner"]["name"]
            view_count = data["data"]["stat"]["view"]
            return (title, owner, view_count)
        else:
            print(f"视频不存在或其他错误，code: {data.get('code')}, message: {data.get('message')}")
            return None
    else:
        print(f"请求失败，状态码：{r.status_code}")
        return None

# --- 第 4 题（必做，别跳）---
# 亲手体验一次没有 timeout 的后果：
#   请求 https://echo.apifox.com/delay/10，**故意不写 timeout**，
#   老老实实等那 10 秒。
#   然后加上 timeout=3 再跑一次。
# 在注释里回答：如果对方永远不回，第一种写法会怎样？你怎么才能发现程序卡住了？
# ★ 这种事看一百遍不如自己等一次
# TODO
# 我的答案：


# --- 第 5 题（第 18 课直接用）---
# 把 3.8 的 fetch_json 改造成 post_json(url, payload, headers=None, timeout=30)：
#   发 POST，body 用 json= 传 payload
#   同样处理那四种异常
#   成功返回解析后的字典，失败返回 None
# 用 https://echo.apifox.com/post 测试，确认发过去的数据被回显了。
#
# ★ 这个函数第 18 课直接就用，认真写。写完可以收进 mytools.py
# TODO


# --- 第 6 题（挑战）---
# 给 post_json 加**自动重试**：失败最多重试 2 次，每次之前等 1 秒（time.sleep）。
#
# 但先想清楚一件事，答案写注释里：
#   哪些失败**值得**重试？哪些重试一万次也没用？
#   （提示：回去看"4xx 是你错、5xx 是他们错"）
#
# 重试代码本身不难，难的是"什么时候该重试"这个判断。
# 而这正是 AI 写重试逻辑时最常搞错的地方 —— 它经常无脑重试所有错误，
# 包括 401（key 错了，重试一百次还是错）和 429（越重试越糟）。
# TODO
# 该重试的：
# 不该重试的：


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑 ----------
"""
下面这段是"帮我写个函数从 API 获取数据"的典型 AI 产物。
网络正常时它表现完美。找出 5 个问题：

    import requests

    def get_video(bvid):
        url = "https://api.bilibili.com/x/web-interface/view?bvid=" + bvid
        try:
            response = requests.get(url)
            data = response.json()
            return data["data"]["title"]
        except:
            return None

写下你找到的：
    1.
    2.
    3.
    4.
    5.

【方向提示，每条对应一个坑】
    · 3.6 反复强调的那个参数
    · 3.7 说的"失败时不会自动抛异常"
    · 3.4 说的"HTTP 200 不等于成功"          ← 这条最难想到
    · 3.2 说的"别自己拼 URL"（bvid 要是带了特殊字符呢？）
    · 第 11 课就骂过的写法（ruff 规则 E722）

顺便：这个函数对着 B 站还有第 6 个问题 —— 3.3 讲过的。你发现了吗？

【找完再往下】
把这段发给 AI 问"这段代码有什么问题"，然后比对：
    · 它找到几个？
    · 它有没有提"要检查 data['code']"？（我赌它不会 —— 它不知道 B 站的约定）
    · 它给你的"改进版"里，有没有 timeout？

★ 最后这一问最有意思。经常出现的情况是：
  AI 在**被专门问到**时能说出"应该加 timeout"，
  但你直接让它"写个请求函数"，它自己就不加。
  **它知道，但它不做。** 所以你不能指望它自觉，只能自己检查。
"""

# ---------- 5.2 去问 ----------
"""
【模板 1 —— 先给方案，再让它挑刺】

    我要写一个调 API 的函数。我打算这样处理错误：
    用 try/except 包住，失败返回 None，调用的地方判断是不是 None。

    这个方案在什么情况下会坑到我？给我两个具体场景。不要写代码。

    ↑ 注意这个模板的结构：**先给出你的方案，再让它挑刺。**
      比问"我该怎么处理错误"好得多 —— 那样只会拿到泛泛的教科书回答。

【模板 2 —— 问原理，不问用法】

    不要给我代码。用一个生活里的类比解释：
    为什么 HTTP 要把错误分成 4xx 和 5xx 两类？这个划分对写代码的人有什么用？

【模板 3 —— 挖它的边界，然后抓它的错】

    requests 的 timeout 参数，官方文档说它其实是两个超时。
    分别是什么？它们的区别在什么场景下会体现出来？

    ↑ 这题 AI 有一定概率答得含糊或答错。
      答完去官方文档核对：
      https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
      **对着文档抓 AI 一次错，比顺利问对十次收获都大。**

【做完记在 summary 里】
    · 「找坑」你找到几个、漏了哪个
    · 模板 3 有没有抓到 AI 的错
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] 为什么每个 requests 调用都必须带 timeout？不带会怎样？
# [ ] 服务器返回 404 时 requests.get() 会抛异常吗？那你怎么知道失败了？
# [ ] HTTP 状态码 200 就代表成功了吗？B 站那个例子说明了什么？
# [ ] 4xx 和 5xx 的区别？这个区别怎么影响"要不要重试"？
# [ ] json= 和 data= 的区别？调 AI API 用哪个？
# [ ] 为什么不能自己用字符串拼 URL 参数？
# [ ] 请求 B 站为什么要带 User-Agent？不带会返回什么？
# [ ] .json() 报 "Expecting value: line 1 column 1" 时，你第一步该干什么？


if __name__ == "__main__":
    print("\n第 17 课「读一读」全部跑完（网络正常）。")
    print("第 4、5 题必做 —— 第 18 课直接用第 5 题的成果。")
