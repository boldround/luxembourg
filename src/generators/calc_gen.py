"""회계학 계산문제 + 단계별 풀이 생성기."""

import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.calc")

ROTATION = [
    ("accounting1", "재무회계", "재무회계의 인식·측정·공시 (K-IFRS 기준)"),
    ("accounting1", "원가관리", "원가배부, CVP 분석, 차이분석"),
    ("accounting2", "법인세", "각사업연도소득금액 → 과세표준 → 산출세액"),
    ("accounting2", "소득세", "종합소득금액 → 과세표준 → 산출세액"),
]


class CalcGenerator(BaseGenerator):
    CONTENT_TYPE = "calculation"
    PROMPT_NAME = "calc_gen"

    def _select_topic(self):
        from datetime import datetime
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, topic, desc = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 출제 영역\n- 과목: {subj_id}\n- 주제: {topic}\n- 설명: {desc}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 출력 형식\n- frontmatter (layout: calculation, subject, topics, difficulty, applied_date)\n"
            f"- <div class='question-block'> 문제\n"
            f"- <div class='calc-step'> 단계별 풀이 (3-5단계)\n"
            f"- <div class='calc-answer'> 정답\n"
        )

    def fallback_content(self) -> str:
        subj_id, topic, _ = self._select_topic()
        fm = self.frontmatter(
            title=f"[fallback] 계산문제 — {topic} ({self.date_str})",
            date_str=self.date_str,
            category="calculation",
            subjects=[subj_id],
            topics=[topic],
            difficulty="기본",
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback. 실제 풀이는 Claude CLI로 재실행 필요.",
            layout="calculation",
        )
        body = (
            "<div class='question-block'>fallback 문제 placeholder</div>\n\n"
            "<div class='calc-step'><div class='calc-step-header'>"
            "<span style='display:flex;align-items:center;flex:1;'>"
            "<span class='calc-step-num'>1</span>"
            "<span class='calc-step-title'>1단계 — placeholder</span></span>"
            "<span class='calc-step-toggle'>▼</span></div>"
            "<div class='calc-step-body'>풀이 단계 placeholder</div></div>\n"
        )
        return fm + body
