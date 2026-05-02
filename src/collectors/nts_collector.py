#!/usr/bin/env python3
"""국세청 보도자료 / 예규 수집기.

크롤링 안전 수칙 준수:
- 요청 간 최소 5초 대기
- 대량 수집 시 10초 + 1분 휴식
- 차단 신호(429, 403) 감지 시 즉시 중단
"""

import json
import logging
import re
import time
from datetime import datetime, timezone, timedelta
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

# 수집 대상 — RSS 또는 정적 HTML
SOURCES = [
    {
        "name": "국세청 보도자료 RSS",
        "type": "rss",
        "url": "https://www.nts.go.kr/comm/rss/rss.xml?mi=12106",
        "category": "press",
    },
    # 추가 소스는 안전 확인 후 점진적 등록
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
                if resp.status == 429 or resp.status == 403:
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
