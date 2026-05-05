"""1차 영역별 단권화 요약 생성기 (A4 1장 압축).

객관식 시험 직전 빠른 회독용 — 한 영역을 5분 내 다시 훑을 수 있도록 핵심만 응축.
"""

import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.summary")

# (subject_id, 한글 라벨, 단권화 영역)
ROTATION = [
    ("public_finance", "재정학", "공공재 이론과 시장실패"),
    ("public_finance", "재정학", "조세귀착과 초과부담"),
    ("tax_intro", "세법학개론", "국세기본법 — 부과·징수·불복"),
    ("tax_intro", "세법학개론", "소득세·법인세 핵심 비교"),
    ("accounting_intro", "회계학개론", "재무제표 요소와 인식·측정"),
    ("accounting_intro", "회계학개론", "수익·비용 인식과 원가 흐름"),
    ("admin_litigation", "행정소송법", "취소소송의 소송요건 (원고적격·처분성)"),
    ("admin_litigation", "행정소송법", "본안판단 — 위법성 판단 기준시"),
]


class SummaryGenerator(BaseGenerator):
    CONTENT_TYPE = "summary"
    PROMPT_NAME = "summary_gen"

    def _select_topic(self):
        from datetime import datetime
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, label, area = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 단권화 영역\n"
            f"- 과목 ID: {subj_id}\n"
            f"- 과목명: {label}\n"
            f"- 영역: {area}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 압축 원칙\n"
            f"- A4 1장 (모바일 5분 회독)\n"
            f"- 표/리스트 위주, 서술 최소화\n"
            f"- 함정 포인트 별도 섹션\n"
            f"- 조문 번호·판례 사건번호 정확히\n"
        )

    def fallback_content(self) -> str:
        subj_id, label, area = self._select_topic()
        fm = self.frontmatter(
            title=f"[fallback] {label} 단권화 — {area} ({self.date_str})",
            date_str=self.date_str,
            category="summary",
            subjects=[subj_id],
            topics=[area],
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback.",
        )
        return fm + f"## {area}\n\nfallback placeholder. Claude CLI 재실행 필요.\n"
