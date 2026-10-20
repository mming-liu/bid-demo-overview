# bid-demo-overview · 能力演示总览

给客户 / 评标人看的**单页入口**：不读代码，1 分钟内看懂能做什么、证据在哪、怎么自己验证。

👉 **在线打开总览页**：https://mming-liu.github.io/bid-demo-overview/

---

## 一、这个页面是什么

一张 HTML 页面，把三个真实可运行项目的能力、硬指标和证据集中呈现：

- 三张**真实运行产物截图**（无头浏览器实拍，不是示意图）
- 硬指标：4,425 行源码 / 43 条自测全过 / 0 第三方依赖 / 产物 100% 留痕
- 店铺服务编号 1-1 ~ 3-3 与 demo 功能点的逐条对照，评标人可直接按编号核对
- 「不用信我们，自己跑一遍」的四条命令

## 二、三个项目（点进去看真东西）

| 项目 | 代码仓库 | 在线报表（真 HTML） | 一条命令 |
| --- | --- | --- | --- |
| ① Python 脚本开发 | [py-automation-kit](https://github.com/mming-liu/py-automation-kit) | [打开运行报告](https://mming-liu.github.io/py-automation-kit/) | `python cli.py demo` |
| ② 数据清洗服务 | [data-clean-pipeline](https://github.com/mming-liu/data-clean-pipeline) | [打开清洗报告](https://mming-liu.github.io/data-clean-pipeline/) | `python clean.py --demo` |
| ③ 数据分析服务 | [offline-analytics-report](https://github.com/mming-liu/offline-analytics-report) | [打开复盘报表](https://mming-liu.github.io/offline-analytics-report/) | `python analyze.py --demo` |

三个项目字段口径统一，可串成 `接口同步 → 清洗 → 报表` 的链路，链路已实测跑通。

## 三、本仓库内容

```
bid-demo-overview/
├── index.html     # 能力总览页（单文件，无外部依赖，可直接双击打开）
├── verify.py      # 一键质量验证：跑三个项目共 43 条用例并汇总 PASS/FAIL
└── shots/         # 三个项目 HTML 产物的首屏截图（index.html 引用）
```

## 四、自己验证

```bat
:: 需要三个项目与本仓库放在同一父目录下（verify.py 按同级目录查找）
python verify.py
```

期望输出：

```
[PASS] py-automation-kit           17 条用例
[PASS] data-clean-pipeline         15 条用例
[PASS] offline-analytics-report    11 条用例
全部通过：43/43 条用例 OK —— 环境正常，可以交付
```

只想看页面：双击 `index.html` 即可，无需服务器、无需联网。

## 五、演示顺序建议

1. 打开总览页讲全局（1 分钟）
2. 现场跑 `verify.py`，43 条用例全 PASS（约 15 秒）
3. 按客户关注点现场跑对应 demo（每条约 5–10 秒）
4. 打开在线报表下钻细节（清洗留痕 / 图表 / 口径说明）

---

维护：需求分析师 + 测试与开发工程师 轻量化协作
