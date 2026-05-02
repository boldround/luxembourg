# 프로젝트 룩셈부르크

노아의 세무사 자격시험 학습 플랫폼. 도영이 [비엔나](../vienna)의 자매 프로젝트.

## 시험 일정

| 시험 | 일자 | 비고 |
|---|---|---|
| 2026 1차 | 4/25 (응시 완료) | 합격자 5/27 발표 |
| 2026 2차 | 7/18 | 1차 합격 시 도전 |
| 2027 1차 | 4/24 (예상) | 본격 합격 목표 |
| 2027 2차 | 7/17 (예상) | 최종 합격 |

## 과목

**1차 (객관식 4과목)**
- 재정학 / 세법학개론 / 회계학개론 / **행정소송법(선택)**

**2차 (논술+계산 4과목)**
- 회계학 1부 — 재무회계 + 원가관리회계
- 회계학 2부 — 세무회계
- 세법학 1부 — 국기 / 소득 / 법인 / 상증
- 세법학 2부 — 부가 / 개소 / 지방 / 조특

## 콘텐츠 스케줄 (요일 자동)

| 요일 | 콘텐츠 |
|---|---|
| 월 | 일일 브리핑 (개정세법·예규·판례) |
| 화 | 회계학 계산문제 1세트 |
| 수 | 세법학 핵심개념 정리 |
| 목 | 플래시카드 30장 |
| 금 | 세법학 논술 모범답안 1제 |
| 토 | 주간 회독 리포트 + 약점 진단 |
| 일 | 휴식 |

## 디렉토리

```
luxembourg/
├── src/                # Python 콘텐츠 파이프라인
│   ├── pipeline.py     # 요일 스케줄 오케스트레이터
│   ├── collectors/     # NTS, 판례, 개정 추적
│   ├── generators/     # briefing/calc/concept/flashcard/practice/weekly
│   ├── validators/     # 팩트체커 (조문/판례/applied_date)
│   ├── analyzers/      # 출제 트렌드
│   └── prompts/        # Claude 프롬프트
├── data/
│   ├── raw/            # 수집 원본
│   ├── reference/      # 세법 조문 / 판례 / 예규 / 개정 이력
│   ├── exams/          # 10년치 기출
│   └── analysis/       # 트렌드/예측
├── site/               # Jekyll
└── logs/
```

## 운영

```bash
# 로컬 빌드
cd site && bundle install && bundle exec jekyll serve

# 콘텐츠 파이프라인 (수동)
python3 -m src.pipeline --date 2026-05-02 --content-type briefing

# 자동 스케줄 (cron)
# crontab -e 후 등록 — env -i 사전 검증 필수
```

## 정확도 원칙

- 모든 콘텐츠에 `applied_date: YYYY-MM-DD` frontmatter 필수
- 조문 번호 / 판례명 / 통칙 인용은 팩트체커 통과 후 배포
- 시험일 시점 시행 법령만 적용 (개정 전 조문 인용 시 배포 차단)
- 불확실한 내용은 "[확인 필요]" 표시 — "모른다"가 틀리는 것보다 낫다

## 접속 (배포 후)

- URL: https://boldround.github.io/luxembourg/
- 접속 코드: 별도 메모 (default.html `CODE_HASH` 변경 시 업데이트)
