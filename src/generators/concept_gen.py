"""세법학 핵심개념 정리 생성기."""

import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.concept")

ROTATION = [
    ("tax_law1", "국세기본법", "실질과세, 신의성실, 부과제척기간, 조세불복"),
    ("tax_law1", "소득세법", "종합소득 vs 분리과세, 양도소득, 인적공제"),
    ("tax_law1", "법인세법", "익금/손금, 세무조정, 부당행위계산부인"),
    ("tax_law1", "상속·증여세법", "포괄증여, 합산과세, 가업상속공제"),
    ("tax_law2", "부가가치세법", "과세대상, 영세율 vs 면세, 매입세액공제"),
    ("tax_law2", "조세특례제한법", "비과세 vs 감면, 사후관리, 일몰조항"),
]


class ConceptGenerator(BaseGenerator):
    CONTENT_TYPE = "concept"
    PROMPT_NAME = "concept_gen"

    def _select_topic(self):
        from datetime import datetime
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, area, themes = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 정리 영역\n- 과목: {subj_id}\n- 영역: {area}\n- 핵심 테마: {themes}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 출력 원칙\n- 두괄식: 핵심 명제 1줄로 요약 후 전개\n"
            f"- 학설 대립 제시 + 실무 통설 명시\n- 판례 핵심구절 1-2줄 정확 인용\n"
            f"- 개정 전후 비교 (필요 시)\n"
        )

    def fallback_content(self) -> str:
        subj_id, area, _ = self._select_topic()
        fm = self.frontmatter(
            title=f"[fallback] {area} 핵심개념 — {self.date_str}",
            date_str=self.date_str,
            category="concept",
            subjects=[subj_id],
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback.",
        )
        return fm + f"## {area}\n\nfallback placeholder. Claude CLI 재실행 필요.\n"
