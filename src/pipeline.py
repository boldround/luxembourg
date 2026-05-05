#!/usr/bin/env python3
"""프로젝트 룩셈부르크 — 세무사 시험 학습 콘텐츠 파이프라인 오케스트레이터.

요일 스케줄에 따라 콘텐츠 타입을 자동 선택하고 생성기를 호출, git commit + push.
비엔나 패턴(요일 스케줄 + 멱등성 + Claude CLI + 자동 배포)을 그대로 차용.
"""

import argparse
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"
POSTS_DIR = BASE_DIR / "site" / "_posts"
KST = timezone(timedelta(hours=9))

# 요일별 콘텐츠 타입 (0=월 ... 6=일)
WEEKDAY_SCHEDULE = {
    0: "briefing",    # 월: 개정세법·예규·판례 브리핑
    1: "calculation", # 화: 회계학 계산문제
    2: "concept",     # 수: 세법학 핵심개념
    3: "flashcard",   # 목: 암기카드 30장
    4: "practice",    # 금: 세법학 논술 모범답안
    5: "weekly",      # 토: 주간 회독 + 약점 진단
    6: "quiz",        # 일: 1차 객관식 모의고사 (불합격 대비 트랙)
}

CONTENT_TYPE_KR = {
    "briefing": "개정 브리핑",
    "calculation": "계산 문제",
    "concept": "핵심개념",
    "flashcard": "암기카드",
    "practice": "논술 답안",
    "weekly": "주간 회독",
    "quiz": "1차 모의고사",
    "summary": "1차 단권화",
}


def _setup_logging(date_str: str) -> logging.Logger:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_DIR / f"{date_str}.log"

    logger = logging.getLogger("luxembourg")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
    )

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger


def _step(logger: logging.Logger, name: str, func, *args, **kwargs):
    logger.info("=" * 50)
    logger.info("[%s] 시작", name)
    start = time.time()
    try:
        result = func(*args, **kwargs)
        logger.info("[%s] 완료 (%.1fs)", name, time.time() - start)
        return result
    except Exception as e:
        logger.error("[%s] 실패 (%.1fs): %s", name, time.time() - start, e, exc_info=True)
        raise


def _select_content_type(date_str: str) -> str | None:
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return WEEKDAY_SCHEDULE.get(dt.weekday())


def _check_idempotent(date_str: str, content_type: str) -> Path | None:
    """이미 생성된 콘텐츠 파일이 있으면 경로 반환."""
    expected = POSTS_DIR / f"{date_str}-{content_type}.md"
    if expected.exists():
        return expected
    matches = list(POSTS_DIR.glob(f"{date_str}-{content_type}*.md"))
    return matches[0] if matches else None


def _git_commit_and_push(logger: logging.Logger, date_str: str, content_type: str, dry_run: bool):
    os.chdir(BASE_DIR)
    new_posts = list(POSTS_DIR.glob(f"{date_str}-{content_type}*.md"))
    raw_data = DATA_DIR / "raw" / f"{date_str}.json"
    files_to_add = list(new_posts)
    if raw_data.exists():
        files_to_add.append(raw_data)

    if not files_to_add:
        logger.info("커밋할 새 파일 없음")
        return

    if dry_run:
        logger.info("[DRY-RUN] 커밋 대상:")
        for p in files_to_add:
            logger.info("  - %s", p.relative_to(BASE_DIR))
        return

    try:
        for p in files_to_add:
            subprocess.run(["git", "add", str(p.relative_to(BASE_DIR))], cwd=BASE_DIR, check=True)

        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"], cwd=BASE_DIR
        )
        if result.returncode == 0:
            logger.info("이미 커밋됨")
            return

        type_kr = CONTENT_TYPE_KR.get(content_type, content_type)
        msg = f"content: {date_str} {type_kr} 자동 생성"
        subprocess.run(["git", "commit", "-m", msg], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "origin", "master"], cwd=BASE_DIR, check=True)
        logger.info("배포 완료: %s", msg)
    except subprocess.CalledProcessError as e:
        logger.error("git 작업 실패: %s", e)


def run_pipeline(
    date: str = None,
    content_type: str = None,
    skip_collect: bool = False,
    dry_run: bool = False,
):
    if date is None:
        date = datetime.now(KST).strftime("%Y-%m-%d")

    logger = _setup_logging(date)
    pipeline_start = time.time()

    logger.info("룩셈부르크 파이프라인 시작 -- %s", date)
    logger.info("옵션: type=%s skip_collect=%s dry_run=%s", content_type, skip_collect, dry_run)

    if content_type is None:
        content_type = _select_content_type(date)

    if content_type is None:
        logger.info("오늘 스케줄에 매핑된 콘텐츠 타입 없음 — 종료")
        return None

    type_kr = CONTENT_TYPE_KR.get(content_type, content_type)
    logger.info("콘텐츠 타입: %s (%s)", content_type, type_kr)

    # 멱등성
    existing = _check_idempotent(date, content_type)
    if existing and not dry_run:
        logger.info("이미 생성됨: %s", existing)
        return existing

    # Step 1: 데이터 수집 (briefing만)
    if not skip_collect and content_type == "briefing" and not dry_run:
        try:
            from .collectors.nts_collector import NTSCollector

            def do_collect():
                return NTSCollector(date_str=date).collect()

            _step(logger, "NTS 수집", do_collect)
        except Exception as e:
            logger.warning("NTS 수집 실패 (계속): %s", e)

    # Step 2: 생성기 호출
    output_path = None
    generator = None
    try:
        if dry_run:
            output_path = POSTS_DIR / f"{date}-{content_type}.md"
            logger.info("[DRY-RUN] 출력 경로: %s", output_path)
        elif content_type == "briefing":
            from .generators.briefing_gen import BriefingGenerator
            generator = BriefingGenerator(date)
            output_path = _step(logger, "브리핑 생성", generator.generate)
        elif content_type == "calculation":
            from .generators.calc_gen import CalcGenerator
            generator = CalcGenerator(date)
            output_path = _step(logger, "계산문제 생성", generator.generate)
        elif content_type == "concept":
            from .generators.concept_gen import ConceptGenerator
            generator = ConceptGenerator(date)
            output_path = _step(logger, "개념 정리 생성", generator.generate)
        elif content_type == "flashcard":
            from .generators.flashcard_gen import FlashcardGenerator
            generator = FlashcardGenerator(date)
            output_path = _step(logger, "플래시카드 생성", generator.generate)
        elif content_type == "practice":
            from .generators.practice_gen import PracticeGenerator
            generator = PracticeGenerator(date)
            output_path = _step(logger, "논술 답안 생성", generator.generate)
        elif content_type == "weekly":
            from .generators.weekly_review import WeeklyReviewGenerator
            generator = WeeklyReviewGenerator(date)
            output_path = _step(logger, "주간 리포트 생성", generator.generate)
        elif content_type == "quiz":
            from .generators.quiz_gen import QuizGenerator
            generator = QuizGenerator(date)
            output_path = _step(logger, "1차 모의고사 생성", generator.generate)
        elif content_type == "summary":
            from .generators.summary_gen import SummaryGenerator
            generator = SummaryGenerator(date)
            output_path = _step(logger, "1차 단권화 생성", generator.generate)
        else:
            logger.error("알 수 없는 타입: %s", content_type)
            sys.exit(1)
    except Exception as e:
        logger.error("생성기 실패: %s", e)
        sys.exit(1)

    # fallback 사용 시 배포 스킵
    if generator and generator.used_fallback and not dry_run:
        logger.warning("fallback 콘텐츠 — git push 스킵 (수동 검토 후 재실행 권장)")
        return output_path

    if output_path:
        logger.info("출력: %s", output_path)

    # Step 3: 팩트체커
    if output_path and not dry_run and output_path.exists():
        try:
            from .validators.fact_checker import check_file

            def do_check():
                return check_file(output_path)

            critical = _step(logger, "팩트체커", do_check)
            if critical:
                logger.error("CRITICAL 오류 발견 — 배포 차단")
                logger.error("오류: %s", critical)
                sys.exit(2)
        except ImportError:
            logger.warning("팩트체커 미구현 — 배포 진행")
        except Exception as e:
            logger.warning("팩트체커 오류 (배포 진행): %s", e)

    # Step 4: 배포
    _git_commit_and_push(logger, date, content_type, dry_run)

    logger.info("=" * 50)
    logger.info("총 %.1fs", time.time() - pipeline_start)
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="프로젝트 룩셈부르크 파이프라인")
    parser.add_argument("--date", type=str, default=None, help="YYYY-MM-DD")
    parser.add_argument(
        "--content-type",
        type=str,
        choices=sorted(set(list(WEEKDAY_SCHEDULE.values()) + ["summary"])),
        default=None,
    )
    parser.add_argument("--skip-collect", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    run_pipeline(
        date=args.date,
        content_type=args.content_type,
        skip_collect=args.skip_collect,
        dry_run=args.dry_run,
    )
