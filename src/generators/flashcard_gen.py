"""암기 플래시카드(30장) 생성기."""

import json
import logging
import re
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.flashcard")

ROTATION = [
    ("tax_law1", "국세기본법 핵심 30장"),
    ("tax_law1", "소득세법 빈출 30장"),
    ("tax_law1", "법인세법 빈출 30장"),
    ("tax_law2", "부가가치세법 핵심 30장"),
    ("accounting1", "재무회계 핵심 30장"),
    ("accounting2", "세무회계 빈출 30장"),
]


class FlashcardGenerator(BaseGenerator):
    CONTENT_TYPE = "flashcard"
    PROMPT_NAME = "flashcard_gen"

    def _select_topic(self):
        from datetime import datetime
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, deck_title = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 덱\n- 과목: {subj_id}\n- 덱 제목: {deck_title}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 출력 형식\n"
            f"- frontmatter에 layout: flashcard, cards: [...] 30개\n"
            f"- 각 카드: q (질문), a (답), law (조문/판례), applied_date\n"
            f"- 답은 1-3문장 이내, 조문 번호 정확히\n"
        )

    def fallback_content(self) -> str:
        subj_id, deck_title = self._select_topic()
        fm = self.frontmatter(
            title=f"[fallback] {deck_title}",
            date_str=self.date_str,
            category="flashcard",
            subjects=[subj_id],
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback.",
            layout="flashcard",
            extra={"cards": [{"q": "placeholder", "a": "fallback 답", "law": "—", "applied_date": "2026-01-01"}]},
        )
        return fm + "fallback 카드 placeholder. Claude CLI 재실행 필요.\n"
