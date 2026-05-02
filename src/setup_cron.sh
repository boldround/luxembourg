#!/bin/bash
# 프로젝트 룩셈부르크 — cron 설정 안내 (실제 등록은 노아가 직접)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIPELINE_SCRIPT="$SCRIPT_DIR/run_pipeline.sh"

echo "=================================================="
echo " 프로젝트 룩셈부르크 — cron 설정 안내"
echo "=================================================="
echo ""
echo "1) env -i 환경에서 스크립트 PATH 검증 (claude CLI 인증은 별도):"
echo "   env -i HOME=\"\$HOME\" PATH=\"/usr/bin:/bin\" $PIPELINE_SCRIPT \$(date +%Y-%m-%d) briefing"
echo "   → 스크립트 자체는 동작해야 함. Claude CLI 인증 실패 시 fallback 콘텐츠 생성됨."
echo ""
echo "2) Claude CLI 인증 (cron 환경에서 OAuth keychain 접근):"
echo "   - 사용자 cron은 GUI 세션 안에서 실행 → keychain 접근 가능 (최초 prompt 시 'Always Allow' 클릭)"
echo "   - 또는 ANTHROPIC_API_KEY 환경변수를 ~/.zshrc 또는 launchd plist에 등록"
echo ""
echo "3) crontab -e 로 다음 라인 추가:"
echo ""
echo "   # 프로젝트 룩셈부르크 — 매일 06:30 요일 기반 자동"
echo "   30 6 * * * $PIPELINE_SCRIPT"
echo ""
echo "4) 첫 1주일은 매일 logs/{YYYY-MM-DD}-cron.log 확인하여 fallback 발생 시 원인 파악"
echo ""
echo "=================================================="
echo "현재 crontab:"
crontab -l 2>/dev/null | grep -A1 -B1 luxembourg || echo "(루즈 관련 항목 없음)"
echo "=================================================="
