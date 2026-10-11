# 第 17 课学习总结：requests 调 HTTP API

## 为什么学这个很重要

| 重要点 | 说明 |
| --- | --- |
| 程序可以从网络获取数据 | `requests` 让 Python 像浏览器一样发送 HTTP 请求、接收响应，是连接外部 API 的基础。 |
| 接入 AI 并没有魔法 | 调用 AI API 也是发送 HTTP 请求；理解请求方法、请求头和 JSON，才能判断是网络、认证还是请求内容出了问题。 |
| 请求必须设置 `timeout` | `requests` 默认没有超时；网络或服务器没有响应时，程序可能一直等下去。 |
| HTTP 成功不一定代表业务成功 | 有些 API 即使请求成功也会返回 HTTP 200，仍要检查响应 JSON 里的业务状态，例如 B 站的 `code`。 |
| 出错时要分清问题类型 | 超时、连接失败、HTTP 错误和 JSON 解析失败需要不同处理；盲目捕获所有异常会把代码自身的问题也藏起来。 |

## 学习目标与真正学会的内容

| 学习目标 | 本课代码体现的内容 |
| --- | --- |
| 发送 GET 请求 | `requests.get(url, params=..., timeout=...)` 可读取网页或 API 数据。 |
| 发送 POST 请求 | `requests.post(url, json=..., timeout=...)` 会将字典编码成 JSON，并设置相应的 `Content-Type`。 |
| 读取响应 | `status_code` 查看 HTTP 状态码，`text` 读取原文，`json()` 将 JSON 响应解析为 Python 数据。 |
| 安全传递 URL 参数 | 用 `params` 传查询参数，让 `requests` 处理中文、空格等字符的转义，不要手工拼接 URL。 |
| 设置请求头 | 通过 `headers` 传 `User-Agent`；本课的 B 站示例不带请求头会得到 412。 |
| 设置超时并检查响应 | 每个请求都要带 `timeout`；用 `r.ok` 或 `raise_for_status()` 检查 HTTP 层的结果。 |
| 检查业务层结果 | 对 B 站响应还要检查 `data["code"]`，不能只因为 HTTP 状态码是 200 就认定视频存在。 |
| 处理常见请求异常 | `fetch_json()` 分别处理超时、连接错误、HTTP 错误和无效 JSON，并给出可读提示。 |
| 区分 `json=` 与 `data=` | `json=` 发送 JSON，适合本课后续的 AI API 请求；`data=` 通常用于表单或原始请求体。 |

## 关键代码

### 1. 用 `params` 发 GET，并给请求设置超时

```python
def suggest(word):
    r = requests.get(
        "https://www.baidu.com/sugrec",
        params={"prod": "pc", "wd": word},
        timeout=10,
    )
    if r.status_code == 200:
        data = r.json()
        return [item["q"] for item in data.get("g", [])]
    print(f"请求失败，状态码：{r.status_code}")
    return []
```

### 2. 对 HTTP 状态与业务状态分别检查

```python
def bili_info(bvid):
    r = requests.get(
        BILI,
        params={"bvid": bvid},
        headers=BROWSER,
        timeout=10,
    )
    if r.status_code != 200:
        print(f"请求失败，状态码：{r.status_code}")
        return None

    data = r.json()
    if data.get("code") != 0:
        print(f"视频不存在或其他错误，code: {data.get('code')}")
        return None

    video = data["data"]
    return video["title"], video["owner"]["name"], video["stat"]["view"]
```

### 3. 把请求错误转成清楚的提示

```python
def fetch_json(url, params=None, timeout=15):
    try:
        resp = requests.get(
            url, params=params, headers=BROWSER, timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.Timeout:
        print(f"请求超时（{timeout} 秒）")
    except requests.ConnectionError:
        print("无法连接，请检查网络或网址")
    except requests.HTTPError as e:
        print(f"对方返回了错误状态码：{e.response.status_code}")
    except ValueError:
        print("返回的不是合法 JSON")
    return None
```

## 本课最值得记住的坑

| 现象 | 原因 | 处理方式 |
| --- | --- | --- |
| 程序一直停在请求处 | 没有设置 `timeout`，请求可能无限等待 | 给每一个请求设置合理的 `timeout`；调用耗时较长的 AI API 时再适当放宽。 |
| 404 后代码没有立刻抛异常 | `requests.get()` 默认不会因为 4xx/5xx 自动抛出 HTTP 异常 | 检查 `status_code` / `ok`，或调用 `raise_for_status()`。 |
| HTTP 200 但数据取不到 | HTTP 请求成功不代表 API 的业务操作成功 | 继续检查响应 JSON 中 API 自己定义的状态字段。 |
| `.json()` 报解析错误 | 响应可能是 HTML 错误页、登录页或其他非 JSON 内容 | 先看 `r.text[:200]`，确认实际响应内容，再判断请求哪里出错。 |
| 中文或空格参数导致 URL 异常 | 手动拼 URL 没有正确转义参数 | 用 `params` 传入查询参数。 |
| 请求被网站拒绝 | 服务可能要求特定请求头 | 按接口规则设置请求头；遵守服务的访问频率限制，不用伪装请求绕过限制。 |
| 捕获 `except:` 后看不出问题 | 无差别捕获会吞掉程序自身的 bug | 只捕获知道如何处理的异常，不用宽泛捕获掩盖错误。 |

## 练习记录与待补充

源码中已经写出了第 1–3 题的请求示例：读取 UUID、实现百度联想词查询，以及查询 B 站视频信息。源码也保留了后续题目的空白记录，因此不能据此确认这些内容已经完成：

- 第 4 题：亲自比较不设超时与设置超时的行为；目前“我的答案”尚未填写。
- 第 5 题：实现 `post_json()` 并用回声服务确认 JSON 请求体；代码中仍是待完成项。
- 第 6 题：设计重试条件；“该重试的 / 不该重试的”尚未填写。不要无差别重试客户端错误；是否重试应结合错误类型及服务端的限流提示。
- 「问 AI」：找坑题答案、与 AI 的对比及官方文档核对结果没有记录。

## 卡在哪（根据现有记录）

- **卡了最久的地方**：文件没有记录具体卡点，不能据此推断。
- **卡了多久**：没有记录。
- **最后怎么通的**：没有记录是否查文档或问过 AI。
- **现在还是不确定的**：源码提出了 `timeout` 中连接超时与读取超时的区别，但没有留下核对结果；可以结合 requests 官方文档补记。

## 明天要注意

- 优先补完第 4、5 题，尤其完成第 5 题的 `post_json()`，因为第 18 课会直接用到它。
- 调试 JSON 解析问题时，先确认 HTTP 状态和响应正文，再调用 `.json()`。
- 设计重试时先判断失败原因；不要把认证失败、参数错误或限流等所有情况都当作可以立即重试。
- 在 `post_json()` 中沿用本课的边界：设置超时、检查 HTTP 状态、解析 JSON，并只处理明确知道如何应对的异常。

## 一句话总结

第 17 课的核心是：用 `requests` 发 HTTP 请求并读取响应；每次请求都设置超时，同时检查 HTTP 状态和 API 的业务状态，再按具体异常给出明确处理。
