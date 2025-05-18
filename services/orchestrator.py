# services/orchestrator.py

import asyncio, time
from typing import List, Dict
from models.interfaces import ContentFetcher, ContentFormatter, ContentPublisher

class BotOrchestrator:
    def __init__(
            self,
            fetchers: List[ContentFetcher],
            formatters: Dict[str, ContentFormatter],
            publishers: List[ContentPublisher],
            interval: int = 600
    ):
        self.fetchers = fetchers
        self.formatters = formatters
        self.publishers = publishers
        self.interval = interval

    async def _run_once(self):
        for fetcher in self.fetchers:
            raws = await fetcher.fetch()
            for raw in raws:
                fmt = self.formatters[fetcher.source_name]
                post = fmt.format(raw)
                for pub in self.publishers:
                    if pub.target_name != post.source:
                        await pub.publish(post)
    
    async def run(self):
        while True:
            start = time.time()
            await self._run_once()
            elapsed = time.time() - start
            await asyncio.sleep(max(0, self.interval-elapsed))