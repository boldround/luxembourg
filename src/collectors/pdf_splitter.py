#!/usr/bin/env python3
"""1차 합본 PDF 분리 스플리터.

세무사 1차 시험 구성:
- 1교시 = 재정학(1-40) + 세법학개론(41-80) — 합본 1 PDF
- 2교시 = 회계학개론(1-40) + 선택과목(41-80) — 선택과목별 PDF (행정소송법/민법/상법)

이 스크립트는 raw/ 의 1차 PDF를 다음 구조로 분리:
- 1교시: data/exams/public_finance/{year}.md, data/exams/tax_intro/{year}.md
- 2교시: data/exams/accounting_intro/{year}.md (선택과목 markdown은 hwpx_parser가 이미 만든 것 — 필요 시 41-80만 잘라서 갱신)
"""
import argparse
import logging
import re
import unicodedata
from pathlib import Path

import pypdf

logger = logging.getLogger("luxembourg.pdf_splitter")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "exams" / "raw"
OUT_DIR = BASE_DIR / "data" / "exams"

YEAR_RE = re.compile(r"(20\d{2})")
ROUND_RE = re.compile(r"제\s*(\d{2,3})\s*회")
GYOSI_RE = re.compile(r"(\d)\s*교시")

# 문제 번호 패턴: "1.", "2.", ... "80." (각 줄 시작 또는 단독)
# 회수에 따라 띄어쓰기 다양 — 좀 느슨하게
PROBLEM_NUM_RE = re.compile(r"(?:^|\n|[^\d])(\d{1,2})\s*\.\s*[<\(]?")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def detect_meta(pdf_path: Path) -> dict:
    parent = _nfc(pdf_path.parent.name)
    name = _nfc(pdf_path.stem)
    full = f"{parent} {name}"

    meta = {"year": None, "round": None, "gyosi": None, "selective": None}

    m = YEAR_RE.search(full) or YEAR_RE.search(_nfc(pdf_path.parent.parent.name))
    if m:
        meta["year"] = int(m.group(1))

    m = ROUND_RE.search(full)
    if m:
        meta["round"] = int(m.group(1))

    m = GYOSI_RE.search(full)
    if m:
        meta["gyosi"] = int(m.group(1))

    # 2교시 선택과목 (괄호 안)
    if "행정소송법" in full:
        meta["selective"] = ("admin_litigation", "행정소송법")
    elif "민법" in full:
        meta["selective"] = ("civil_law", "민법")
    elif "상법" in full:
        meta["selective"] = ("commercial_law", "상법")

    return meta


def extract_text(pdf_path: Path) -> str:
    r = pypdf.PdfReader(pdf_path)
    return "\n\n".join((p.extract_text() or "").strip() for p in r.pages)


def find_problem_position(text: str, problem_num: int) -> int | None:
    """문제 번호 헤더의 시작 위치를 찾음. 가장 그럴듯한 것."""
    # 정확히 "{N}." 형태 + 그 뒤 한 글자가 한글/공백/<(
    pattern = re.compile(rf"(?:^|[^\d]){problem_num}\.\s*[<\(가-힣]")
    matches = list(pattern.finditer(text))
    if not matches:
        return None
    # 가장 첫 매치 (앞에서 등장한 41은 페이지 헤더(30-41) 같은 가짜 매치 제외 위해 좀 뒤에서 찾기 시도)
    return matches[0].start()


def split_1교시(text: str) -> tuple[str, str] | None:
    """1교시 텍스트 → (재정학 1-40, 세법학개론 41-80)."""
    p41 = find_problem_position(text, 41)
    if p41 is None:
        return None
    return text[:p41].strip(), text[p41:].strip()


def split_2교시(text: str) -> tuple[str, str] | None:
    """2교시 텍스트 → (회계학개론 1-40, 선택과목 41-80)."""
    p41 = find_problem_position(text, 41)
    if p41 is None:
        return None
    return text[:p41].strip(), text[p41:].strip()


def to_markdown(year: int, round_: int | None, subject_kr: str, body: str, type_label: str = "1차") -> str:
    head = []
    title_round = f"제{round_}회 " if round_ else ""
    head.append(f"# {year}년 {title_round}세무사 {type_label} — {subject_kr}")
    head.append("")
    head.append(f"> 출처: 한국산업인력공단 Q-Net (원본 PDF, 합본에서 분리)")
    head.append(f"> 적용 법령 시점: {year}-01-01 (시험일 기준)")
    head.append("")
    # 문제 번호를 ## [문제 N]로 정규화
    body_md = re.sub(r"(?:^|\n)(\d{1,2})\.\s*", r"\n\n## [문제 \1]\n\n", body)
    return "\n".join(head) + body_md.strip() + "\n"


def split_one(pdf_path: Path) -> list[Path]:
    meta = detect_meta(pdf_path)
    if not meta["year"] or not meta["gyosi"]:
        logger.warning("메타 부족: %s — %s", pdf_path.name, meta)
        return []

    text = extract_text(pdf_path)
    outputs = []

    if meta["gyosi"] == 1:
        # 재정학 + 세법학개론
        parts = split_1교시(text)
        if not parts:
            logger.warning("1교시 분리 실패: %s", pdf_path.name)
            return []
        pf, ti = parts

        for sid, skr, body in [
            ("public_finance", "재정학", pf),
            ("tax_intro", "세법학개론", ti),
        ]:
            out_dir = OUT_DIR / sid
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"{meta['year']}.md"
            out.write_text(to_markdown(meta["year"], meta["round"], skr, body), encoding="utf-8")
            outputs.append(out)
            logger.info("OK %s/%s", meta["year"], sid)

    elif meta["gyosi"] == 2:
        # 회계학개론 + 선택과목
        parts = split_2교시(text)
        if not parts:
            logger.warning("2교시 분리 실패: %s", pdf_path.name)
            return []
        ai, sel = parts

        # 회계학개론 (40문제)
        out_dir = OUT_DIR / "accounting_intro"
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / f"{meta['year']}.md"
        out.write_text(to_markdown(meta["year"], meta["round"], "회계학개론", ai), encoding="utf-8")
        outputs.append(out)
        logger.info("OK %s/accounting_intro", meta["year"])

        # 선택과목 (회계학개론 빠진 41-80만)
        if meta["selective"]:
            sid, skr = meta["selective"]
            out_dir = OUT_DIR / sid
            out_dir.mkdir(parents=True, exist_ok=True)
            out = out_dir / f"{meta['year']}.md"
            out.write_text(to_markdown(meta["year"], meta["round"], skr, sel), encoding="utf-8")
            outputs.append(out)
            logger.info("OK %s/%s (분리 후 갱신)", meta["year"], sid)

    return outputs


def split_all() -> list[Path]:
    """raw/ 하위 모든 1차 PDF 분리."""
    results = []
    for pdf in sorted(RAW_DIR.rglob("*.pdf")):
        # 1차 PDF만
        full = _nfc(str(pdf))
        if "1차" not in full:
            continue
        try:
            outs = split_one(pdf)
            results.extend(outs)
        except Exception as e:
            logger.error("FAIL %s: %s", pdf.name, e)
    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="단일 PDF만 분리")
    args = parser.parse_args()

    if args.file:
        outs = split_one(Path(args.file))
        for o in outs:
            print(f"  -> {o}")
    else:
        outs = split_all()
        print(f"\n총 {len(outs)}개 markdown 생성")
