# main.py

import asyncio
import json
from services.db import init_db
from services.post_history_repository import PostHistoryRepository
from services.orchestrator import BotOrchestrator

# Imports dos adaptadores
from services.fetchers.reddit_fetcher import RedditFetcher
from services.formatters.reddit_formatter import RedditFormatter
from services.publishers.twitter_publisher import TwitterPublisher
from services.publishers.email_publisher import EmailPublisher

# Credenciais
reddit_credentials = json.load(open('credentials/reddit_credentials.json'))
twitter_credentials = json.load(open('credentials/twitter_credentials.json'))
telegram_credentials = json.load(open('credentials/telegram_credentials.json'))
email_credentials = json.load(open('credentials/email_credentials.json'))

