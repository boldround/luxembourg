#!/usr/bin/env python3
"""국세청 보도자료 / 예규 수집기.

국세청은 RSS를 제공하지 않으므로 보도자료 리스트 페이지(HTML)를 가볍게 스크래핑한다.
- 리스트 페이지: https://www.nts.go.kr/nts/na/ntt/selectNttList.do?mi=2201&bbsId=1028
- 상세 링크: https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?nttSn={id}&mi=2201

크롤링 안전 수칙 준수:
- 요청 간 최소 5초 대기
- 대량 수집 시 10초 + 1분 휴식
- 차단 신호(429, 403) 감지 시 즉시 중단
- 리스트 페이지 1장만 가져오고 상세 페이지는 호출하지 않음 (요청 횟수 최소화)
"""

import json
import logging
import re
import time
from datetime import datetime, timezone, timedelta
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

logger = logging.getLogger("luxembourg.nts")

KST = timezone(timedelta(hours=9))
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

REQUEST_DELAY = 5.0
LONG_BREAK_DELAY = 60.0
BATCH_SIZE = 10
REQUEST_TIMEOUT = 30
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# 수집 대상 — 국세청 RSS는 존재하지 않음 (2026-05 기준 확인).
# 대신 보도자료 리스트 페이지의 HTML 테이블을 파싱한다.
SOURCES = [
    {
        "name": "국세청 보도자료",
        "type": "html_list",
        "url": "https://www.nts.go.kr/nts/na/ntt/selectNttList.do?mi=2201&bbsId=1028",
        "detail_url_template": "https://www.nts.go.kr/nts/na/ntt/selectNttInfo.do?nttSn={id}&mi=2201",
        "category": "press",
    },
    # 향후 후보(현재 미적용):
    # - 국세법령정보시스템 신규 예규/통칙 (taxlaw.nts.go.kr) — JS 렌더 의존, 별도 조사 필요
    # - 기획재정부 보도자료 (moef.go.kr) — RSS 없음, 별도 스크래퍼 필요
]


class NTSCollector:
    """국세청 + 조세 판례 수집기."""

    def __init__(self, date_str: str = None):
        if date_str is None:
            date_str = datetime.now(KST).strftime("%Y-%m-%d")
        self.date_str = date_str
        self.output_path = RAW_DIR / f"{date_str}.json"

    def collect(self) -> Path:
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        items = []

        for i, source in enumerate(SOURCES):
            try:
                fetched = self._fetch_source(source)
                items.extend(fetched)
                logger.info("%s: %d건 수집", source["name"], len(fetched))
            except Exception as e:
                logger.warning("%s 실패 (계속): %s", source["name"], e)

            # 안전 대기
            time.sleep(REQUEST_DELAY)
            if (i + 1) % BATCH_SIZE == 0:
                logger.info("배치 휴식 %ds", LONG_BREAK_DELAY)
                time.sleep(LONG_BREAK_DELAY)

        result = {
            "collected_at": datetime.now(KST).isoformat(),
            "date": self.date_str,
            "source_count": len(SOURCES),
            "item_count": len(items),
            "items": items,
        }
        self.output_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info("저장: %s (%d건)", self.output_path, len(items))
        return self.output_path

    def _fetch_source(self, source: dict) -> list[dict]:
        url = source["url"]
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                if resp.status in (429, 403):
                    logger.error("차단 감지 (%d) — 즉시 중단", resp.status)
                    raise RuntimeError(f"blocked: {resp.status}")
                content = resp.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            if e.code in (429, 403):
                logger.error("HTTP %d 차단 — 즉시 중단", e.code)
                raise
            return []

        if source["type"] == "rss":
            return self._parse_rss(content, source)
        if source["type"] == "html_list":
            return self._parse_html_list(content, source)
        return []

    def _parse_rss(self, content: str, source: dict) -> list[dict]:
        from xml.etree import ElementTree as ET

        items = []
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            logger.warning("RSS 파싱 실패: %s", e)
            return []

        for item in root.iter("item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            desc = (item.findtext("description") or "").strip()
            pub = (item.findtext("pubDate") or "").strip()
            if not title:
                continue
            items.append({
                "source": source["name"],
                "category": source["category"],
                "title": title,
                "link": link,
                "description": desc[:500],
                "pub_date": pub,
            })
        return items

    def _parse_html_list(self, content: str, source: dict) -> list[dict]:
        """국세청 보도자료 리스트 테이블 파서.

        각 <tr>에는 다음과 같은 td가 있다:
        - data-table="number" → 게시 번호
        - data-table="subject" → <a data-id="{nttSn}" title="{title}">…</a>
        - data-table="write" (첫 번째) → 담당부서
        - data-table="date" → 작성일자 (YYYY.MM.DD.)
        """
        items = []
        rows = re.findall(r"<tr[^>]*>(.*?)</tr>", content, re.DOTALL)
        template = source.get("detail_url_template", "")

        for row in rows:
            # 헤더 행/빈 행 스킵
            if "data-table" not in row:
                continue

            id_match = re.search(
                r'<a[^>]*data-id="(\d+)"[^>]*title="([^"]+)"[^>]*class="nttInfoBtn"',
                row,
            )
            if not id_match:
                continue
            nttsn, title = id_match.group(1), unescape(id_match.group(2)).strip()

            # 첫 번째 data-table="write" 셀 안의 주석을 건너뛰고 부서명만 추출
            dept = ""
            write_cells = re.findall(
                r'<td[^>]*data-table="write"[^>]*>(.*?)</td>', row, re.DOTALL
            )
            if write_cells:
                # 주석/태그 제거 후 첫 줄
                stripped = re.sub(r"<!--.*?-->", "", write_cells[0], flags=re.DOTALL)
                stripped = re.sub(r"<[^>]+>", "", stripped)
                dept = unescape(stripped).strip()

            date_match = re.search(
                r'<td[^>]*data-table="date"[^>]*>\s*([^<]+?)\s*</td>', row
            )
            pub_date = date_match.group(1).strip() if date_match else ""

            link = template.format(id=nttsn) if template else ""

            items.append({
                "source": source["name"],
                "category": source["category"],
                "title": title,
                "link": link,
                "description": f"[{dept}] {title}" if dept else title,
                "pub_date": pub_date,
                "ntt_sn": nttsn,
                "department": dept,
            })

        return items


if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    collector = NTSCollector(date_str=args.date)
    collector.collect()
