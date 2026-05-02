"""개정세법·예규·판례 일일 브리핑 생성기."""

import json
import logging
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.briefing")


class BriefingGenerator(BaseGenerator):
    CONTENT_TYPE = "briefing"
    PROMPT_NAME = "briefing_gen"

    def build_context(self) -> str:
        nts_path = self.data_dir / "raw" / f"{self.date_str}.json"
        revisions_path = self.data_dir / "reference" / "law-revisions.json"

        parts = [f"# 컨텍스트\n\n## 오늘 날짜\n{self.date_str} (적용 시점 기준)"]

        if nts_path.exists():
            data = json.loads(nts_path.read_text(encoding="utf-8"))
            parts.append(f"\n## 국세청 보도자료 / 예규 (수집)\n\n{json.dumps(data, ensure_ascii=False, indent=2)[:4000]}")
        else:
            parts.append("\n## 국세청 데이터\n수집 데이터 없음 — 일반 브리핑으로 작성")

        if revisions_path.exists():
            rev = json.loads(revisions_path.read_text(encoding="utf-8"))
            parts.append(f"\n## 최근 개정 이력 (참고)\n\n{json.dumps(rev, ensure_ascii=False, indent=2)[:2000]}")

        return "\n".join(parts)

    def fallback_content(self) -> str:
        fm = self.frontmatter(
            title=f"개정세법 브리핑 — {self.date_str}",
            date_str=self.date_str,
            category="briefing",
            applied_date="2026-01-01",
            excerpt="자동 생성 fallback — 실제 콘텐츠는 NTS 데이터 수집 후 재실행 필요.",
        )
        body = (
            "## 오늘의 주요 개정\n\n"
            "(데이터 수집 또는 Claude CLI 실패로 fallback 콘텐츠가 표시됩니다.)\n\n"
            "수동으로 다음을 확인:\n"
            "- 국세청 보도자료\n"
            "- 최근 7일 신규 예규/통칙\n"
            "- 시험 직결 판례 (대법원)\n"
        )
        return fm + body
