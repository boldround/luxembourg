"""기출문제 풀이/모범답안 생성기.

입력: data/exams/{subject}/{year}.md (hwpx_parser 출력)
출력: site/_posts/{date}-exam-{year}-{subject}.md (단계별 풀이)

각 기출 파일에서 문제 단위로 분리하고, 문제마다 Claude CLI로 풀이 생성.
회계학(계산형)은 calculation 레이아웃, 세법학(논술형)은 post 레이아웃.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.exam_solver")

SUBJECT_TO_LAYOUT = {
    # 회계학도 layout: post 사용 (calc-step HTML 강제 시 Claude CLI 출력 형식 깨짐 → fallback 다수).
    # 단계 풀이는 markdown ### 헤딩으로 표현하면 안정적이고 모바일 가독성도 양호.
    "accounting1": "post",
    "accounting2": "post",
    "tax_law1": "post",
    "tax_law2": "post",
    "admin_litigation": "post",
}

SUBJECT_KR = {
    "accounting1": "회계학 1부",
    "accounting2": "회계학 2부",
    "tax_law1": "세법학 1부",
    "tax_law2": "세법학 2부",
}


class ExamSolverGenerator(BaseGenerator):
    """기출문제 풀이 생성기.

    하나의 (year, subject) 조합에 대해 모든 문제를 풀어 단일 markdown 파일로 출력.
    문제 분리는 hwpx_parser가 만든 markdown의 헤딩(##) 기준.
    """

    CONTENT_TYPE = "exam"
    PROMPT_NAME = "exam_solver"

    def __init__(self, year: int, subject: str, date_str: str = None):
        super().__init__(date_str)
        self.year = year
        self.subject = subject
        self.subject_kr = SUBJECT_KR.get(subject, subject)
        self.layout = SUBJECT_TO_LAYOUT.get(subject, "post")
        self.exam_md_path = self.data_dir / "exams" / subject / f"{year}.md"

    def output_path(self) -> Path:
        return self.posts_dir / f"{self.date_str}-exam-{self.year}-{self.subject}.md"

    def build_context(self) -> str:
        if not self.exam_md_path.exists():
            raise FileNotFoundError(f"파싱된 기출 없음: {self.exam_md_path}")
        exam_text = self.exam_md_path.read_text(encoding="utf-8")
        return (
            f"# 컨텍스트\n\n"
            f"## 시험 정보\n"
            f"- 연도: {self.year}\n"
            f"- 과목: {self.subject_kr} ({self.subject})\n"
            f"- 적용 법령 시점: {self.year}-01-01 (시험일 기준 시행 법령)\n"
            f"- 출력 layout: {self.layout}\n\n"
            f"## 원본 기출문제\n\n"
            f"{exam_text}\n"
        )

    def fallback_content(self) -> str:
        fm = self.frontmatter(
            title=f"[fallback] {self.year}년 {self.subject_kr} 기출 풀이",
            date_str=self.date_str,
            category="exam",
            subjects=[self.subject],
            applied_date=f"{self.year}-01-01",
            excerpt="자동 생성 fallback. Claude CLI 재실행 필요.",
            layout=self.layout,
            extra={
                "exam_year": self.year,
                "exam_round": None,
                "exam_type": "2차",
            },
        )
        return fm + f"## 풀이 생성 실패\n\n원본: `{self.exam_md_path.relative_to(self.base_dir)}`\n"


def list_available_exams(base_dir: Path = None) -> list[tuple[int, str]]:
    """data/exams/{subject}/{year}.md 패턴으로 사용 가능한 (year, subject) 목록 반환."""
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent.parent
    exams_dir = base_dir / "data" / "exams"
    result = []
    for subj_dir in exams_dir.iterdir():
        if not subj_dir.is_dir() or subj_dir.name.startswith("_") or subj_dir.name in {"raw"}:
            continue
        for md in subj_dir.glob("*.md"):
            try:
                year = int(md.stem)
            except ValueError:
                continue
            result.append((year, subj_dir.name))
    return sorted(result)


if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=False, help="없으면 사용 가능한 모든 (year, subject) 처리")
    parser.add_argument("--subject", choices=list(SUBJECT_KR.keys()))
    parser.add_argument("--date", default=None, help="포스트 발행일 (기본: 오늘)")
    args = parser.parse_args()

    if args.year and args.subject:
        targets = [(args.year, args.subject)]
    else:
        targets = list_available_exams()
        if not targets:
            print("사용 가능한 기출 없음 — data/exams/{subject}/{year}.md 가 필요")
            exit(1)
        print(f"발견: {len(targets)}건")

    for year, subject in targets:
        gen = ExamSolverGenerator(year=year, subject=subject, date_str=args.date)
        try:
            out = gen.generate()
            print(f"OK: {out}")
        except Exception as e:
            print(f"FAIL ({year}/{subject}): {e}")
