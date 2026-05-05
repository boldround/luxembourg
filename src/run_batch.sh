#!/bin/bash
# 다중 날짜 콘텐츠 일괄 생성 (백그라운드용).
# 사용법: ./run_batch.sh 2026-05-12:calculation 2026-05-13:concept ...

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BASE_DIR"

LOG_FILE="$BASE_DIR/logs/batch-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$BASE_DIR/logs"
log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "===== 일괄 생성 시작 ($# 건) ====="
SUCCESS=0
FAIL=0

for spec in "$@"; do
    DATE="${spec%%:*}"
    TYPE="${spec##*:}"
    log "--- $DATE / $TYPE ---"
    if python3 -m src.pipeline --date "$DATE" --content-type "$TYPE" >> "$LOG_FILE" 2>&1; then
        SUCCESS=$((SUCCESS+1))
        log "  OK"
    else
        FAIL=$((FAIL+1))
        log "  FAIL (exit $?)"
    fi
    sleep 2
done

log "===== 완료 — 성공 $SUCCESS / 실패 $FAIL ====="
