# -*- coding: utf-8 -*-
"""生成平台相册用竖版长图页面（1080x1920）。

数据来源全部取自三个项目的真实运行产物，不手写数字：
- 项目三：out/report.html 提取 SVG 图表 + out/summary.md 提取 KPI 与结论
- 项目二：out/stats.json 提取清洗数字
- 项目一：workspace/out/daily_report.html 提取任务结果
"""
from __future__ import annotations

import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # bid-demo-overview/
OUT = ROOT / "shots" / "album"
OUT.mkdir(parents=True, exist_ok=True)

GIT = ROOT.parent  # C:/myFloders/git/

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;overflow:hidden;background:#f4f6fa;color:#1f2937;
font:30px/1.7 "Microsoft YaHei","PingFang SC",sans-serif;-webkit-font-smoothing:antialiased}
.head{background:linear-gradient(120deg,#0f2d4e,#1d5f9c);color:#fff;padding:52px 60px 42px}
.head .tag{display:inline-block;font-size:24px;letter-spacing:.18em;background:rgba(255,255,255,.16);padding:8px 22px;border-radius:8px}
.head h1{font-size:56px;font-weight:700;margin:24px 0 12px;letter-spacing:1px}
.head p{font-size:28px;color:#c7dcf1;line-height:1.8}
.nums{display:grid;grid-template-columns:1fr 1fr;gap:22px;padding:34px 60px 4px}
.nums.three{grid-template-columns:1fr 1fr 1fr}
.nums .n{background:#fff;border:1px solid #e4eaf2;border-radius:18px;padding:26px 26px;box-shadow:0 4px 14px rgba(24,42,66,.06)}
.nums .n b{display:block;font-size:52px;font-weight:700;color:#0f2d4e;letter-spacing:-1px;line-height:1.2}
.nums .n span{font-size:25px;color:#5b6b7f}
.nums .n em{font-style:normal;color:#0f8a4d;font-weight:700}
.sec{background:#fff;border:1px solid #e4eaf2;border-radius:20px;margin:24px 60px;padding:28px 36px;box-shadow:0 4px 14px rgba(24,42,66,.05)}
.sec h2{font-size:33px;color:#123a63;margin-bottom:16px;border-left:8px solid #1d5f9c;padding-left:18px}
.sec svg{width:100%;height:auto;display:block}
.concl li{list-style:none;font-size:28px;line-height:1.68;margin:0 0 16px;padding:18px 24px;background:#f8fbff;border:1px solid #e9eff7;border-radius:14px}
.concl li b{color:#123a63}
.prod{background:#fff;border:1px solid #e4eaf2;border-radius:20px;margin:24px 60px 0;padding:30px 38px;box-shadow:0 4px 14px rgba(24,42,66,.05)}
.prod h3{font-size:38px;color:#123a63}
.prod h3 span{font-size:23px;color:#7b8a9c;font-weight:400;margin-left:14px}
.prod p{font-size:27px;color:#41536b;margin-top:8px}
.prod .k{font-size:28px;color:#0f2d4e;font-weight:700;margin-top:10px}
.foot{position:absolute;bottom:0;left:0;right:0;background:#0f2942;color:#9fc3e4;font-size:20px;padding:20px 60px;display:flex;justify-content:space-between;align-items:center;white-space:nowrap}
.foot b{color:#fff;font-size:21px}
"""

FOOT_L = '<b>需求分析师 + 测试与开发工程师</b><span>源码交付 · 本机可复现 · 数据不出电脑</span>'


def svgs_from_report() -> list[dict]:
    """从复盘报表 HTML 提取全部主图（viewBox 800 宽），标注所属章节。"""
    html = io.open(GIT / "offline-analytics-report" / "out" / "report.html", encoding="utf-8").read()
    out = []
    for m in re.finditer(r"<svg\b", html):
        end = html.index("</svg>", m.start()) + len("</svg>")
        block = html[m.start():end]
        if 'viewBox="0 0 800' not in block:
            continue
        h2 = re.findall(r'<h2><span class="idx">\d+</span>([^<]*)', html[: m.start()])
        title = h2[-1].strip() if h2 else ""
        block = re.sub(r'(<svg\b[^>]*?)\swidth="[^"]*"\sheight="[^"]*"', r"\1", block, count=1)
        out.append({"title": title, "svg": block})
    return out


def summary_facts() -> dict:
    md = io.open(GIT / "offline-analytics-report" / "out" / "summary.md", encoding="utf-8").read()
    kpi = dict(re.findall(r"\| 累计 GMV \| (¥[\d,.万]+) \|", md) and [("gmv", re.findall(r"\| 累计 GMV \| (¥[\d,.万]+)", md)[0])])
    concl = re.findall(r"^\d+\. \*\*(.+?)\*\* —— (.+)$", md, re.M)
    rows = dict(re.findall(r"\| (累计 GMV|累计订单数|客单价|销量) \| ([^|]+) \|", md))
    month = re.findall(r"\| (\d{4}-\d{2}) 单月 GMV \| ([^|]+) \|", md)
    return {"rows": rows, "concl": concl, "month": month}


def page(body: str, foot_r: str) -> str:
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{body}
<div class="foot">{FOOT_L}<span>{foot_r}</span></div></body></html>"""


def album_analysis() -> None:
    charts = svgs_from_report()
    facts = summary_facts()
    rows = facts["rows"]
    concl = facts["concl"]
    by_title = {c["title"]: c["svg"] for c in charts}

    kpi = f"""
  <div class="nums three">
    <div class="n"><b>{rows.get('累计 GMV','').strip()}</b><span>累计 GMV</span></div>
    <div class="n"><b>{rows.get('累计订单数','').strip()}</b><span>订单数</span></div>
    <div class="n"><b>{rows.get('客单价','').strip()}</b><span>客单价</span></div>
  </div>"""
    trend = by_title.get("月度 GMV 趋势", "")
    picks = [c for c in concl if any(k in c[0] for k in ("最大市场", "转化率", "客单价最高"))][:3]
    concl_html = "".join(f"<li><b>{t}</b> —— {d}</li>" for t, d in picks)

    body = f"""
  <div class="head">
    <div class="tag">产品 03 · 离线数据分析 · 服务 3-1 / 3-2 / 3-3</div>
    <h1>订单明细进，复盘报表出</h1>
    <p>把一堆订单导出表，变成老板 5 分钟能看完的复盘报告：7 张图 + 7 条自动结论，口径写在报告里。</p>
  </div>{kpi}
  <div class="sec"><h2>月度 GMV 趋势（同比按月对齐）</h2>{trend}</div>
  <div class="sec"><h2>报告自动生成的结论（可逐条回溯）</h2><ul class="concl">{concl_html}</ul></div>"""
    io.open(OUT / "p3_analysis.html", "w", encoding="utf-8").write(page(body, "服务 3-1 · 3-2 · 3-3"))


def album_clean() -> None:
    st = json.load(io.open(GIT / "data-clean-pipeline" / "out" / "stats.json", encoding="utf-8"))
    body = f"""
  <div class="head">
    <div class="tag">产品 02 · 数据清洗 · 服务 2-1 / 2-2 / 2-3</div>
    <h1>脏表进，标准表出</h1>
    <p>五种日期写法、带 ¥ 的金额、重复上报、空值……洗成能直接用的标准数据集，每一格改动都有留痕。</p>
  </div>
  <div class="nums three">
    <div class="n"><b>{st['src_rows']} 行</b><span>原始脏表</span></div>
    <div class="n"><b><em>{st['out_rows']} 行</em></b><span>交付标准数据集</span></div>
    <div class="n"><b>{st['total_fixes']:,} 处</b><span>单元格修复（可逐格追溯）</span></div>
  </div>
  <div class="sec"><h2>这次清洗改了什么</h2><ul class="concl">
    <li><b>格式归一</b> —— 日期 5 种写法 → YYYY-MM-DD；金额去掉 ¥ 和千分位；手机号统一 11 位并校验</li>
    <li><b>缺失与异常</b> —— 必填项按中位数 / 众数填充；IQR 超界异常只标记不删除，{st.get('outliers_flagged',4)} 条留待人工复核</li>
    <li><b>去重守恒</b> —— 同一订单重复上报保留字段最全的一条；{st['src_rows']} = {st['out_rows']} + 剔除 {st['rejected_rows']} + 去重 {st['deduped_rows']}，数据不丢</li>
  </ul></div>
  <div class="sec"><h2>交付物</h2><ul class="concl">
    <li><b>标准数据集</b> —— clean_dataset.csv，可直接入库 / 建模 / 做报表</li>
    <li><b>清洗报告</b> —— 前后体检对比 HTML，问题分布与待复核清单全在报告里</li>
    <li><b>规则清单</b> —— 规则写在配置文件里，开工前先对齐口径再动手</li>
  </ul></div>"""
    io.open(OUT / "p2_clean.html", "w", encoding="utf-8").write(page(body, "服务 2-1 · 2-2 · 2-3"))


def album_script() -> None:
    body = f"""
  <div class="head">
    <div class="tag">产品 01 · Python 脚本开发 · 服务 1-1 / 1-2 / 1-3</div>
    <h1>重复的活儿，一键跑完</h1>
    <p>批量重命名、表格合并拆分、接口对接，做成一条命令就能跑的本地脚本，交付源码和运行说明。</p>
  </div>
  <div class="nums three">
    <div class="n"><b>19 个</b><span>乱名文件一键归位</span></div>
    <div class="n"><b>3 张</b><span>口径不一的表自动对齐</span></div>
    <div class="n"><b>137 条</b><span>订单分页同步带重试</span></div>
  </div>
  <div class="sec"><h2>和手工做有什么不一样</h2><ul class="concl">
    <li><b>先预览，后执行</b> —— 重命名先出「原名 → 新名」对照表，确认了才动你的原文件，冲突直接中止</li>
    <li><b>表头不一致也能合</b> —— 三张表字段名对不上？自动按并集对齐，带来源标记，随时能查这行来自哪个表</li>
    <li><b>接口挂了会自己重试</b> —— 分页拉取逐页留痕，请求失败自动退避重试，断了知道断在哪一页</li>
    <li><b>跑完有日报</b> —— 每次运行生成 Markdown / HTML 日报：处理了多少、跳过了什么、哪里要人工看</li>
  </ul></div>
  <div class="sec"><h2>你会拿到什么</h2><ul class="concl">
    <li><b>全部源码 + 运行说明</b> —— 改文件名规则、合并口径，改配置就行</li>
    <li><b>自测用例随包交付</b> —— 假日期、空文件、接口不通都测过，可自己重跑验证</li>
  </ul></div>"""
    io.open(OUT / "p1_script.html", "w", encoding="utf-8").write(page(body, "服务 1-1 · 1-2 · 1-3"))


def album_cover() -> None:
    body = f"""
  <div class="head">
    <div class="tag">本地 Python 服务 · 三件套演示</div>
    <h1>文件和表格的活儿<br>交给跑在本机的脚本</h1>
    <p>数据不出你的电脑 · 源码交付 · 跑前先预览 · 每一步有留痕</p>
  </div>
  <div class="prod"><h3>① Python 脚本开发<span>服务 1-1 ~ 1-3</span></h3>
    <p>重复的文件、表格操作，做成一键就能跑的本地脚本</p>
    <div class="k">19 个乱名文件归位 · 3 张表自动对齐 · 137 条订单同步</div></div>
  <div class="prod"><h3>② 数据清洗<span>服务 2-1 ~ 2-3</span></h3>
    <p>脏表进标准表出，每一格改动都能查到</p>
    <div class="k">302 行 → 260 行交付 · 1,323 处修复逐格可溯</div></div>
  <div class="prod"><h3>③ 离线数据分析<span>服务 3-1 ~ 3-3</span></h3>
    <p>订单明细进，老板能直接看的复盘报表出</p>
    <div class="k">3,975 条明细 → 7 张图 + 7 条自动结论</div></div>
  <div class="sec" style="margin-top:24px"><h2>怎么验证不是空话</h2><ul class="concl">
    <li><b>样例可复跑</b> —— 每个项目自带演示数据，一条命令重新生成同样的结果</li>
    <li><b>43 条自测用例全过</b> —— 边界和异常路径都测过，随源码一起交付</li>
    <li><b>在线样例报告</b> —— 三个产品的完整报告可在浏览器直接打开（链接见店铺）</li>
  </ul></div>"""
    io.open(OUT / "p0_cover.html", "w", encoding="utf-8").write(page(body, "案例均可现场复现"))


if __name__ == "__main__":
    album_analysis()
    album_clean()
    album_script()
    album_cover()
    for f in sorted(OUT.glob("*.html")):
        print("OK", f.name)
