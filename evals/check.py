"""像我本人的自動檢查。

用法：
    python3 evals/check.py 輸出檔.json [輸出檔2.json ...]
    python3 evals/check.py --spec 某次試跑/checks.json 輸出檔.json ...

每次試跑的資料夾裡會存一份當時的 checks.json，重現舊結果時用 --spec 指定它。

輸出檔格式：[{"id": "R01", "output": "...", "followup_output": "..."}]
也可以直接吃 runs/*.json 裡某一輪的 cases 陣列。

這支腳本只檢查程式判斷得了的條件：標點、敬稱、對岸用詞、必留資料、
原文不動、正文外說明、段落數、項目數與長度。內容有沒有補事實、語氣像不像作者，
交給盲評（judge-prompt.md）。

結束碼：全部通過為 0，有任何失敗為 1。
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC = HERE / "checks.json"


def load_specs(path=None):
    return json.loads(Path(path or DEFAULT_SPEC).read_text(encoding="utf-8"))

CJK = r"一-鿿"
HALF_PUNCT = re.compile(rf"[{CJK}][,.;:?!]|[,.;:?!][{CJK}]")
URL = re.compile(r"https?://\S+")
INLINE_CODE = re.compile(r"`[^`]*`")
FENCE = re.compile(r"```.*?```", re.S)
MAINLAND = ["視頻", "信息", "軟件", "硬件", "默認", "設置", "網絡", "質量", "數據庫", "服務器", "屏幕"]
META = ["以下是", "修改後的", "改好了", "希望這", "如有需要", "有需要再", "我幫你", "供你參考"]
NOTE_START = ("（", "(", "提醒", "註：", "註:", "說明：", "備註", "正文外")
ITEM = re.compile(r"^\s*(\d+[.、)）]|[-*•])\s*")
MD = re.compile(r"(\*\*|^#{1,6}\s|^\s*\d+[.、)]\s)", re.M)


def squash(text):
    return re.sub(r"\s+", "", text)


def chars_only(text):
    """只留中日韓字、英數字，用來比對字詞有沒有被改。"""
    return re.sub(rf"[^{CJK}A-Za-z0-9]", "", text)


def strip_code_and_urls(text):
    text = FENCE.sub(" ", text)
    text = INLINE_CODE.sub(" ", text)
    return URL.sub(" ", text)


def lines(text):
    return [ln.strip() for ln in text.split("\n") if ln.strip()]


def check_text(text, spec, first_output=None):
    errors = []
    flat = squash(text)
    plain = strip_code_and_urls(text)

    # 標點與敬稱
    if "——" in text:
        errors.append("出現破折號「——」")
    if "；" in plain or re.search(rf"[{CJK}];", plain):
        errors.append("出現分號")
    hp = HALF_PUNCT.findall(plain)
    if hp:
        errors.append(f"中文旁邊出現半形標點：{hp[:3]}")
    if "您" in text and not spec.get("allow_nin"):
        errors.append("出現「您」")
    allowed_terms = set(spec.get("allow_terms", []))
    found = [w for w in MAINLAND if w in text and w not in allowed_terms]
    if found:
        errors.append(f"對岸用詞：{found}")

    # 聊天殘留與正文外說明
    meta = [w for w in META if w in text]
    if meta:
        errors.append(f"聊天殘留：{meta}")
    if not spec.get("allow_notes"):
        notes = [ln for ln in lines(text) if ln.startswith(NOTE_START)]
        if notes:
            errors.append(f"正文外說明：{notes[0][:30]}")

    # 必留與禁用
    for word in spec.get("require", []):
        if squash(word) not in flat:
            errors.append(f"缺少：{word}")
    for group in spec.get("require_any", []):
        if not any(squash(w) in flat for w in group):
            errors.append(f"缺少其中之一：{group}")
    for word in spec.get("forbid", []):
        if squash(word) in flat:
            errors.append(f"不該出現：{word}")

    # 原文不動
    if "exact_input" in spec and flat != squash(spec["exact_input"]):
        errors.append("原句已自然，成稿卻有改動")
    if "same_chars_input" in spec and chars_only(text) != chars_only(spec["same_chars_input"]):
        errors.append("只該動標點或分段，字詞卻有改動")

    # 結構
    body = lines(text)
    if spec.get("fb"):
        labels = [ln for ln in body if ln.startswith("版本")]
        bad = [ln for ln in labels if ln not in ("版本一", "版本二")]
        if bad:
            errors.append(f"版本標示多了說明：{bad[0][:20]}")
        if MD.search(text):
            errors.append("FB 貼文出現 Markdown 或編號")
    if "paragraphs" in spec and len(body) != spec["paragraphs"]:
        errors.append(f"段落數 {len(body)}，應為 {spec['paragraphs']}")
    if "max_items" in spec:
        items = [ln for ln in body if ITEM.match(ln)]
        if len(items) > spec["max_items"]:
            errors.append(f"列了 {len(items)} 項，最多 {spec['max_items']}")
    if "max_chars" in spec and len(flat) > spec["max_chars"]:
        errors.append(f"長度 {len(flat)} 字，上限 {spec['max_chars']}")
    if "cjk_range" in spec:  # 舊版規格（before 批）使用
        n = len(re.findall(rf"[{CJK}]", text))
        lo, hi = spec["cjk_range"]
        if not lo <= n <= hi:
            errors.append(f"中文字數 {n}，應在 {lo}–{hi}")
    if "length_target" in spec:
        target = spec["length_target"]
        lo, hi = round(target * 0.85), round(target * 1.2)
        if not lo <= len(flat) <= hi:
            errors.append(f"字數 {len(flat)}（不含空白），要求約 {target}，應在 {lo}–{hi}")
    if first_output is not None:
        before, after = lines(first_output), body
        for i in spec.get("keep_paragraphs_from_first", []):
            if i >= len(before) or i >= len(after) or squash(before[i]) != squash(after[i]):
                errors.append(f"第 {i + 1} 段應與第一輪一字不差")
    return errors


def check_case(case, specs=None):
    specs = specs if specs is not None else load_specs()
    spec = specs.get(case["id"])
    if spec is None:
        return [f"checks.json 沒有 {case['id']} 的規格"]
    errors = check_text(case["output"], spec)
    if "followup" in spec:
        follow = case.get("followup_output")
        if not follow:
            errors.append("缺少第二輪輸出")
        else:
            merged = {**spec, **spec["followup"]}
            merged.pop("followup", None)
            errors += [f"第二輪：{e}" for e in check_text(follow, merged, first_output=case["output"])]
    return errors


def load(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = list(data.values())
    return data


def main(args):
    spec_path = None
    if args[:1] == ["--spec"]:
        spec_path, args = args[1], args[2:]
    specs = load_specs(spec_path)
    failed = 0
    for path in args:
        for case in load(path):
            errors = check_case(case, specs)
            status = "FAIL" if errors else "pass"
            failed += bool(errors)
            print(f"{status}\t{case['id']}\t{' | '.join(errors) if errors else ''}".rstrip())
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
