#!/bin/bash
# 기출 풀이 일괄 생성 — exam_solver_gen으로 (year, subject) 페어 처리.
# 각 풀이 후 자동 git add/commit/push.

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BASE_DIR"

LOG_FILE="$BASE_DIR/logs/exam-batch-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$BASE_DIR/logs"
log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

DATE_TAG="$(date +%Y-%m-%d)"

log "===== 기출 풀이 일괄 생성 시작 ($# 페어) ====="
SUCCESS=0; FAIL=0

for spec in "$@"; do
    YEAR="${spec%%:*}"
    SUBJECT="${spec##*:}"
    log "--- $YEAR / $SUBJECT ---"

    if python3 -m src.generators.exam_solver_gen \
        --year "$YEAR" --subject "$SUBJECT" --date "$DATE_TAG" >> "$LOG_FILE" 2>&1; then

        OUT="site/_posts/${DATE_TAG}-exam-${YEAR}-${SUBJECT}.md"
        if [ -f "$OUT" ]; then
            git add "$OUT" >> "$LOG_FILE" 2>&1
            git commit -m "content: $YEAR 2차 $SUBJECT 기출 풀이 자동 생성" >> "$LOG_FILE" 2>&1 || true
            git push origin master >> "$LOG_FILE" 2>&1 || log "  push 실패"
            SUCCESS=$((SUCCESS+1))
            log "  OK"
        else
            FAIL=$((FAIL+1))
            log "  파일 미생성"
        fi
    else
        FAIL=$((FAIL+1))
        log "  FAIL"
    fi
    sleep 3
done

log "===== 완료 — 성공 $SUCCESS / 실패 $FAIL ====="
