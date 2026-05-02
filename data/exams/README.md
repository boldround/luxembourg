# 세무사 2차 기출문제 — 다운로드 및 파싱 가이드

프로젝트 룩셈부르크의 학습 데이터 소스. 한국산업인력공단 Q-Net에서 제공하는 세무사 2차 기출문제 HWP/HWPX 파일을 받아서 Markdown으로 파싱한다.

## 1. 다운로드 위치 (공식 출처)

**한국산업인력공단 Q-Net — 세무사 자격정보 > 자료실**

- 기출문제 내려받기: <https://www.q-net.or.kr/cst003.do?id=cst00309&gSite=L&gId=22>
- 최종정답: <https://www.q-net.or.kr/cst003.do?id=cst00310&gSite=L&gId=22>
- 시행공고(출제기준 포함): <https://www.q-net.or.kr/crf002.do?id=crf00201&gSite=L&gId=22>
- 시험통계: <https://www.q-net.or.kr/cst003.do?id=cst00308&gSite=L&gId=22>

대안 출처:
- 한국세무사회: <https://www.kacta.or.kr> (license.kacta.or.kr 자격시험 페이지)

> Q-Net 페이지는 회차/연도 선택 후 첨부파일(.hwp/.hwpx)을 직접 다운로드하는 방식이다. 자동 크롤링은 차단될 수 있으니 수동으로 받는 것을 권장.

## 2. 파일 저장 위치

받은 원본 파일은 다음 폴더에 둔다.

```
luxembourg/data/exams/raw/
```

연도별 하위 폴더로 정리하면 파서가 부모 디렉토리에서도 연도를 감지한다.

```
data/exams/raw/
  2024년/
    2024-2차-회계학1부.hwpx
    2024-2차-회계학2부.hwpx
    2024-2차-세법학1부.hwpx
    2024-2차-세법학2부.hwpx
  2023년/
    ...
```

## 3. 파일명 컨벤션 (권장)

파서가 과목과 연도를 자동 인식하려면 다음 키워드가 파일명 또는 부모 디렉토리에 있어야 한다.

- 과목 키워드: `회계학1부`, `회계학 1부`, `회계학2부`, `회계학 2부`, `세법학1부`, `세법학 1부`, `세법학2부`, `세법학 2부`
- 연도: 4자리(`2024`) 또는 부모 디렉토리의 `2024년` 형태

권장 포맷:

```
{연도}-2차-{과목}.{확장자}

예) 2024-2차-회계학1부.hwpx
    2024-2차-세법학2부.hwp
    2023-2차-회계학2부.hwpx
```

Q-Net에서 받은 원본 파일명을 그대로 두어도 대부분 인식되지만, 위 컨벤션으로 정리하면 디버깅이 쉽다.

## 4. 파싱 실행

원본 파일을 `raw/`에 넣은 뒤 프로젝트 루트(`luxembourg/`)에서:

```bash
# 전체 파싱
python3 -m src.collectors.hwpx_parser

# 2차시험만
python3 -m src.collectors.hwpx_parser --type 2차

# 단일 파일
python3 -m src.collectors.hwpx_parser --file data/exams/raw/2024년/2024-2차-회계학1부.hwpx
```

출력 결과:

```
data/exams/
  accounting1/{year}.md
  accounting1/_index.json
  accounting2/{year}.md
  accounting2/_index.json
  tax_law1/{year}.md
  tax_law1/_index.json
  tax_law2/{year}.md
  tax_law2/_index.json
```

## 5. 사전 요구사항

- Python 3.10+ (`tuple[str, str] | None` 타입 힌트 사용)
- HWP 파일(.hwp) 파싱 시: `hwp5html` CLI 필요 — `pip install pyhwp`
- HWPX 파일(.hwpx) 파싱 시: 표준 라이브러리만 사용 (zipfile + xml)
