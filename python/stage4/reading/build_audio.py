# 这是 Opus 在 2026-10 帮你做实验讲解视频时写的原版脚本。除了这几行说明，下面的代码一个字没改。
# 来源：~/dev/html/lab-video-src/tools/build_audio.py
# 第 27 课会回头读它：那时你会发现自己已经能看懂大部分，还能挑出它偷懒的地方。
# 不要运行它（它需要命令行参数，还会生成一堆音频文件）。

import json, subprocess, sys, os, wave, array

OUT = sys.argv[1]
os.makedirs(f"{OUT}/audio", exist_ok=True)
VOICE, RATE = "Samantha", "150"

# (scene id, lead-in s, tail s, [(en, zh), ...])
SCENES = [
 ("s1", 0.8, 0.8, [
   ("Mix citric acid with baking soda, and the cup gets colder.", "把柠檬酸和小苏打混合，杯子会变冷。"),
   ("Does more baking soda always make it colder? Let's find out.", "小苏打越多，就一定越冷吗？我们来找出答案。")]),
 ("s2", 0.5, 0.8, [
   ("The reaction is endothermic: it takes in energy from the solution, so the temperature drops.", "这个反应吸热，它从溶液中吸收能量，所以温度下降。"),
   ("One mole of citric acid reacts with exactly three moles of baking soda.", "1 摩尔柠檬酸恰好和 3 摩尔小苏打反应。")]),
 ("s3", 0.5, 1.2, [
   ("In 25 millilitres of 15 percent citric acid, that means 5.22 grams of baking soda.", "在 25 毫升 15% 的柠檬酸溶液里，就是 5.22 克小苏打。"),
   ("Below 5.22 grams, more baking soda gives a bigger temperature drop.", "低于 5.22 克时，小苏打越多，降温越多。"),
   ("Above it, the acid runs out, and the drop levels off.", "超过之后，酸用完了，降温幅度不再增加。")]),
 ("s4", 0.6, 2.0, [
   ("We change only one thing: the mass of baking soda. Six masses, three trials each.", "我们只改变一样东西：小苏打的质量。6 个质量，每个做 3 次。")]),
 ("st1", 0.8, 1.8, [
   ("Step one: make the solution. Dissolve 90 grams of citric acid in water to a total of 600 grams,", "第一步：配溶液。把 90 克柠檬酸溶于水，总质量配到 600 克，"),
   ("then let it return to room temperature.", "再放到回到室温。")]),
 ("st2", 0.8, 2.2, [
   ("Step two: weigh the baking soda samples in advance, and label each one.", "第二步：提前称好每份小苏打，并贴上标签。")]),
 ("st3", 0.8, 1.8, [
   ("Step three: measure 25 millilitres of solution into the cup,", "第三步：量 25 毫升溶液倒入杯中，"),
   ("wait until the temperature is steady, and record it.", "等温度稳定后记录下来。")]),
 ("st4", 0.8, 1.8, [
   ("Step four: tip in all the baking soda at once, put the lid on,", "第四步：把小苏打一次性倒入，盖上盖子，"),
   ("start the stopwatch, and keep stirring.", "开始计时，持续搅拌。")]),
 ("st5", 0.8, 2.2, [
   ("Step five: record the temperature every 15 seconds for three minutes.", "第五步：每 15 秒记录一次温度，持续 3 分钟。"),
   ("The temperature drop is the start minus the lowest reading.", "降温幅度 = 初始温度 − 最低温度。")]),
 ("st6", 0.8, 2.0, [
   ("Step six: rinse and dry the cup, then repeat with the next sample, in a random order.", "第六步：冲洗擦干杯子，按随机顺序做下一份。")]),
 ("s6", 0.6, 3.0, [
   ("Finally, plot the average temperature drop against mass.", "最后，画出平均降温与质量的关系图。"),
   ("If it rises, then levels off near 5.22 grams, our hypothesis is supported.", "如果曲线先上升、在 5.22 克附近变平，假设就得到支持。")]),
]
GAP = 0.35
SR = 22050

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
    return float(r.stdout.strip())

scenes, cues, t, idx = [], [], 0.0, 0
for sid, lead, tail, lines in SCENES:
    start = t
    t += lead
    for en, zh in lines:
        idx += 1
        aiff, wav = f"{OUT}/audio/c{idx:02d}.aiff", f"{OUT}/audio/c{idx:02d}.wav"
        subprocess.run(["say", "-v", VOICE, "-r", RATE, "-o", aiff, en], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", aiff, "-ar", str(SR), "-ac", "1", "-sample_fmt", "s16", wav], check=True)
        d = dur(wav)
        cues.append({"i": idx, "scene": sid, "start": round(t, 3), "end": round(t + d, 3), "en": en, "zh": zh, "wav": wav})
        t += d + GAP
    t += tail - GAP
    scenes.append({"id": sid, "start": round(start, 3), "end": round(t, 3)})

total = t
# assemble narration track
buf = array.array("h", [0] * (int(total * SR) + SR))
for c in cues:
    with wave.open(c["wav"]) as w:
        data = array.array("h", w.readframes(w.getnframes()))
    o = int(c["start"] * SR)
    buf[o:o + len(data)] = data
with wave.open(f"{OUT}/narration.wav", "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(buf.tobytes())

timeline = {"total": round(total, 3), "scenes": scenes, "cues": [{k: v for k, v in c.items() if k != "wav"} for c in cues]}
with open(f"{OUT}/timeline.js", "w", encoding="utf-8") as f:
    f.write("window.TIMELINE = " + json.dumps(timeline, ensure_ascii=False, indent=1) + ";\n")

def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
with open(f"{OUT}/subtitles.srt", "w", encoding="utf-8") as f:
    for n, c in enumerate(cues, 1):
        f.write(f"{n}\n{ts(c['start'])} --> {ts(c['end'] + 0.25)}\n{c['en']}\n{c['zh']}\n\n")

for s in scenes:
    print(f"{s['id']:4s} {s['start']:6.2f} - {s['end']:6.2f}  ({s['end']-s['start']:.1f}s)")
print("TOTAL", round(total, 2))
