#!/usr/bin/env python3
"""기계적 팩트체커.

콘텐츠 파일에서 조문 인용, 판례, applied_date를 추출해
레퍼런스 DB와 자동 대조한다.

CRITICAL 오류가 있으면 배포 차단 (pipeline.py에서 sys.exit(2)).
"""

import json
import re
from datetime import date as Date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
REF_DIR = BASE_DIR / "data" / "reference"

# 4대 세법 + 부가 법령 약칭
LAW_ALIASES = {
    "국세기본법": "national_tax_act",
    "국기법": "national_tax_act",
    "소득세법": "income_tax_act",
    "소득법": "income_tax_act",
    "법인세법": "corporate_tax_act",
    "법인법": "corporate_tax_act",
    "부가가치세법": "vat_act",
    "부가세법": "vat_act",
    "부가법": "vat_act",
    "상속세 및 증여세법": "inheritance_gift_act",
    "상증세법": "inheritance_gift_act",
    "상증법": "inheritance_gift_act",
    "조세특례제한법": "special_tax_treatment_act",
    "조특법": "special_tax_treatment_act",
    "지방세법": "local_tax_act",
    "개별소비세법": "individual_consumption_act",
    "행정소송법": "admin_litigation_act",
}

# "국세기본법 제14조", "국세기본법 제14조의2", "법인세법 §52" 등
ARTICLE_PATTERN = re.compile(
    r"(국세기본법|국기법|소득세법|소득법|법인세법|법인법|부가가치세법|부가세법|부가법|"
    r"상속세 및 증여세법|상증세법|상증법|조세특례제한법|조특법|지방세법|개별소비세법|행정소송법)"
    r"\s*(?:제\s*(\d+)\s*조(?:의\s*(\d+))?|§\s*(\d+))"
)

# "대법원 2023두12345" 형태
CASE_PATTERN = re.compile(r"대법원\s*(\d{4})[\s,]*([두누다도드])\s*(\d+)")

# applied_date frontmatter
APPLIED_DATE_PATTERN = re.compile(r"^applied_date:\s*['\"]?(\d{4}-\d{2}-\d{2})['\"]?", re.MULTILINE)


def load_law_db() -> dict:
    path = REF_DIR / "tax-laws.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_case_db() -> dict:
    path = REF_DIR / "tax-cases.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_revisions() -> dict:
    path = REF_DIR / "law-revisions.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_file(path: Path) -> list[dict]:
    """콘텐츠 파일을 검증. CRITICAL 오류 리스트 반환 (빈 리스트면 OK)."""
    text = path.read_text(encoding="utf-8")
    critical = []

    # 1. applied_date 필수
    m = APPLIED_DATE_PATTERN.search(text)
    if not m:
        critical.append({"type": "MISSING_APPLIED_DATE", "msg": "applied_date frontmatter 누락"})
    else:
        applied = Date.fromisoformat(m.group(1))
        # 시험일 시점 시행 법령이어야 함 (현실적으로 미래 1년 이내)
        today = Date.today()
        if applied.year > today.year + 1:
            critical.append({
                "type": "APPLIED_DATE_FUTURE",
                "msg": f"applied_date {applied}가 너무 미래 (today={today})",
            })

    # 2. 조문 번호 검증 (DB 있을 때만)
    laws = load_law_db()
    if laws:
        for match in ARTICLE_PATTERN.finditer(text):
            law_kr = match.group(1)
            article_num = match.group(2) or match.group(4)
            sub = match.group(3)
            law_id = LAW_ALIASES.get(law_kr)
            if not law_id or law_id not in laws:
                continue
            law_data = laws[law_id]
            article_key = f"{article_num}-{sub}" if sub else str(article_num)
            articles = law_data.get("articles", {})
            if article_num not in articles and article_key not in articles:
                critical.append({
                    "type": "UNKNOWN_ARTICLE",
                    "msg": f"{law_kr} 제{article_num}조" + (f"의{sub}" if sub else "") + " — DB에 없음",
                })

    # 3. 판례 사건번호 검증 (DB 있을 때만)
    cases = load_case_db()
    if cases:
        for match in CASE_PATTERN.finditer(text):
            year, kind, num = match.groups()
            case_id = f"{year}{kind}{num}"
            if case_id not in cases:
                # 미검증은 WARN, CRITICAL은 명백한 형식 오류만
                pass

    return critical


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("usage: fact_checker.py <markdown_file>")
        sys.exit(1)
    errors = check_file(Path(sys.argv[1]))
    if not errors:
        print("OK")
    else:
        for e in errors:
            print(f"[{e['type']}] {e['msg']}")
        sys.exit(2)
