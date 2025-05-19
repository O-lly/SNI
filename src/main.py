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
reddit_credentials = json.load(open('../credentials/reddit_credentials.json'))
twitter_credentials = json.load(open('../credentials/twitter_credentials.json'))
telegram_credentials = json.load(open('../credentials/telegram_credentials.json'))
email_credentials = json.load(open('../credentials/email_credentials.json'))


def main():

    # 1) Inicializa DB e histórico
    init_db()
    repo = PostHistoryRepository()

    # 2) Carrega config
    config = json.load(open('../config/config.json'))

    # 3) Instancia fetchers
    fetchers = [
        RedditFetcher(
            credentials=reddit_credentials,
            repository=repo,
            subreddit='HonkaiStarRail',
            filter=config['reddit_filter'],
            limit=config['reddit_limit']
        ),
    ]

    # 4) Instancia formatters
    formatters = {
        'reddit': RedditFormatter(),
    }

    # 5) Instancia publishers
    publishers = []

    if config['twitter_send']:
        from tweepy import TwitterClient
        twitter_client = TwitterClient(twitter_credentials)
        publishers.append(TwitterPublisher(twitter_client, repo))
    if config['email_send']:
        import mail
        publishers.append(EmailPublisher(
            mailer=mail,
            repository=repo,
            receiver=email_credentials['receiver']
        ))

    # 6) Cria e roda orquestrador
    orchestrator = BotOrchestrator(
        fetchers=fetchers,
        formatters=formatters,
        publishers=publishers,
        interval=600
    )
    asyncio.run(orchestrator.run())

if __name__ == "__main__":
    main()