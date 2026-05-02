"""세법학 논술 모범답안 생성기."""

import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.practice")

ROTATION = [
    ("tax_law1", "국세기본법", "조세불복 절차의 효력과 한계"),
    ("tax_law1", "소득세법", "소득의 귀속과 실질과세원칙"),
    ("tax_law1", "법인세법", "부당행위계산부인의 요건과 효과"),
    ("tax_law1", "상속·증여세법", "포괄적 증여의제의 적용 한계"),
    ("tax_law2", "부가가치세법", "면세와 영세율의 비교와 실무 적용"),
    ("tax_law2", "조세특례제한법", "조세감면 사후관리 위반의 효과"),
]


class PracticeGenerator(BaseGenerator):
    CONTENT_TYPE = "practice"
    PROMPT_NAME = "practice_gen"

    def _select_topic(self):
        from datetime import datetime
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, area, theme = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 논제\n- 과목: {subj_id}\n- 영역: {area}\n- 주제: {theme}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 답안 작성 원칙\n"
            f"- 두괄식 + 논리 흐름 (서론 10-15% / 본론 70-80% / 결론 10-15%)\n"
            f"- 모든 주장에 조문/판례/통칙 인용\n"
            f"- 판례 핵심구절 1-2줄 정확 인용 (paragraph 번호까지)\n"
            f"- 학설 대립 제시 후 통설 입장 명시\n"
            f"- 개정 전후 비교 (해당 시)\n"
        )

    def fallback_content(self) -> str:
        subj_id, area, theme = self._select_topic()
        fm = self.frontmatter(
            title=f"[fallback] {theme} ({area})",
            date_str=self.date_str,
            category="practice",
            subjects=[subj_id],
            topics=[area],
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback.",
        )
        return fm + f"## {theme}\n\nfallback placeholder. Claude CLI 재실행 필요.\n"
