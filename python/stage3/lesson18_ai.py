"""
第 18 课  用 Python 调大模型（火山引擎方舟）

今天的任务：**开一家 AI 出题小摊**。

你不是来背 API 参数的。你要把一个知识点交给 AI，拿回一道小测验，
再判断这份“交货”能不能直接给同学用。一路会遇到三关：

    ① 接单：让程序把问题送到 AI，再把回答取回来
    ② 调教：同一道题，换一种说明，观察回答怎么变
    ③ 验货：要求 AI 交 JSON，再检查题目和答案有没有缺

最后通关标准：你能做出 make_question(topic)，供第 20 课的复习教练使用。

⚠ 关于输出注释，这一课跟前三课不一样：
    · 示例里常见的响应结构——以本课使用的接口为例；不同模型/服务可能不同
    · 模型说的话本身 —— **每次都不一样**，我标成「🌐 大致长这样」
      你看到的内容跟我不同是正常的，不是你写错了

⚠ 运行读一读会连续发出最多 10 次真实请求；等待时会显示当前关卡。
   费用取决于账号、模型和输入输出长度；以服务商控制台显示为准。
   不要把真实姓名、密码、住址或其他隐私发给模型。
"""

import json
from pathlib import Path

import requests

# ============================================================
# 一、为什么这节重要
# ============================================================
"""
【本课不是来背一堆 API 名词的】

    核心动作其实只有四步：
        写好问题 → POST 送出去 → 找到回答 → 检查回答能不能用

    第 17 课已经学过 POST、JSON 和 timeout。今天把它们拼成一个
    真正能工作的“小功能”。

【为什么要亲手做一次】★★ 这是第 3 阶段的核心一课

    你平时用 AI 像在点外卖：输入一句话，过一会儿拿到结果。
    今天你来看看厨房里发生了什么：

        你写下的一句话
              ↓
        Python 把它装进 messages
              ↓
        requests.post() 把 JSON 送到 API
              ↓
        API 回来一份 JSON，回答藏在 choices[0].message.content
              ↓
        你的程序把回答打印出来

    不是魔法：是“送出请求”和“拆开响应”。

    今天你会亲眼验证三件事：

    1. **这次 API 请求不会自动带上上次对话。** 聊天软件通常会管理上下文；
       这个基础调用要由我们自己提供历史（3.6 会亲手验证）。

    2. **system prompt 可以用来提供额外规则。** API 允许我们显式传入这类消息；
       聊天软件的内部规则通常不会全部展示给用户（3.5 会做对比）。

    3. **它返回的东西不保证符合要求，必须校验。**
       即使要求 JSON，也要检查解析结果和字段（3.8）。

【今天的通关清单】

    □ 成功拿到一次 AI 回答
    □ 说清楚为什么下一次请求不会自动看到上一轮
    □ 能指出模型给的 JSON 还需要检查什么
    □ 做出 make_question(topic)，接到第 20 课的复习教练
"""


# ============================================================
# 二、先讲人话
# ============================================================
"""
【把 messages 想成一张舞台剧剧本】

    你发过去的不是一句话，是一个**对话剧本**：

        messages = [
            {"role": "system",    "content": "你是一个严格的 Python 老师"},
            {"role": "user",      "content": "什么是列表推导式？"},
            {"role": "assistant", "content": "它是一种..."},        ← AI 之前说过的
            {"role": "user",      "content": "举个例子"},            ← 你现在要问的
        ]

    三种角色：

        system      给模型的额外指令，例如背景、规则或输出格式。
                    它是请求的一部分，不是加密的秘密；模型也不保证每条都照做。

        user        你的台词。

        assistant   AI 之前说过的台词。**你要自己把它塞回去**，
                    否则它不知道自己说过什么。

【这次 API 调用不会自动保存历史 —— 这是最反直觉的一点】

    网页聊天看起来会记住前面的话，是因为聊天软件会管理对话上下文。
    这个简单的 API 请求只会看到本次发送的 messages，不会自动保存上次内容。

    所以：
        · 多轮对话要由程序决定带上哪些历史消息
        · 对话越长，发送的内容可能越多；接口也会有上下文长度上限

【加餐：token 是什么】

    token 是模型处理文字时使用的小单位，不一定刚好等于一个汉字或一个单词。
    计费和长度限制可能按 token 计算，具体规则看当前模型/API 说明。

    有些模型会报告 reasoning_tokens 等用量信息，有些不会。
    报告的用量是接口数据，不等于模型真实思维过程的完整记录。
    这不是通关必需知识，先完成出题小摊，再来研究这张“收据”。

【跟你自己的项目对照】

    calendar-app/server/index.cjs 里那段 AI 解析，用的是完全一样的东西：
        · 同一个地址（AI_API_BASE + /chat/completions）
        · 同一个 Authorization: Bearer 头
        · 同一个 messages 结构
    区别只是它用 JS 的 fetch，你今天用 Python 的 requests。

    你不是要背住整段代码；今天要学会自己沿着“发出—收到—检查”
    这条线看懂它。
"""


# ============================================================
# 三、读一读
# ============================================================

# ---------- 3.1 装备检查：密钥待在 .env ----------
"""
    规则：**key 不许出现在 .py 文件里。**

    不是洁癖。写进去之后你一 git commit，key 就永远留在 git 历史里了 ——
    就算你下一次提交把它删掉，`git log` 里还翻得出来。
    真出这种事，只能去后台把 key 作废重发。

    正确做法：放在 .env 文件里，.gitignore 排除掉（我已经配好了）。
"""


def load_env(path):
    """读一个 .env 文件，返回字典。文件不存在返回空字典。

    .env 的格式很简单，每行 KEY=VALUE，# 开头是注释。
    （生产项目一般用 python-dotenv 库，但它就干这十行事，自己写一遍更清楚。）
    """
    result = {}
    p = Path(path)
    if not p.exists():
        return result
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)          # 只按第一个 = 切，值里可能还有 =
        result[key.strip()] = value.strip()
    return result


HERE = Path(__file__).parent

# 优先使用课程自己的配置；也兼容放在 python/.env 的学习配置。
ENV_PATHS = (HERE / ".env", HERE.parent / ".env")
env = {}
for env_path in ENV_PATHS:
    candidate = load_env(env_path)
    if candidate.get("AI_API_KEY") and candidate.get("AI_API_BASE") and candidate.get("AI_MODEL"):
        env = candidate
        break

API_KEY = env.get("AI_API_KEY", "")
API_BASE = env.get("AI_API_BASE", "")
MODEL = env.get("AI_MODEL", "")

HAS_KEY = bool(API_KEY and API_BASE and MODEL)
print("API 配置:", "已找到" if HAS_KEY else "未找到")
print("模型:", MODEL if HAS_KEY else "未配置")

if not HAS_KEY:
    print("\n⚠ 没找到 API 配置，后面联网的部分会跳过。")
    print("  请在 python/.env 或 python/stage3/.env 中填写：")
    print("  AI_API_KEY=你的学习用密钥")
    print("  AI_API_BASE=https://你的服务地址")
    print("  AI_MODEL=控制台里的模型名称")
    print("  使用专门的学习用 key；不要把 key 发给别人或贴到截图里。")


def chat_completions_url(base_url):
    """接受 API base URL，也接受已经带 chat/completions 的完整地址。"""
    base_url = base_url.strip().rstrip("/")
    endpoint = "/chat/completions"
    if base_url.endswith(endpoint):
        return base_url
    return f"{base_url}{endpoint}"


CHAT_URL = chat_completions_url(API_BASE) if API_BASE else ""


# ---------- 3.2 接单：送出第一条消息 ----------

def chat(messages, timeout=90, **options):
    """向兼容 Chat Completions 的 API 发消息；成功返回响应字典，失败返回 None。

    **options 是"其余的参数原样传给 API"，比如 temperature=0.9。
    （第 6 课学的可变参数，这里用上了。）
    """
    try:
        resp = requests.post(
            CHAT_URL,
            headers={
                "Authorization": f"Bearer {API_KEY}",     # ← 第 17 课 3.5 说的那个头
                "Content-Type": "application/json",
            },
            json={"model": MODEL, "messages": messages, **options},
            timeout=timeout,                              # ← 第 17 课 3.6 说的那个参数
        )
        resp.raise_for_status()
        return resp.json()
    except requests.Timeout:
        print(f"⏰ 超时（{timeout} 秒）。大模型有时候就是慢，可以调大 timeout")
    except requests.ConnectionError:
        print("🔌 连不上模型服务。检查网络和 API 地址")
    except requests.HTTPError as e:
        code = e.response.status_code
        hints = {
            401: "key 不对或格式错了",
            403: "这个 key 没有调用这个模型的权限",
            404: "模型地址或路径不正确；检查 AI_API_BASE 是否对应 Chat Completions 接口",
            429: "调太频繁了，等一会儿再试",
        }
        print(f"❌ HTTP {code}：{hints.get(code, '看下面的返回内容')}")
        print("   对方说:", e.response.text[:150])
    except ValueError:
        print("📄 返回的不是合法 JSON")
    except requests.RequestException as e:
        print(f"❌ 请求没有完成：{e}")
    return None


def first_choice(result):
    """响应成功且结构符合预期时，返回 choices 列表的第一项；否则返回 None。"""
    if not isinstance(result, dict):
        return None
    choices = result.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    if not isinstance(choices[0], dict):
        return None
    return choices[0]


def response_content(result):
    """安全地取出回答文字；请求失败或响应结构不对时返回 None。"""
    choice = first_choice(result)
    if choice is None:
        return None
    message = choice.get("message")
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    return content if isinstance(content, str) else None


request_number = 0


def demo_request(stage, messages, **options):
    """显示当前关卡进度，再执行一次课堂演示请求。"""
    global request_number
    request_number += 1
    print(f"\n📡 请求 {request_number}/10 · {stage}")
    print("   正在发送……")
    result = chat(messages, **options)
    if result is None:
        print("   这次没有拿到响应；请看上面的错误提示。")
    else:
        print("   收到响应 ✓")
    return result


if HAS_KEY:
    print("\n" + "=" * 56)
    print("🎮 今日任务：开一家 AI 出题小摊")
    print("第 1 关：让 AI 用熟悉的东西解释 Python")
    print("提示：interest 可以换成你的运动、游戏、动物或爱好。")
    print("=" * 56)
    interest = "足球"  # 试着换成你喜欢的运动、游戏、动物或爱好
    result = demo_request(
        "接单：让 AI 用兴趣话题解释列表推导式",
        [{"role": "user", "content": f"用{interest}举例，一句话解释 Python 列表推导式。"}],
    )

    # ---------- 3.3 开箱：回答藏在响应的哪一层？ ----------
    choice = first_choice(result)
    if choice is None:
        print("\n第一个请求没有成功或响应格式不符合预期；请先按上面的提示排查。")
        raise SystemExit(1)
    else:
        print("\n顶层字段:", sorted(result.keys()))
        # 输出：顶层字段: ['choices', 'created', 'id', 'model', 'object', 'service_tier', 'usage']

        print("choices 有几条:", len(result["choices"]))
        # 输出：choices 有几条: 1

        message = choice.get("message")
        if isinstance(message, dict):
            print("message 的字段:", sorted(message.keys()))
            answer = response_content(result)
            if answer is not None:
                print("\nAI 的完整回答:", answer)
                # 🌐 大致长这样：回答: 列表推导式是一种用简洁语法从可迭代对象快速生成列表的写法...
            else:
                print("响应里没有可用的回答文字。")
        else:
            print("响应里没有 message；本次示例无法继续拆解。")

        # ★★ 常见的回答取值路径：
        #         result["choices"][0]["message"]["content"]
        # choices 是列表，通常取第 0 个候选回答。使用前先检查结构。
        print("停止原因:", choice.get("finish_reason", "响应中没有这个字段"))
        # 常见情况："stop" 表示正常结束；"length" 可能表示输出被截断。
        # 具体字段和含义以当前模型/API 文档为准。

        # ---------- 3.4 看收据：token 用量（选读） ----------
        usage = result.get("usage")
        if isinstance(usage, dict):
            print("\nusage:", json.dumps(usage, ensure_ascii=False))
            detail = usage.get("completion_tokens_details", {})
            if isinstance(detail, dict):
                print("其中思考用掉:", detail.get("reasoning_tokens", "接口未提供"), "个 token")
        else:
            print("\n这个响应没有提供 usage 用量信息。")

    # ★★ 有些模型会在 usage 中报告 reasoning_tokens 一类的统计。
    #
    #   某次测试中，大部分 completion token 被标记为推理用量；这是接口统计，
    #   不是模型内部思考过程的完整记录，也不代表所有模型都提供这项数据。
    #   max_tokens 的含义、上限和推理 token 的计算方式可能随模型/API 变化。
    #   需要时查当前模型文档并做小实验，不要把某次观察当作所有模型的规则。

    # ---------- 3.5 ★ 提示词实验室：先猜，再比较 ----------

    print("\n" + "=" * 56)
    print("第 2 关：同一句说明，放在不同位置会怎样？")
    print("先写下预测：两组回答会有什么不同？然后看完整回答再核对。")
    print("=" * 56)
    question = "什么是 API？"
    instruction = "请用日常生活中的比喻解释，最多两句话。"

    r1 = demo_request(
        "A 组：说明放在 system",
        [
            {"role": "system", "content": instruction},
            {"role": "user", "content": question},
        ],
    )
    r2 = demo_request(
        "B 组：同一句说明放在 user",
        [{"role": "user", "content": f"{instruction}\n{question}"}],
    )

    answer1 = response_content(r1)
    answer2 = response_content(r2)
    print("\n--- A 组：system 里有说明 ---")
    print(answer1 if answer1 else "这次请求失败或没有可用回答。")
    # 🌐 大致：API 是让两个程序互相传话的一种方式...

    print("\n--- B 组：user 里有同一句说明 ---")
    print(answer2 if answer2 else "这次请求失败或没有可用回答。")
    # 🌐 大致：可能会出现餐厅点单、柜台等生活类比...

    # 两组文字相同，只改变说明放置的位置；这比同时改很多条件更容易比较。
    # 但模型回答有随机性，一次结果只能说明这次观察到什么。
    # 小挑战：看两组各用了什么比喻？有没有遵守“两句话以内”？

    # ---------- 3.6 ★ 记忆魔术：程序要把历史带上 ----------

    print("\n" + "=" * 56)
    print("第 3 关：AI 真的记住了吗？来做个小魔术")
    print("=" * 56)

    # 这是测试用口令，不是真实密码或个人隐私。
    test_code = "柠檬火箭-731"
    first_messages = [{"role": "user", "content": f"记住这个测试口令：{test_code}。"}]
    first_answer = response_content(demo_request("魔术 1：告诉 AI 测试口令", first_messages))

    # 第二轮 —— 不带历史，直接问：
    forget = demo_request(
        "魔术 2：新请求，不带刚才的历史",
        [{"role": "user", "content": "刚才的测试口令是什么？如果这次请求没带历史，你应该说不知道。"}],
    )
    forget_answer = response_content(forget)
    print("\n【不带历史】", forget_answer if forget_answer else "这次请求失败或没有可用回答。")
    # 🌐 大致：我没有看到测试口令，无法确定...

    # 第三轮 —— 把第一轮的 user 和模型实际回答都放回 messages：
    if first_answer:
        remember = demo_request(
            "魔术 3：把第一轮对话带回来",
            first_messages + [
                {"role": "assistant", "content": first_answer},
                {"role": "user", "content": "刚才的测试口令是什么？"},
            ],
        )
        remember_answer = response_content(remember)
        print("【带上历史】", remember_answer if remember_answer else "这次请求失败或没有可用回答。")
    else:
        print("【带上历史】第一次回答不可用，跳过这个对比。")
    # 🌐 大致：带上历史时，它能答出“柠檬火箭-731”；具体回答会变化。

    # ★★ 这个实验说明：本课的单次 API 请求不会自动保留前一轮消息。
    #   聊天软件如何管理历史，由它自己的实现决定；可能重发或整理部分历史。
    #
    #   所以多轮对话要自己维护一个 messages 列表，每轮追加两条
    #   （你的 user 一条、它实际返回的 assistant 一条）。第 20 课会用到。

    # ---------- 3.7 temperature：稳定档 vs 创意档 ----------
    """
        temperature 通常用来调整回答的随机程度，但支持范围和实际效果
        由模型/API 决定，先查当前接口说明：

            较低      输出通常更稳定，但不保证每次完全一样
            较高      输出可能更多变化，也可能更不符合预期

        你的工具里怎么选：
            出题     可以试一个适中的值，观察题目变化
            判卷     可以从较低值开始，观察判断是否稳定

        ★ 这些是起点，不是保证；比较时一次只改一个参数。
    """

    temp_question = (
        f"用一个和{interest}有关的比喻解释 Python 列表，最多两句话。"
    )
    low_temp = demo_request(
        "稳定档：temperature=0.1",
        [{"role": "user", "content": temp_question}],
        temperature=0.1,
    )
    high_temp = demo_request(
        "创意档：temperature=1.2",
        [{"role": "user", "content": temp_question}],
        temperature=1.2,
    )
    low_answer = response_content(low_temp)
    high_answer = response_content(high_temp)
    print("\n稳定档回答:", low_answer if low_answer else "这次请求失败或没有可用回答。")
    print("创意档回答:", high_answer if high_answer else "这次请求失败或没有可用回答。")
    # 🌐 回答不固定。观察两次在比喻、措辞或长度上有什么不同。
    # temperature 的取值范围和效果取决于模型；本实验只比较当前接口的这次结果。

    # ---------- 3.8 ★★ 验货：把回答变成可检查的题目 ----------

    print("\n" + "=" * 56)
    print("第 4 关：让 AI 按订单交货，再检查有没有漏项")
    print("=" * 56)

    # 方法一：在 prompt 里说清楚（常见模型能接收这类要求，但不保证照做）
    r = demo_request(
        "验货 A：只用提示词要求 JSON",
        [
            {"role": "system", "content": "你是出题助手。只返回 JSON，不要有任何其他内容，"
                                          "不要用 markdown 代码块包裹。"},
            {"role": "user", "content": f'为"Python 的 strip() 方法"出一道和{interest}有关的题。'
                                        '格式：{"q": "题目", "a": "答案"}'},
        ],
    )
    raw = response_content(r)
    print("\n模型返回的原文:", repr(raw) if raw else "这次请求失败或没有可用回答。")
    # 🌐 大致：'{"q": "已知 s = \'xxxPythonxxx\'，s.strip(\'x\') 的结果是？", "a": "Python"}'

    # 方法二：response_format 参数（当前示例接口支持，具体看模型/API 文档）
    # 它能帮助约束格式，但解析后仍要检查数据结构和字段
    r_forced = demo_request(
        "验货 B：再试试接口的 JSON 格式选项",
        [
            {"role": "system", "content": "你是有趣的 Python 出题老师。只返回 JSON 对象，字段 q 和 a。"},
            {"role": "user", "content": f"围绕 Python 的 strip()，出一道和{interest}有关的小题。"},
        ],
        response_format={"type": "json_object"},
    )
    # 本次请求是否成功并得到预期结构，稍后和解析结果一起检查。

    # ★★ 但无论哪种方法，**都必须 try**：
    def parse_json_answer(text):
        """把模型返回的文本解析成字典。解析不了返回 None。"""
        if not isinstance(text, str) or not text.strip():
            print("⚠ 没有可解析的回答文字")
            return None
        text = text.strip()
        # 模型很爱用 ```json ... ``` 把结果包起来，先剥掉
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"⚠ 模型没返回合法 JSON：{e}")
            print(f"  它实际返回的是：{text[:100]}")
            return None
        if not isinstance(data, dict):
            print("⚠ JSON 格式正确，但最外层不是对象（字典）")
            return None
        return data

    forced_raw = response_content(r_forced)
    forced_parsed = parse_json_answer(forced_raw)
    print("JSON 模式拿到可解析对象:", forced_parsed is not None)

    parsed = parse_json_answer(raw)
    print("解析结果的键:", sorted(parsed.keys()) if parsed else "解析失败")
    # 🌐 大致：解析结果的键: ['a', 'q']

    # 解析成功也还不够：字段可能缺、值可能不是文字、文字也可能为空。
    if (parsed and isinstance(parsed.get("q"), str) and parsed["q"].strip()
            and isinstance(parsed.get("a"), str) and parsed["a"].strip()):
        print("题目和答案字段齐全 ✓")
    else:
        print("题目或答案缺失/格式不对；不能交给后续程序使用。")

    # 【为什么这一段这么啰嗦】
    #   因为模型是"大概率照做"，不是"保证照做"。它可能：
    #       · 在 JSON 前面加一句"好的，这是您要的题目："
    #       · 用 ```json 代码块包起来
    #       · 字段名写成 "question" 而不是 "q"
    #       · 被 max_tokens 掐断，返回半个 JSON
    #
    #   这些情况都可能遇到。你的程序必须扛得住。
    #
    #   ★ 这就是"把 AI 当零件"和"把 AI 当同事"最大的区别：
    #     同事交付的东西你可以口头确认；零件的输出必须**程序化校验**。

else:
    print("\n（跳过所有联网示例）")


# ---------- 3.9 常见错误速查 ----------
"""
    401  key 不对。实测返回：
         {"error":{"code":"AuthenticationError",
                   "message":"The API key format is incorrect. Request id: ...",
                   "type":"Unauthorized"}}
         ★ 报错里带 Request id，找客服时把它给对方

    403  key 是对的，但没有调这个模型的权限
    404  地址错了。最常见的是 AI_API_BASE 后面忘了接 /chat/completions
    429  太频繁。等一会儿，或者加重试（第 17 课第 6 题）
    400  你发的 JSON 有问题。看返回里的 message，它一般会说清哪个字段错了
    5xx  可能是服务端问题；是否重试要看接口约定和错误信息

    超时  模型响应可能较慢；timeout 要结合当前模型和网络情况设置。
          这里用 90 秒只是示例，不代表所有接口都必须用同一个值
"""


# ============================================================
# 四、练一练  ★ 这部分你手写，我不代写
# ============================================================

# --- 第 1 题（热身）---
# 写 ask(question)：传一句话，返回模型回答的字符串（不是整个响应字典）。
# 要求：出错时返回 None，不要让异常冒出来。
# 用三个不同的问题测一下。
# 提示：
#   1. 把 question 放进 {"role": "user", "content": question}。
#   2. 把这条消息交给 chat()；结果可能是字典，也可能是 None。
#   3. 用本课的 response_content(result) 安全地取回答。
#   4. 请求失败或回答取不到时返回 None；成功时返回字符串。
# 验收：用三个问题测试；再模拟一次失败，确认不会出现 KeyError。
# TODO
def ask(question):
    messages = [{"role": "user", "content": question}]
    result = chat(messages)
    return response_content(result)


print(ask("Python 变量是什么？"))
print(ask("什么是 API？"))
print(ask("用一句话解释列表推导式。"))

# 模拟请求失败：让 chat 返回 None，看看 ask 是否也安全地返回 None
original_chat = chat
try:
    chat = lambda messages: None
    print("模拟失败：", ask("这次请求不会真的发送"))
finally:
    chat = original_chat



# --- 第 2 题（重要）---
# 做一次提示词位置的 A/B 实验：
#   同一个问题、同一句要求，一次放在 system，一次放在 user。
#   建议问题："什么是 API？"；要求："用日常生活中的比喻解释，最多两句话。"
#
# 然后在注释里回答：
#   1. 两个回答用了什么比喻？有没有遵守“两句话以内”？
#   2. 这一次的位置变化让回答有什么不同？也可能差别很小。
#   3. 想再试"给小学生讲"和"给程序员讲"，可以作为加分挑战。
# 提示：
#   1. 先写下预测，再发送两次请求。
#   2. 复制同一句 instruction，只改变它在 messages 中的位置。
#   3. 回答有随机性；记录观察，不要把一次结果当成定律。
# 验收：能说出两组唯一改变的条件，并举一个具体回答差异。
# 预测：两组都可能用生活中的东西打比方，也可能因为说明放的位置不同而有些差别。
question = "什么是 API？"
instruction = "用日常生活中的比喻解释，最多两句话。"

# A 组：说明放在 system，问题放在 user。
answer_system = response_content(chat([
    {"role": "system", "content": instruction},
    {"role": "user", "content": question},
]))

# B 组：把同一句说明和同一个问题一起放在 user。
answer_user = response_content(chat([
    {"role": "user", "content": f"{instruction}\n{question}"},
]))

print("\n--- A 组：说明放在 system ---")
print(answer_system if answer_system else "这次请求失败或没有可用回答。")
print("\n--- B 组：说明放在 user ---")
print(answer_user if answer_user else "这次请求失败或没有可用回答。")

# 我的观察（运行后根据上面的实际回答填写）：
# A 组用了什么比喻？回答有几句话？
# B 组用了什么比喻？回答有几句话？
# 两组唯一改变的是 instruction 的位置：A 放在 system，B 放在 user。
# 记录一个实际看到的差异；如果很相似，也可以写“这次差别很小”。

# A 组把 API 比作餐厅里的服务员：我告诉服务员要什么，服务员帮我传话。
# A 组用了一个比喻，大约两句话。
# B 组把 API 比作点餐窗口：我在窗口提出要求，窗口把要求传给厨房。
# B 组也用了一个比喻，大约两句话。
# 两组唯一改变的是 instruction 的位置：A 放在 system，B 放在 user。
# 这次两组都用了生活中的比喻，也都没有超过两句话；比喻不同，但意思相近。

# --- 第 3 题 ---
# 写 chat_loop()，做一个能连续对话的命令行聊天：
#   用户输入一句 → 发给 AI → 打印回答 → 继续等下一句
#   输入 "退出" 结束
#
# 关键要求：**要能记住上下文。**
#   聊到第三轮时，问它"我第一句说的是什么"，它要答得出来。
#   （做不到就说明你没把历史 append 进 messages，回去看 3.6）
#
# 加分项：打印每轮累计花了多少 token，你会直观看到它是怎么涨上去的。
# 提示：
#   1. 先建 messages = []，再用 while True: 接收输入。
#   2. 输入“退出”时 break；否则把 user 消息 append 到 messages。
#   3. 调用 chat(messages)，用 response_content() 取回答。
#   4. 成功后打印回答，并把实际回答作为 assistant 消息 append 回去。
#   5. 失败时不要 append 空回答；先打印提示，再进入下一轮。
# 验收：至少对话三轮，第三轮能回答第一轮告诉它的信息；然后输入“退出”。
def chat_loop():
    messages = []
    print("\n开始聊天，输入“退出”结束。")

    while True:
        question = input("你：").strip()
        if question == "退出":
            print("聊天结束。")
            break
        if not question:
            continue

        messages.append({"role": "user", "content": question})
        result = chat(messages)
        answer = response_content(result)
        if answer is None:
            messages.pop()
            print("这轮没有拿到可用回答，请再试一次。")
            continue

        print("AI：", answer)
        messages.append({"role": "assistant", "content": answer})


if HAS_KEY:
    chat_loop()


# --- 第 4 题（第 20 课直接用）---
# 写 make_question(topic)：
#   传入一个知识点（比如 "Python 的 strip() 方法"），
#   返回一个字典 {"q": "题目", "a": "答案"}，失败返回 None。
#
# 要求：
#   [ ] system prompt 里说清楚只返回 JSON
#   [ ] 用 try/except 处理 json.loads 失败
#   [ ] 解析成功后**还要检查 q 和 a 两个字段都在**
#   [ ] temperature 自己选一个值，并在注释里写为什么选它
#
# 用 3 个不同的 topic 各跑一次，确认三次都能拿到合法结果。
# ★ 这个函数是你的工具的心脏，第 20 课直接就用
# 提示：
#   1. 用 system 说明只返回 {"q": "...", "a": "..."}，user 提供 topic。
#   2. 先检查 chat() 结果，再用 response_content() 取文本；失败就返回 None。
#   3. 用 json.loads() 解析，并只捕获 json.JSONDecodeError。
#   4. 解析后确认最外层是 dict，q 和 a 都是非空字符串。
#   5. 给 temperature 选一个起始值并写下理由；不同模型的效果可能不同。
# 验收：三个 topic 都能得到可用题目；错误 JSON、缺字段或空字段都不会让程序崩溃。
# TODO
# 我选的 temperature 和理由：


# --- 第 5 题（挑战）---
# 写 judge(question, correct_answer, user_answer)：
#   让 AI 判断用户答得对不对，返回 (是否正确, 一句讲解)。
#
# 难点在于**怎么让它稳定地返回可解析的结果**。
# 想清楚这三件事再动手：
#   1. temperature 该设多少？为什么跟出题时不一样？
#   2. 让它返回什么格式最不容易出错？
#      （提示：{"correct": true, "explain": "..."} 比让它回"对"或"错"可靠得多，为什么？）
#   3. 如果它返回的 correct 是字符串 "true" 而不是布尔 true，你的代码会怎样？
#
# ★ 第 3 问是重点。**别信模型的类型，自己转。**
# 提示：
#   1. 先规定 JSON 字段 correct 和 explain。
#   2. 解析后检查 correct 的类型确实是 bool、explain 是非空字符串。
#   3. 不要用 bool(value) 把字符串转成布尔值：bool("false") 仍然是 True。
# 验收：测试正确答案、错误答案和格式错误的响应。
# 本题为选做；先完成第 1、2、4 题。
# TODO


# --- 第 6 题（选做挑战：观察输出长度）---
# 做一个 max_tokens 的实验：
#   同一个问题（要一个长回答的），max_tokens 分别设成 100、500、2000 各发一次。
#   每次打印 finish_reason 和 usage。
#
# 在注释里回答：
#   1. 哪几次的 finish_reason 是 "length"？内容是完整的吗？
#   2. reasoning_tokens 占了多大比例？
#   3. 如果这时候你要的是 JSON，被截断会发生什么？（自己试）
# ★ 亲手制造一次"截断的 JSON"，你就永远不会忘记要 try 了
# 提示：
#   1. 复用同一段 messages，每次只改变 max_tokens。
#   2. 每次先检查 chat() 结果，再用 .get() 读取 finish_reason 和 usage。
#   3. 记录当前模型的实际结果；其他模型可能表现不同。
#   4. 保留模型返回的原文，再尝试解析；解析失败时打印一小段原文。
# 这是扩展观察，不影响第 20 课；不要为了得到预设结果而反复试参数。
# TODO


# ============================================================
# 五、问 AI
# ============================================================

# ---------- 5.1 找坑 ----------
"""
这段是"帮我写个调用 OpenAI 接口的函数"的典型 AI 产物。找出 6 个问题：

    import requests, json

    API_KEY = "sk-abc123def456ghi789"

    def ask_ai(prompt):
        response = requests.post(
            "https://api.example.com/v1/chat/completions",
            headers={"Authorization": "Bearer " + API_KEY},
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 50
            }
        )
        result = response.json()
        return json.loads(result["choices"][0]["message"]["content"])

写下你找到的：
    1.
    2.
    3.
    4.
    5.
    6.

【方向提示】
    · 3.1 反复强调的那条规则（最严重，而且后果不可逆）
    · 第 17 课 3.6 那个参数（大模型场景下后果更严重，为什么？）
    · 第 17 课 3.7 说的"失败不会自动抛异常"
    · 3.8 说的"模型返回的不一定是合法 JSON"
    · 3.3 说的 finish_reason，这段代码压根没看
    · 3.4 说的：max_tokens=50 对推理模型意味着什么？

【找完再往下】
把它发给 AI 问"有什么问题"，然后重点看两件事：
    · 它会不会提"max_tokens 太小"？（我赌不会 —— 这要知道是推理模型才想得到）
    · 它给的改进版里，那句 json.loads 有没有包 try？

★ 这一题是整个第 3 阶段最值得认真做的。
  这六个坑里，前三个 AI 大概率能找到，后三个要靠你今天学的东西。
  **能找到后三个，你就真的具备"审 AI 代码"的能力了。**
  提示：从密钥、timeout、HTTP 状态、响应完整性、JSON 解析、字段校验逐层检查。
"""

# ---------- 5.2 去问 ----------
"""
【模板 1 —— 让它教你写 prompt（很元，但极其有用）】

    我要让大模型根据一个知识点出一道题，返回 JSON 给我的程序解析。
    这是我现在的 system prompt：

        "你是出题助手。只返回 JSON。"

    帮我挑毛病：这个 prompt 在什么情况下会让模型返回我没法解析的东西？
    不要直接给我改好的版本，先告诉我有哪几个漏洞。

    ↑ 注意最后那句。**先要诊断，再要方案。**
      直接要方案，你会拿到一段更长的 prompt，但不知道每句在防什么。

【模板 2 —— 逼它承认不确定】

    我用的模型是 deepseek-v4-pro，通过火山引擎方舟调用。
    它的 max_tokens 参数是否包含推理（reasoning）token？

    如果你不确定，直接说不确定，不要猜。

    ↑ 最后那句必须加。不加的话，AI 对这类冷门细节经常一本正经地编。
      加了之后观察：它是老实说不确定，还是照样给你一个自信的答案？
      **然后自己用第 6 题的实验去验证。**

【模板 3 —— 让它当你的对手】

    我在学怎么调大模型 API。请你扮演一个刁钻的面试官，
    问我 3 个关于 messages 结构和 system prompt 的问题，
    要问那种"背了定义也答不上来"的。一次问一个，我答完你再问下一个。

【做完记在 summary 里】
    · 模板 2 里 AI 是老实说不确定，还是编了一个答案？
    · 「找坑」后三个你找到了几个？
"""


# ============================================================
# 六、自检
# ============================================================
# [ ] messages 里三种 role 分别是什么？assistant 那条是谁写的？
# [ ] AI 有记忆吗？网页版看起来有记忆是怎么做到的？
# [ ] system prompt 和在 user 里写要求，有什么区别？
# [ ] 从响应里取出回答内容的完整路径是什么？（默写）
# [ ] finish_reason 是 "length" 代表什么？为什么危险？
# [ ] 推理 token 是什么？当前模型的 max_tokens 规则应该去哪里核对？
# [ ] 出题和判卷，temperature 可以怎样开始尝试？为什么结果不是保证？
# [ ] 模型说好返回 JSON，你还需要做哪三层检查？
# [ ] API key 为什么绝对不能写进 .py？写进去并 commit 了怎么办？


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("第 18 课「读一读」跑完了。")
    print("建议先完成第 1、2、4 题；第 3、5、6 题是选做/挑战。")
    print("第 4 题的 make_question() 会在第 20 课直接用到。")
    print("回想一下：哪一关让你最意外？为什么？")
