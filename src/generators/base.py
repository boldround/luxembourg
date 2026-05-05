"""콘텐츠 생성기 공통 베이스 — Claude CLI 호출 + 파일 저장."""

import json
import logging
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

logger = logging.getLogger("luxembourg.generator")
KST = timezone(timedelta(hours=9))


class BaseGenerator:
    """모든 콘텐츠 생성기의 부모.

    하위 클래스는 다음을 구현:
    - CONTENT_TYPE: str — 'briefing', 'calculation', 'concept', ...
    - PROMPT_NAME: str — prompts/{name}.md 파일명
    - build_context(self) -> str — 프롬프트에 주입할 컨텍스트 문자열
    - fallback_content(self) -> str — Claude CLI 실패 시 기본 마크다운
    """

    CONTENT_TYPE: str = ""
    PROMPT_NAME: str = ""

    def __init__(self, date_str: str = None):
        if date_str is None:
            date_str = datetime.now(KST).strftime("%Y-%m-%d")
        self.date_str = date_str
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.posts_dir = self.base_dir / "site" / "_posts"
        self.data_dir = self.base_dir / "data"
        self.prompt_path = self.base_dir / "src" / "prompts" / f"{self.PROMPT_NAME}.md"
        self.used_fallback = False

    def output_path(self) -> Path:
        return self.posts_dir / f"{self.date_str}-{self.CONTENT_TYPE}.md"

    def build_context(self) -> str:
        raise NotImplementedError

    def fallback_content(self) -> str:
        raise NotImplementedError

    def _read_prompt(self) -> str:
        if not self.prompt_path.exists():
            logger.warning("프롬프트 없음: %s", self.prompt_path)
            return ""
        return self.prompt_path.read_text(encoding="utf-8")

    def _claude_cli_available(self) -> bool:
        return shutil.which("claude") is not None

    SYSTEM_PROMPT_APPEND = (
        "당신은 단일 마크다운 파일의 텍스트만 stdout으로 출력합니다. "
        "도구를 호출하거나 파일을 작성/수정하지 않습니다. "
        "어떤 보고서, 요약, 메타 코멘트도 출력에 포함하지 않습니다. "
        "출력은 반드시 '---'로 시작하는 Jekyll frontmatter로 시작하고, "
        "frontmatter 다음에 본문 마크다운만 이어집니다. "
        "출력의 마지막에는 'BACKTICK x3' 코드블록이나 보고 문장을 절대 추가하지 않습니다.\n\n"
        "frontmatter 필수 필드: layout, title, date (YYYY-MM-DD HH:MM:SS +0900), "
        "categories ([type] 형태 배열), subject ([id] 형태 배열, 단수 문자열 금지), "
        "applied_date (\"YYYY-MM-DD\"). "
        "subject 값은 반드시 [accounting1, accounting2, tax_law1, tax_law2, admin_litigation] 중 하나 이상을 배열로."
    )

    def _generate_via_claude(self, full_prompt: str) -> str | None:
        """Claude CLI로 콘텐츠 생성. 실패 또는 형식 불일치 시 None."""
        if not self._claude_cli_available():
            logger.warning("claude CLI 없음 — fallback 사용")
            return None
        try:
            result = subprocess.run(
                [
                    "claude",
                    "--print",
                    "--disallowedTools",
                    "Read Write Edit MultiEdit Bash Glob Grep WebFetch WebSearch Agent NotebookEdit TodoWrite Task",
                    "--disable-slash-commands",
                    "--append-system-prompt",
                    self.SYSTEM_PROMPT_APPEND,
                    "--output-format",
                    "text",
                ],
                input=full_prompt,
                capture_output=True,
                text=True,
                timeout=600,
            )
            if result.returncode != 0:
                logger.error("Claude CLI 실패: %s", result.stderr[:500])
                return None
            output = result.stdout.strip()
            if not output.startswith("---"):
                logger.error("Claude 출력이 frontmatter로 시작하지 않음 (앞 200자: %r)", output[:200])
                return None
            return output + "\n"
        except subprocess.TimeoutExpired:
            logger.error("Claude CLI 타임아웃 (10분)")
            return None
        except Exception as e:
            logger.error("Claude CLI 호출 오류: %s", e)
            return None

    def generate(self) -> Path:
        self.posts_dir.mkdir(parents=True, exist_ok=True)
        out = self.output_path()

        prompt = self._read_prompt()
        ctx = self.build_context()
        full = prompt + "\n\n---\n\n" + ctx if prompt else ctx

        content = self._generate_via_claude(full)
        if content is None:
            logger.warning("fallback 콘텐츠 사용 — 배포 스킵 권장")
            content = self.fallback_content()
            self.used_fallback = True

        out.write_text(content, encoding="utf-8")
        logger.info("저장: %s (fallback=%s)", out, self.used_fallback)
        return out

    @staticmethod
    def frontmatter(
        title: str,
        date_str: str,
        category: str,
        subjects: list[str] = None,
        topics: list[str] = None,
        applied_date: str = None,
        difficulty: str = None,
        excerpt: str = None,
        layout: str = "post",
        extra: dict = None,
    ) -> str:
        lines = ["---", f'layout: {layout}', f'title: "{title}"',
                 f"date: {date_str} 09:00:00 +0900",
                 f"categories: [{category}]"]
        if subjects:
            lines.append(f"subject: [{', '.join(subjects)}]")
        if topics:
            lines.append(f"topics: {json.dumps(topics, ensure_ascii=False)}")
        if difficulty:
            lines.append(f"difficulty: {difficulty}")
        if applied_date:
            lines.append(f'applied_date: "{applied_date}"')
        if excerpt:
            esc = excerpt.replace('"', "'")
            lines.append(f'excerpt: "{esc}"')
        if extra:
            for k, v in extra.items():
                if isinstance(v, str):
                    lines.append(f'{k}: "{v}"')
                else:
                    lines.append(f"{k}: {json.dumps(v, ensure_ascii=False)}")
        lines.append("---")
        return "\n".join(lines) + "\n\n"
