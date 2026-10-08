"""彙整多次試跑：自動檢查、盲評與通過率。

用法：
    python3 evals/aggregate.py prepare 輸出目錄 次數 每次分組數
        依題庫切出每次的執行批次 batch-r{次}-{組}.json，執行者讀這些檔案寫稿。
    python3 evals/aggregate.py judge-input 輸出目錄 分組數
        合併 out-r*-*.json，依題目切成盲評檔 judge-in-{組}.json（同一題的多次輸出放在一起）。
    python3 evals/aggregate.py report 輸出目錄
        跑 check.py、讀 judge-out-*.json，寫出 summary.md 與 results.json。

一題算通過，要每一次輸出都同時通過自動檢查與盲評。
"""
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from check import check_case  # noqa: E402

PROMPT_FILES = ["prompts.json", "additional-prompts.json", "v4-prompts.json"]


def prompts():
    items = []
    for name in PROMPT_FILES:
        items += json.loads((HERE / name).read_text(encoding="utf-8"))
    return items


def prepare(out_dir, reps, groups):
    out_dir.mkdir(parents=True, exist_ok=True)
    items = prompts()
    for r in range(1, reps + 1):
        for g in range(groups):
            batch = items[g::groups]
            path = out_dir / f"batch-r{r}-{g + 1}.json"
            path.write_text(json.dumps(batch, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(items)} 題 × {reps} 次，每次 {groups} 組，批次寫在 {out_dir}")


def load_outputs(out_dir):
    runs = defaultdict(dict)
    for path in sorted(out_dir.glob("out-r*-*.json")):
        rep = int(path.stem.split("-")[1][1:])
        for case in json.loads(path.read_text(encoding="utf-8")):
            runs[case["id"]][rep] = case
    return runs


def judge_input(out_dir, groups):
    runs = load_outputs(out_dir)
    by_id = {p["id"]: p for p in prompts()}
    ids = [p["id"] for p in prompts() if p["id"] in runs]
    for g in range(groups):
        chunk = []
        for cid in ids[g::groups]:
            entry = {"id": cid, "request": by_id[cid]["request"], "runs": []}
            if "followup" in by_id[cid]:
                entry["followup"] = by_id[cid]["followup"]
            for rep, case in sorted(runs[cid].items()):
                run = {"rep": rep, "output": case["output"]}
                if case.get("followup_output"):
                    run["followup_output"] = case["followup_output"]
                entry["runs"].append(run)
            chunk.append(entry)
        path = out_dir / f"judge-in-{g + 1}.json"
        path.write_text(json.dumps(chunk, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(ids)} 題切成 {groups} 份盲評檔")


def report(out_dir):
    runs = load_outputs(out_dir)
    judged = {}
    for path in out_dir.glob("judge-out-*.json"):
        for v in json.loads(path.read_text(encoding="utf-8")):
            judged[(v["id"], int(v["rep"]))] = v
    rows, disagreements, results = [], [], []
    order = [p["id"] for p in prompts() if p["id"] in runs]
    for cid in order:
        reps = sorted(runs[cid])
        check_ok = judge_ok = 0
        for rep in reps:
            errors = check_case(runs[cid][rep])
            j = judged.get((cid, rep))
            j_pass = j is not None and j["verdict"] == "pass"
            check_ok += not errors
            judge_ok += j_pass
            if (not errors) != j_pass:
                disagreements.append((cid, rep, "；".join(errors) or "通過", j["reason"] if j else "沒有盲評結果"))
            results.append({"id": cid, "rep": rep, "check": "pass" if not errors else "fail",
                            "check_errors": errors, "judge": j["verdict"] if j else "missing",
                            "judge_reason": j["reason"] if j else ""})
        n = len(reps)
        final = "pass" if check_ok == n and judge_ok == n else "fail"
        rows.append((cid, f"{check_ok}/{n}", f"{judge_ok}/{n}", final))

    passed = sum(r[3] == "pass" for r in rows)
    lines = ["# 試跑彙整", "",
             f"每題 {max(len(v) for v in runs.values())} 次，每一次都要同時通過自動檢查與盲評才算通過。",
             "", f"通過 {passed} / {len(rows)} 題。", "",
             "| 題目 | 自動檢查 | 盲評 | 結果 |", "| --- | --- | --- | --- |"]
    lines += [f"| {cid} | {c} | {j} | {f} |" for cid, c, j, f in rows]
    lines += ["", "## 自動檢查與盲評不一致", ""]
    if disagreements:
        lines += ["| 題目 | 次 | 自動檢查 | 盲評理由 |", "| --- | --- | --- | --- |"]
        lines += [f"| {cid} | {rep} | {c} | {j} |" for cid, rep, c, j in disagreements]
    else:
        lines.append("沒有。")
    fails = [r for r in results if r["check"] == "fail" or r["judge"] != "pass"]
    lines += ["", "## 未通過的輸出", ""]
    if fails:
        for r in fails:
            why = "；".join(r["check_errors"]) or r["judge_reason"]
            lines.append(f"- {r['id']} 第 {r['rep']} 次：自動檢查 {r['check']}，盲評 {r['judge']}。{why}")
    else:
        lines.append("沒有。")
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, target = sys.argv[1], Path(sys.argv[2])
    if cmd == "prepare":
        prepare(target, int(sys.argv[3]), int(sys.argv[4]))
    elif cmd == "judge-input":
        judge_input(target, int(sys.argv[3]))
    elif cmd == "report":
        report(target)
    else:
        sys.exit(__doc__)
