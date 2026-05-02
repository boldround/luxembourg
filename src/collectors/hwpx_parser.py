#!/usr/bin/env python3
"""
HWP/HWPX 파서 — 세무사 시험 기출문제 → Markdown 변환

HWPX 파일(ZIP 아카이브) 및 HWP 파일(OLE 바이너리)에서 텍스트를 추출하고,
과목/연도/문제 구조를 파싱하여 Markdown + _index.json으로 출력한다.

세무사 2차 시험 4과목 (회계학 1·2부, 세법학 1·2부)을 지원한다.

사용법:
    python3 hwpx_parser.py                    # raw 디렉토리 전체 파싱
    python3 hwpx_parser.py --file path.hwpx   # 단일 파일 파싱
    python3 hwpx_parser.py --type 2차          # 2차시험만 파싱
"""

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


def _nfc(s: str) -> str:
    """macOS HFS+ 파일명은 NFD로 저장됨 → NFC 정규화."""
    return unicodedata.normalize("NFC", s)


# ── 경로 설정 ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DIR = BASE_DIR / "data" / "exams" / "raw"
OUT_DIR = BASE_DIR / "data" / "exams"

# ── 과목 매핑 ──────────────────────────────────────────────
# 세무사 2차 4과목 (공백 유무 두 형태 모두 지원)
SUBJECT_MAP = {
    "회계학1부": ("accounting1", "회계학 1부"),
    "회계학 1부": ("accounting1", "회계학 1부"),
    "회계학2부": ("accounting2", "회계학 2부"),
    "회계학 2부": ("accounting2", "회계학 2부"),
    "세법학1부": ("tax_law1", "세법학 1부"),
    "세법학 1부": ("tax_law1", "세법학 1부"),
    "세법학2부": ("tax_law2", "세법학 2부"),
    "세법학 2부": ("tax_law2", "세법학 2부"),
}


# ── XHTML 텍스트 추출 (hwp5html 출력용) ──────────────────
class _XHTMLTextExtractor(HTMLParser):
    """XHTML에서 텍스트만 추출하는 HTML 파서."""

    def __init__(self):
        super().__init__()
        self._texts: list[str] = []
        self._skip = False
        self._skip_tags = {"style", "script", "link"}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True
        # <p> 태그 시작 시 줄바꿈 삽입 (블록 요소 구분)
        if tag == "p":
            self._texts.append("\n")
        # <td> 태그로 표 셀 구분
        if tag == "td":
            self._texts.append(" ")

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            # \r 제거, 의미 있는 텍스트만 추가
            cleaned = data.replace("\r", "")
            if cleaned.strip():
                self._texts.append(cleaned)

    def get_text(self) -> str:
        return "".join(self._texts)


def extract_text_from_xhtml(xhtml_path: Path) -> str:
    """hwp5html이 생성한 index.xhtml에서 텍스트를 추출한다."""
    content = xhtml_path.read_text(encoding="utf-8")
    parser = _XHTMLTextExtractor()
    parser.feed(content)
    return parser.get_text()


# ── HWP 텍스트 추출 (hwp5html 사용) ──────────────────────
def extract_text_from_hwp(hwp_path: Path) -> str:
    """hwp5html CLI로 HWP 파일에서 텍스트를 추출한다."""
    tmpdir = tempfile.mkdtemp(prefix="hwp_parse_")
    try:
        output_dir = Path(tmpdir) / "output"
        result = subprocess.run(
            ["hwp5html", str(hwp_path), "--output", str(output_dir)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"    ! hwp5html 오류: {result.stderr[:200]}")
            return ""

        xhtml_path = output_dir / "index.xhtml"
        if not xhtml_path.exists():
            print(f"    ! index.xhtml 없음")
            return ""

        return extract_text_from_xhtml(xhtml_path)
    except subprocess.TimeoutExpired:
        print(f"    ! hwp5html 타임아웃")
        return ""
    except Exception as e:
        print(f"    ! HWP 추출 오류: {e}")
        return ""
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── HWPX 텍스트 추출 ─────────────────────────────────────
def extract_text_from_xml(hwpx_path: Path) -> str:
    """Contents/section0.xml에서 전체 텍스트를 추출한다 (수식 포함)."""
    with zipfile.ZipFile(hwpx_path) as zf:
        xml_data = zf.read("Contents/section0.xml").decode("utf-8")

    root = ET.fromstring(xml_data)
    texts = []
    for elem in root.iter():
        if elem.text and elem.text.strip():
            texts.append(elem.text.strip())
        if elem.tail and elem.tail.strip():
            texts.append(elem.tail.strip())

    return "\n".join(texts)


def extract_text_from_preview(hwpx_path: Path) -> str:
    """Preview/PrvText.txt에서 텍스트를 추출한다 (잘림 가능)."""
    with zipfile.ZipFile(hwpx_path) as zf:
        return zf.read("Preview/PrvText.txt").decode("utf-8")


def extract_text_hwpx(hwpx_path: Path) -> str:
    """XML 우선, 실패 시 Preview fallback."""
    try:
        text = extract_text_from_xml(hwpx_path)
        if len(text) > 100:
            return text
    except Exception:
        pass
    return extract_text_from_preview(hwpx_path)


# ── 통합 텍스트 추출 ─────────────────────────────────────
def extract_text(file_path: Path) -> str:
    """파일 확장자에 따라 적절한 추출 방법을 선택한다."""
    ext = file_path.suffix.lower()
    if ext == ".hwpx":
        return extract_text_hwpx(file_path)
    elif ext == ".hwp":
        return extract_text_from_hwp(file_path)
    else:
        print(f"    ! 지원하지 않는 형식: {ext}")
        return ""


# ── 과목 감지 ─────────────────────────────────────────────
def detect_subject(filename: str) -> tuple[str, str] | None:
    """파일명에서 과목을 감지한다. (slug, korean_name) 반환."""
    name = _nfc(filename)

    # 더 긴 키워드(공백 포함)부터 매칭하여 부분일치 충돌 방지
    for keyword, (slug, kr_name) in sorted(
        SUBJECT_MAP.items(), key=lambda x: -len(x[0])
    ):
        if keyword in name:
            return slug, kr_name
    return None


# ── 연도 감지 ─────────────────────────────────────────────
def detect_year(text: str, filename: str, parent_dir: str = "") -> int | None:
    """텍스트, 파일명, 또는 부모 디렉토리명에서 시험 연도를 추출한다."""
    # 텍스트에서 "2025년도" 같은 패턴
    text_nfc = _nfc(text)
    m = re.search(r"(20\d{2})\s*년도?", text_nfc)
    if m:
        return int(m.group(1))

    # 파일명에서 "250704" → 2025
    filename_nfc = _nfc(filename)
    m = re.search(r"(\d{2})(\d{4})", filename_nfc)
    if m:
        yy = int(m.group(1))
        year = 2000 + yy if yy < 50 else 1900 + yy
        return year

    # 부모 디렉토리에서 "2013년" 같은 패턴
    dir_nfc = _nfc(parent_dir)
    m = re.search(r"(20\d{2})\s*년", dir_nfc)
    if m:
        return int(m.group(1))

    return None


# ── 텍스트 정리 ───────────────────────────────────────────
def clean_text(text: str) -> str:
    """추출 텍스트의 아티팩트를 정리한다."""
    # 수식 마커 정리
    text = re.sub(r"수식입니다\.\n?", "", text)
    # "묶음 개체입니다." 제거
    text = re.sub(r"묶음 개체입니다\.?\n?", "", text)

    lines = text.split("\n")
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # 빈 줄은 하나만 유지
        if not stripped:
            if cleaned and cleaned[-1] == "":
                continue
            cleaned.append("")
            continue
        # 과목명만 있는 짧은 줄 (페이지 헤더 등) 건너뛰기
        if stripped in (
            "회계학", "회 계 학",
            "회계학1부", "회계학 1부", "회계학2부", "회계학 2부",
            "세법학", "세 법 학",
            "세법학1부", "세법학 1부", "세법학2부", "세법학 2부",
        ):
            continue
        # "2025 세무사 제2차" 같은 짧은 헤더
        if re.match(r"^\d{4}\s*(세무사|국가|제\d+회)", stripped) and len(stripped) < 40:
            continue
        # "2025년도 세무사 제2차시험" / "제62회 세무사 자격시험" 형태
        if re.match(
            r"^\d{4}년도?\s*(세무사|국가|5급|제\d+회)", stripped
        ) and len(stripped) < 50:
            continue
        if re.match(r"^제\s*\d+\s*회\s*세무사", stripped) and len(stripped) < 40:
            continue
        # "응시번호" 줄
        if re.match(r"^\s*응시번호\s*:", stripped):
            continue
        # 페이지 번호만 있는 줄
        if re.match(r"^\d{1,2}$", stripped):
            continue
        # "시험출제과장" 등 행정 텍스트 + 산업인력공단
        if re.search(
            r"(시험출제과장|인사혁신처|행정안전부|안전행정부|한국산업인력공단|국세청)",
            stripped,
        ):
            continue
        cleaned.append(stripped)

    text = "\n".join(cleaned)
    # 연속 빈줄 정리
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── 문제 파싱 ─────────────────────────────────────────────
def parse_questions(text: str, subject_slug: str) -> list[dict]:
    """
    텍스트에서 문제 구조를 파싱한다.
    반환: [{"number": 1, "points": 40, "body": "...", "sub_questions": [...]}]
    """
    return _parse_standard(text)


def _parse_standard(text: str) -> list[dict]:
    """세무사 2차 과목 (회계학 1·2부, 세법학 1·2부) 문제 파싱."""
    questions = []

    # "[문제 1]", "[문 1]", "문제 1.", "제 1 문." 등 다양한 패턴 시도
    # 세무사 2차는 일반적으로 "[문제 N]" 또는 "문제 N" 형태가 많음
    patterns = [
        r"\[\s*문제?\s*(\d+)\s*\]",      # [문제 1] / [문 1]
        r"문제\s*(\d+)[\.\s]",            # 문제 1.
        r"제\s*(\d+)\s*문제[\.\s]",       # 제 1 문제.
        r"제\s*(\d+)\s*문[\.\s]",         # 제 1 문.
    ]

    splits = []
    for pattern in patterns:
        splits = list(re.finditer(pattern, text))
        if splits:
            break

    for i, match in enumerate(splits):
        q_num = int(match.group(1))
        start = match.end()
        end = splits[i + 1].start() if i + 1 < len(splits) else len(text)
        q_text = text[start:end].strip()

        # "끝" 제거
        q_text = re.sub(r"\n끝\s*$", "", q_text)

        # 총점 추출
        points_match = re.search(r"\(총\s*(\d+)\s*점\)|\(\s*(\d+)\s*점\)", q_text)
        total_points = None
        if points_match:
            total_points = int(points_match.group(1) or points_match.group(2))

        # 소문제 파싱
        sub_qs = _parse_sub_questions(q_text)

        # 본문 (소문제 시작 전까지)
        first_sub = re.search(r"\n\s*(?:1\)|\(1\)|물음\s*1)", q_text)
        if first_sub:
            body = q_text[: first_sub.start()].strip()
        else:
            body = q_text.strip()

        # 본문에서 "(총 N점)" 제거 (헤딩과 중복)
        body = re.sub(r"\s*\(총\s*\d+\s*점\)\s*", " ", body).strip()

        questions.append({
            "number": q_num,
            "points": total_points,
            "body": body,
            "sub_questions": sub_qs,
        })

    return questions


def _parse_sub_questions(text: str) -> list[dict]:
    """소문제 파싱: "1)", "(1)", "물음 1", "①" 등."""
    sub_qs = []

    # "1)" / "(1)" / "물음 1" 패턴
    pattern = r"(?:^|\n)\s*(?:\((\d+)\)|(\d+)\)|물음\s*(\d+))\s*"
    matches = list(re.finditer(pattern, text))

    for i, match in enumerate(matches):
        sq_num = int(match.group(1) or match.group(2) or match.group(3))
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        sq_text = text[start:end].strip()

        # 점수 추출
        pts_match = re.search(r"\((\d+)\s*점\)", sq_text)
        points = int(pts_match.group(1)) if pts_match else None

        # ① ② 하위 문제 추출
        sub_sub = _parse_circled_numbers(sq_text)

        sub_qs.append({
            "number": sq_num,
            "points": points,
            "text": sq_text,
            "sub_items": sub_sub,
        })

    return sub_qs


def _parse_circled_numbers(text: str) -> list[dict]:
    """① ② 형태 하위 문제 파싱."""
    circled = "①②③④⑤⑥⑦⑧⑨⑩"
    items = []
    pattern = r"([①②③④⑤⑥⑦⑧⑨⑩])\s*"
    matches = list(re.finditer(pattern, text))

    for i, match in enumerate(matches):
        num = circled.index(match.group(1)) + 1
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        item_text = text[start:end].strip()
        items.append({"number": num, "text": item_text})

    return items


# ── Markdown 생성 ─────────────────────────────────────────
def generate_markdown(
    subject_kr: str,
    year: int,
    questions: list[dict],
    exam_title_suffix: str = "세무사 2차시험",
) -> str:
    """파싱된 문제를 Markdown으로 변환한다."""
    lines = [f"# {subject_kr} — {year}년 {exam_title_suffix}", ""]

    for q in questions:
        # 문제 제목
        pts = f" (총 {q['points']}점)" if q.get("points") else ""
        lines.append(f"## 문제 {q['number']}{pts}")
        lines.append("")

        # 본문
        if q.get("body"):
            lines.append(q["body"])
            lines.append("")

        # 소문제
        for sq in q.get("sub_questions", []):
            pts_str = f" ({sq['points']}점)" if sq.get("points") else ""
            lines.append(f"### {sq['number']}){pts_str}")
            lines.append("")
            # 소문제 텍스트에서 점수 표기 제거 (중복 방지)
            sq_text = sq["text"]
            if sq.get("points"):
                sq_text = re.sub(r"\s*\(\d+\s*점\)\s*$", "", sq_text)
            # ① ② 하위 항목이 있으면 구조화
            if sq.get("sub_items"):
                # 하위 항목 전의 텍스트
                first_circled = re.search(r"[①②③④⑤⑥⑦⑧⑨⑩]", sq_text)
                if first_circled:
                    before = sq_text[: first_circled.start()].strip()
                    if before:
                        lines.append(before)
                        lines.append("")
                for item in sq["sub_items"]:
                    circled = "①②③④⑤⑥⑦⑧⑨⑩"[item["number"] - 1]
                    lines.append(f"**{circled}** {item['text']}")
                    lines.append("")
            else:
                lines.append(sq_text)
                lines.append("")

    # 끝 마커 제거
    result = "\n".join(lines)
    result = re.sub(r"\n끝\s*$", "", result)
    return result.rstrip() + "\n"


# ── _index.json 업데이트 ──────────────────────────────────
def update_index(
    subject_slug: str,
    subject_kr: str,
    year: int,
    questions: list[dict],
):
    """_index.json에 새 문제 메타데이터를 추가/갱신한다."""
    subject_dir = OUT_DIR / subject_slug
    index_path = subject_dir / "_index.json"

    if index_path.exists():
        with open(index_path, "r", encoding="utf-8") as f:
            index_data = json.load(f)
    else:
        index_data = {
            "subject": subject_slug,
            "subject_kr": subject_kr,
            "questions": [],
        }

    # 기존 항목 중 같은 year의 항목 제거 (재실행 시 교체)
    existing_questions = [
        q for q in index_data.get("questions", [])
        if q.get("year") != year
    ]

    # 새 항목 추가
    for q in questions:
        body_text = q.get("body", "")
        if not body_text and q.get("sub_questions"):
            body_text = q["sub_questions"][0].get("text", "")
        preview = body_text[:80].replace("\n", " ") if body_text else ""

        entry = {
            "year": year,
            "round": 2,
            "number": q["number"],
            "text_preview": preview,
            "points": q.get("points"),
            "sub_questions": len(q.get("sub_questions", [])),
        }
        existing_questions.append(entry)

    # 연도/문제번호 순 정렬
    existing_questions.sort(key=lambda x: (x.get("year", 0), x.get("number", 0)))
    index_data["questions"] = existing_questions

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(index_data, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return index_path


# ── 단일 파일 처리 ────────────────────────────────────────
def process_file(file_path: Path) -> dict | None:
    """HWP 또는 HWPX 파일 하나를 처리한다."""
    filename = file_path.name
    print(f"  처리 중: {filename}")

    # 과목 감지
    subject_info = detect_subject(filename)
    if not subject_info:
        print(f"    ! 과목 감지 실패: {filename}")
        return None
    subject_slug, subject_kr = subject_info

    # 텍스트 추출
    text = extract_text(file_path)
    if not text or len(text) < 50:
        print(f"    ! 텍스트 추출 실패: {filename}")
        return None

    # 연도 감지 (부모 디렉토리명도 참조)
    parent_dir = file_path.parent.name
    year = detect_year(text, filename, parent_dir)
    if not year:
        print(f"    ! 연도 감지 실패: {filename}")
        return None

    # 텍스트 정리
    cleaned = clean_text(text)

    # 문제 파싱
    questions = parse_questions(cleaned, subject_slug)
    if not questions:
        print(f"    ! 문제 파싱 실패 (0문제): {filename}")
        return None

    # 출력 디렉토리
    subject_dir = OUT_DIR / subject_slug
    subject_dir.mkdir(parents=True, exist_ok=True)

    # Markdown 생성
    md = generate_markdown(subject_kr, year, questions)
    md_path = subject_dir / f"{year}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"    > {md_path.relative_to(BASE_DIR)}")

    # _index.json 업데이트
    idx_path = update_index(subject_slug, subject_kr, year, questions)
    print(f"    > {idx_path.relative_to(BASE_DIR)}")

    total_sub = sum(len(q.get("sub_questions", [])) for q in questions)
    return {
        "subject": subject_slug,
        "year": year,
        "questions": len(questions),
        "sub_questions": total_sub,
        "output": str(md_path),
    }


# ── 디렉토리 스캔 ────────────────────────────────────────
def find_exam_files(
    directory: Path,
    exam_type: str | None = None,
) -> list[Path]:
    """raw 디렉토리에서 HWP/HWPX 파일을 찾는다."""
    files = []
    for ext in ("*.hwp", "*.hwpx"):
        for p in sorted(directory.rglob(ext)):
            if exam_type:
                path_str = _nfc(str(p))
                if exam_type == "2차" and "2차" not in path_str:
                    continue
                if exam_type == "1차" and "1차" not in path_str:
                    continue
            files.append(p)
    # 정렬: 연도 디렉토리 → 파일명 순
    files.sort(key=lambda p: (_nfc(str(p.parent)), _nfc(p.name)))
    return files


# ── CLI ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="HWP/HWPX 파일을 파싱하여 Markdown 기출문제 DB로 변환 (세무사)"
    )
    parser.add_argument(
        "--file", type=str, help="단일 HWP/HWPX 파일 경로"
    )
    parser.add_argument(
        "--type", type=str, choices=["1차", "2차"],
        help="시험 유형 필터 (1차 또는 2차)"
    )
    parser.add_argument(
        "--raw-dir", type=str, default=str(RAW_DIR),
        help=f"원본 파일 디렉토리 (기본: {RAW_DIR})"
    )
    args = parser.parse_args()

    results = []

    if args.file:
        p = Path(args.file).resolve()
        if not p.exists():
            print(f"파일 없음: {p}")
            return
        result = process_file(p)
        if result:
            results.append(result)
    else:
        raw_dir = Path(args.raw_dir)
        if not raw_dir.exists():
            print(f"디렉토리 없음: {raw_dir}")
            return

        files = find_exam_files(raw_dir, exam_type=args.type)
        if not files:
            print("HWP/HWPX 파일을 찾을 수 없습니다.")
            return

        print(f"발견된 파일: {len(files)}개\n")
        for f in files:
            result = process_file(f)
            if result:
                results.append(result)
            print()

    # 요약
    if results:
        print("=" * 60)
        print(f"완료: {len(results)}개 파일 처리")
        print()

        # 과목별 요약
        by_subject: dict[str, list] = {}
        for r in results:
            by_subject.setdefault(r["subject"], []).append(r)

        for subj, items in sorted(by_subject.items()):
            years = sorted(r["year"] for r in items)
            total_q = sum(r["questions"] for r in items)
            total_sq = sum(r["sub_questions"] for r in items)
            year_range = f"{years[0]}-{years[-1]}" if len(years) > 1 else str(years[0])
            print(f"  {subj}: {year_range} ({len(years)}년) — {total_q}문제, {total_sq}소문제")

        # 실패 건 확인
        failed = len(files) - len(results) if not args.file else 0
        if failed > 0:
            print(f"\n  ! 실패: {failed}개 파일")
    else:
        print("처리된 파일이 없습니다.")


if __name__ == "__main__":
    main()
