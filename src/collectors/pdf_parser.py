#!/usr/bin/env python3
"""PDF 기출문제 파서 — pypdf 기반.

세무사 1·2차 시험지 PDF에서 텍스트 추출 + 메타(year/type/subject) 자동 인식.
data/exams/raw/ 하위 모든 PDF를 스캔하여 data/exams/{subject_id}/{year}.md 로 저장.
"""

import argparse
import json
import logging
import re
import unicodedata
from pathlib import Path

import pypdf

logger = logging.getLogger("luxembourg.pdf_parser")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "exams" / "raw"
OUT_DIR = BASE_DIR / "data" / "exams"

# 1차 / 2차 / 합본 패턴
TYPE_PATTERNS = {
    "2차": re.compile(r"2\s*차"),
    "1차": re.compile(r"1\s*차"),
}

# 과목 키워드 → 표준 ID
SUBJECT_KEYWORDS = [
    # 2차
    (re.compile(r"회계학\s*1\s*부|회계학1부"), ("accounting1", "회계학 1부", "2차")),
    (re.compile(r"회계학\s*2\s*부|회계학2부"), ("accounting2", "회계학 2부", "2차")),
    (re.compile(r"세법학\s*1\s*부|세법학1부"), ("tax_law1", "세법학 1부", "2차")),
    (re.compile(r"세법학\s*2\s*부|세법학2부"), ("tax_law2", "세법학 2부", "2차")),
    # 1차 선택과목
    (re.compile(r"행정소송법"), ("admin_litigation", "행정소송법", "1차")),
    (re.compile(r"민\s*법"), ("civil_law", "민법", "1차")),
    (re.compile(r"상\s*법"), ("commercial_law", "상법", "1차")),
    # 1차 1교시 (재정학 + 세법학개론 + 회계학개론 + 영어 합본 흔히)
    (re.compile(r"재정학"), ("public_finance", "재정학", "1차")),
    (re.compile(r"세법학개론"), ("tax_intro", "세법학개론", "1차")),
    (re.compile(r"회계학개론"), ("accounting_intro", "회계학개론", "1차")),
]

# 교시 → 2차 과목 (표준 매핑: 1교시=회계1, 2교시=회계2, 3교시=세법1, 4교시=세법2)
GYOSI_TO_SUBJECT = {
    1: ("accounting1", "회계학 1부"),
    2: ("accounting2", "회계학 2부"),
    3: ("tax_law1", "세법학 1부"),
    4: ("tax_law2", "세법학 2부"),
}

YEAR_RE = re.compile(r"(20\d{2})")
ROUND_RE = re.compile(r"제\s*(\d{2,3})\s*회")
GYOSI_RE = re.compile(r"(\d)\s*교시")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def detect_meta(pdf_path: Path) -> dict:
    """파일 경로(폴더+파일명)에서 메타 추출 + PDF 첫 페이지 단서로 보강."""
    parent = _nfc(pdf_path.parent.name)
    name = _nfc(pdf_path.stem)
    full = f"{parent} {name}"

    meta = {
        "year": None,
        "round": None,
        "type": None,
        "subject_id": None,
        "subject_kr": None,
        "gyosi": None,
        "raw_label": name,
    }

    # 연도
    m = YEAR_RE.search(full)
    if not m:
        # 부모 디렉토리의 부모 (raw/2024/...)에서 추출
        m = YEAR_RE.search(_nfc(pdf_path.parent.parent.name))
    if m:
        meta["year"] = int(m.group(1))

    # 회차
    m = ROUND_RE.search(full)
    if m:
        meta["round"] = int(m.group(1))

    # 1차/2차
    for type_label, pattern in TYPE_PATTERNS.items():
        if pattern.search(full):
            meta["type"] = type_label
            break

    # 교시
    m = GYOSI_RE.search(full)
    if m:
        meta["gyosi"] = int(m.group(1))

    # 과목 — 키워드 우선
    for kw_re, (sid, skr, stype) in SUBJECT_KEYWORDS:
        if kw_re.search(full):
            meta["subject_id"] = sid
            meta["subject_kr"] = skr
            if not meta["type"]:
                meta["type"] = stype
            break

    # 과목 미확정 + 2차 + 교시 알면 매핑
    if not meta["subject_id"] and meta.get("type") == "2차" and meta.get("gyosi") in GYOSI_TO_SUBJECT:
        sid, skr = GYOSI_TO_SUBJECT[meta["gyosi"]]
        meta["subject_id"] = sid
        meta["subject_kr"] = skr

    # PDF 첫 페이지 헤더로 보강 (overrides 안 함, 미정일 때만)
    if not meta["subject_id"] or not meta["year"]:
        try:
            r = pypdf.PdfReader(pdf_path)
            head = r.pages[0].extract_text()[:600] if r.pages else ""
            head_nfc = _nfc(head)
            if not meta["year"]:
                m = YEAR_RE.search(head_nfc)
                if m:
                    meta["year"] = int(m.group(1))
            if not meta["round"]:
                m = ROUND_RE.search(head_nfc)
                if m:
                    meta["round"] = int(m.group(1))
            if not meta["type"]:
                for type_label, pattern in TYPE_PATTERNS.items():
                    if pattern.search(head_nfc):
                        meta["type"] = type_label
                        break
            if not meta["subject_id"]:
                for kw_re, (sid, skr, stype) in SUBJECT_KEYWORDS:
                    if kw_re.search(head_nfc):
                        meta["subject_id"] = sid
                        meta["subject_kr"] = skr
                        if not meta["type"]:
                            meta["type"] = stype
                        break
            if not meta["gyosi"]:
                m = GYOSI_RE.search(head_nfc)
                if m:
                    meta["gyosi"] = int(m.group(1))
                    if not meta["subject_id"] and meta.get("type") == "2차":
                        if meta["gyosi"] in GYOSI_TO_SUBJECT:
                            sid, skr = GYOSI_TO_SUBJECT[meta["gyosi"]]
                            meta["subject_id"] = sid
                            meta["subject_kr"] = skr
        except Exception as e:
            logger.warning("헤더 읽기 실패 %s: %s", pdf_path.name, e)

    return meta


def extract_text(pdf_path: Path) -> str:
    """PDF 전체 텍스트 추출."""
    r = pypdf.PdfReader(pdf_path)
    chunks = []
    for i, page in enumerate(r.pages):
        try:
            t = page.extract_text() or ""
        except Exception as e:
            logger.warning("페이지 %d 추출 실패: %s", i + 1, e)
            t = ""
        chunks.append(t.strip())
    return "\n\n".join(chunks)


def to_markdown(meta: dict, text: str) -> str:
    """추출 텍스트를 markdown으로 정리. 문제 헤딩(##) 자동 부여."""
    head = []
    head.append(f"# {meta['year']}년 제{meta['round']}회 세무사 {meta['type']} — {meta['subject_kr']}")
    head.append("")
    head.append(f"> 출처: 한국산업인력공단 Q-Net (원본 PDF)")
    head.append(f"> 적용 법령 시점: {meta['year']}-01-01 (시험일 기준)")
    head.append("")

    # 【문제 N】 패턴을 ## [문제 N]로 변환
    body = re.sub(
        r"【\s*문제\s*(\d+)\s*】",
        r"\n\n## [문제 \1]\n\n",
        text,
    )
    # 물음 N) 패턴 강조
    body = re.sub(
        r"\b물음\s*(\d+)\)",
        r"\n\n**물음 \1)**",
        body,
    )

    return "\n".join(head) + "\n" + body.strip() + "\n"


def parse_one(pdf_path: Path) -> tuple[dict, Path | None]:
    """단일 PDF 파싱 → 메타 + 출력 경로 반환."""
    meta = detect_meta(pdf_path)
    if not meta["year"] or not meta["subject_id"] or not meta["type"]:
        return meta, None

    out_dir = OUT_DIR / meta["subject_id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{meta['year']}.md"

    text = extract_text(pdf_path)
    md = to_markdown(meta, text)
    out_path.write_text(md, encoding="utf-8")
    return meta, out_path


def parse_all(filter_type: str = None) -> list[dict]:
    """raw/ 하위 모든 PDF 파싱."""
    results = []
    pdfs = sorted(RAW_DIR.rglob("*.pdf"))
    for pdf in pdfs:
        try:
            meta, out = parse_one(pdf)
            entry = {
                "pdf": str(pdf.relative_to(BASE_DIR)),
                "meta": meta,
                "output": str(out.relative_to(BASE_DIR)) if out else None,
            }
            if filter_type and meta.get("type") != filter_type:
                entry["skipped"] = f"type filter {filter_type}"
                results.append(entry)
                continue
            results.append(entry)
            if out:
                logger.info("OK %s/%s → %s", meta.get("year"), meta.get("subject_id"), out.name)
            else:
                logger.warning("UNKNOWN: %s — meta=%s", pdf.name, meta)
        except Exception as e:
            logger.error("FAIL %s: %s", pdf.name, e)
            results.append({"pdf": str(pdf.relative_to(BASE_DIR)), "error": str(e)})
    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, help="단일 PDF만 파싱")
    parser.add_argument("--type", choices=["1차", "2차"], help="해당 type만 처리")
    parser.add_argument("--report", action="store_true", help="요약만 출력")
    args = parser.parse_args()

    if args.file:
        meta, out = parse_one(Path(args.file))
        print(json.dumps({"meta": meta, "output": str(out) if out else None}, ensure_ascii=False, indent=2))
    else:
        results = parse_all(filter_type=args.type)
        ok = [r for r in results if r.get("output")]
        unknown = [r for r in results if not r.get("output") and not r.get("error")]
        errors = [r for r in results if r.get("error")]
        print(f"\n총 {len(results)}건 — OK {len(ok)} / UNKNOWN {len(unknown)} / ERROR {len(errors)}")
        if unknown and args.report:
            print("\n[UNKNOWN]")
            for r in unknown:
                print(f"  {r['pdf']} — meta={r['meta']}")
        if errors:
            print("\n[ERROR]")
            for r in errors:
                print(f"  {r['pdf']}: {r['error']}")
