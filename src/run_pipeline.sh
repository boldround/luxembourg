#!/bin/bash
# 프로젝트 룩셈부르크 — 콘텐츠 파이프라인 실행 (cron 진입점)
#
# 사용법:
#   ./run_pipeline.sh                       # 오늘, 요일 기반 자동
#   ./run_pipeline.sh 2026-05-04            # 특정 날짜
#   ./run_pipeline.sh 2026-05-04 briefing   # 날짜 + 타입 직접 지정

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BASE_DIR"

DATE="${1:-$(date +%Y-%m-%d)}"
CONTENT_TYPE_OVERRIDE="${2:-}"
LOG_DIR="$BASE_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/${DATE}-cron.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }

log "=========================================="
log "룩셈부르크 파이프라인 시작 — ${DATE}"
log "=========================================="

# pyenv / homebrew python (cron 환경 대비 명시)
export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:$HOME/.pyenv/shims:$HOME/.pyenv/bin:/usr/bin:/bin:$PATH"
eval "$(pyenv init -)" 2>/dev/null || true

# nvm (claude CLI는 node 기반)
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" 2>/dev/null || true

# claude CLI 직접 경로 (nvm 의존 회피)
if [ -f "$HOME/.local/bin/claude" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

# pipeline 호출 — content_type 미지정 시 요일 자동
ARGS=("--date" "$DATE")
if [ -n "$CONTENT_TYPE_OVERRIDE" ]; then
    ARGS+=("--content-type" "$CONTENT_TYPE_OVERRIDE")
fi

log "Step: pipeline 실행 (${ARGS[*]})"
python3 -m src.pipeline "${ARGS[@]}" >> "$LOG_FILE" 2>&1 || {
    EC=$?
    log "WARNING: pipeline 종료 코드 ${EC}"
    exit $EC
}

log "=========================================="
log "룩셈부르크 파이프라인 완료"
log "=========================================="
