"""一键验证：依次运行三个项目的全部自测用例并汇总结果。

用法：python verify.py   （在本目录或任意位置运行均可）
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROJECTS = ["py-automation-kit", "data-clean-pipeline", "offline-analytics-report"]


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except Exception:
        pass

    print("=" * 62)
    print("交付样例 · 一键质量验证（49 条自测用例）")
    print("=" * 62)

    total_passed, total_all, all_ok = 0, 0, True
    for name in PROJECTS:
        project = ROOT / name
        if not (project / "tests").is_dir():
            print(f"[跳过] {name}：找不到 tests 目录")
            all_ok = False
            continue

        started = time.time()
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
            cwd=str(project),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        elapsed = time.time() - started
        output = (proc.stdout or "") + (proc.stderr or "")

        # 从 unittest 输出解析 "Ran N tests"
        ran = 0
        for line in output.splitlines():
            if line.strip().startswith("Ran ") and "tests" in line:
                try:
                    ran = int(line.strip().split()[1])
                except (IndexError, ValueError):
                    pass
        ok = proc.returncode == 0
        total_all += ran
        total_passed += ran if ok else 0
        all_ok = all_ok and ok

        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {name:<26} {ran:>3} 条用例  {elapsed:5.2f}s")
        if not ok:
            print("-" * 62)
            print(output[-2500:])
            print("-" * 62)

    print("-" * 62)
    if all_ok:
        print(f"全部通过：{total_passed}/{total_all} 条用例 OK —— 环境正常，可以交付")
        return 0
    print("存在失败用例，详情见上方输出；请把完整输出发给我们")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
