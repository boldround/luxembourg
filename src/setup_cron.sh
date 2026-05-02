#!/bin/bash
# 프로젝트 룩셈부르크 — cron 설정 안내 (실제 등록은 노아가 직접)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIPELINE_SCRIPT="$SCRIPT_DIR/run_pipeline.sh"

echo "=================================================="
echo " 프로젝트 룩셈부르크 — cron 설정 안내"
echo "=================================================="
echo ""
echo "1) env -i 환경에서 동작 검증 (필수):"
echo "   env -i HOME=\"\$HOME\" PATH=\"/usr/bin:/bin\" $PIPELINE_SCRIPT $(date +%Y-%m-%d) briefing"
echo ""
echo "2) 검증 후 crontab -e 로 다음 라인 추가:"
echo ""
echo "   # 프로젝트 룩셈부르크 — 매일 06:30 요일 기반 자동"
echo "   30 6 * * * $PIPELINE_SCRIPT"
echo ""
echo "=================================================="
echo "현재 crontab:"
crontab -l 2>/dev/null | grep -A1 -B1 luxembourg || echo "(루즈 관련 항목 없음)"
echo "=================================================="
