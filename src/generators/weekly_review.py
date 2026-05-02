"""주간 회독 리포트 + 약점 진단 생성기."""

import json
import logging
from datetime import datetime, timedelta
from .base import BaseGenerator

logger = logging.getLogger("luxembourg.weekly")


class WeeklyReviewGenerator(BaseGenerator):
    CONTENT_TYPE = "weekly"
    PROMPT_NAME = "weekly_review"

    def _week_posts(self):
        """이번 주(월~금) 생성된 콘텐츠 파일 경로 모음."""
        d = datetime.strptime(self.date_str, "%Y-%m-%d")
        start = d - timedelta(days=d.weekday())  # 월요일
        result = []
        for i in range(6):
            day = (start + timedelta(days=i)).strftime("%Y-%m-%d")
            for p in self.posts_dir.glob(f"{day}-*.md"):
                result.append(p)
        return result

    def build_context(self) -> str:
        posts = self._week_posts()
        progress_path = self.data_dir / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8")) if progress_path.exists() else {}

        ctx = [f"# 이번 주 학습 데이터\n\n## 생성 콘텐츠 ({len(posts)}건)"]
        for p in posts:
            ctx.append(f"- {p.name}")
        ctx.append(f"\n## 회독·정답률\n\n{json.dumps(progress, ensure_ascii=False, indent=2)[:2000]}")
        ctx.append(
            "\n## 출력\n- 이번 주 학습 요약\n- 과목별 진척도\n- 약점 영역 진단 (정답률 낮은 주제 Top 3)\n- 다음 주 학습 제안\n"
        )
        return "\n".join(ctx)

    def fallback_content(self) -> str:
        fm = self.frontmatter(
            title=f"주간 회독 리포트 — {self.date_str}",
            date_str=self.date_str,
            category="weekly",
            excerpt="자동 생성 fallback.",
        )
        return fm + "## 이번 주 학습 요약\n\nfallback placeholder. progress.json 미존재 또는 Claude CLI 실패.\n"
