"""1차 객관식 모의고사(5지선다 10문제) 생성기.

노아의 출퇴근 5-10분 학습 단위로 1차 4과목을 순환 출제.
- 재정학(public_finance)
- 세법학개론(tax_intro)
- 회계학개론(accounting_intro)
- 행정소송법(admin_litigation, 노아의 1차 선택과목)
"""

import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.quiz")

# (subject_id, 한글 라벨, 영역 힌트)
ROTATION = [
    ("public_finance", "재정학", "공공재 / 외부효과 / 조세귀착 / 사회후생"),
    ("tax_intro", "세법학개론", "국세기본법 / 소득세법 / 법인세법 / 부가가치세법 핵심"),
    ("accounting_intro", "회계학개론", "재무제표 / 자산·부채 인식·측정 / 수익 / 원가"),
    ("admin_litigation", "행정소송법", "취소소송·무효등확인소송 / 원고적격 / 처분성 / 소송요건"),
]


class QuizGenerator(BaseGenerator):
    CONTENT_TYPE = "quiz"
    PROMPT_NAME = "quiz_gen"

    def _select_topic(self):
        from datetime import datetime
        # 일요일 기준 매주 1과목씩 순환
        idx = datetime.strptime(self.date_str, "%Y-%m-%d").isocalendar()[1] % len(ROTATION)
        return ROTATION[idx]

    def build_context(self) -> str:
        subj_id, label, hints = self._select_topic()
        return (
            f"# 컨텍스트\n\n"
            f"## 오늘 1차 모의고사\n"
            f"- 과목 ID: {subj_id}\n"
            f"- 과목명: {label}\n"
            f"- 영역 힌트: {hints}\n"
            f"## 적용 법령 시점\n{self.date_str}\n"
            f"## 출제 원칙\n"
            f"- 5지선다 10문제 (정답 1개)\n"
            f"- 각 문항은 객관식 1차 시험 난이도 (단순 암기 + 함정 회피 50:50)\n"
            f"- 정답 + 핵심 해설 1-3문장\n"
            f"- 함정 보기는 '왜 틀렸는지' 짧게 추가\n"
            f"## 출력 형식\n"
            f"- frontmatter (layout: quiz, categories: [quiz], subject: [{subj_id}])\n"
            f"- 본문은 quiz 레이아웃이 렌더링하는 questions 리스트 (frontmatter 내)\n"
        )

    def fallback_content(self) -> str:
        subj_id, label, _ = self._select_topic()
        sample_q = [
            {
                "q": "fallback 샘플 문제 — Claude CLI 재실행 필요.",
                "choices": [
                    "보기 1",
                    "보기 2",
                    "보기 3",
                    "보기 4",
                    "보기 5",
                ],
                "answer": 1,
                "explanation": "fallback placeholder. 실제 해설은 quiz_gen 재실행으로 채워집니다.",
            }
        ]
        fm = self.frontmatter(
            title=f"[fallback] {label} 1차 모의고사 — {self.date_str}",
            date_str=self.date_str,
            category="quiz",
            subjects=[subj_id],
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback.",
            layout="quiz",
            extra={"questions": sample_q},
        )
        return fm + f"{label} 모의고사 fallback. Claude CLI 재실행 필요.\n"
