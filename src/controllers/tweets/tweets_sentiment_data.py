"""Controller tweets sentiment data."""

from fastapi import HTTPException

from services.abstract.abstract_data_collector import DataCollector
from services.abstract.abstract_sentiment_analyzer import SentimentAnalyzer
from utils.tweet.tweet_utils import format_search_tweets_keywords

from controllers.abstract.abstract_data_processor import SentimentDataProcessor
from controllers.abstract.abstract_db_tweet import IDBTweetController


class ProcessTwitterSentimentData(SentimentDataProcessor):

    """Process Twitter data class."""

    def __init__(
        self,
        data_collector: DataCollector,
        sentiment_analyzer: SentimentAnalyzer,
        db_controller: IDBTweetController,
    ) -> None:
        """Init method.

        Parameters
        ----------
        `data_collector`
            Data collector instance class.
        `sentiment_analyzer`
            Sentiment analyzer instance class.
        `db_controller`
            DB controller instance class.

        Returns
        -------
        None
        """
        self.data_collector = data_collector
        self.sentiment_analyzer = sentiment_analyzer
        self.db_controller = db_controller
        self.tweets_data = []
        self.tweets_analyzed = []
        self.hashtag_query = {"title": ""}

    def get_data(self, *args, **kwargs) -> None:
        """Get data from Twitter.

        Returns
        -------
        `None`
        """
        print("Getting data")
        self.hashtag_query["title"] = kwargs["query"].query
        self.tweets_data = self.data_collector.get_data_by_single_query(
            query=self.hashtag_query["title"],
            **format_search_tweets_keywords(),
        )

    def analyze_sentiment_data(self) -> None:
        """Analyze tweets data.

        Returns
        -------
        `None`
        """
        print(
            f"Analyzing tweets data len tweets data. {len(self.tweets_data)}"
        )
        self.tweets_analyzed = [
            self.sentiment_analyzer.analyze_sentiment(text=tweet["tweet_text"])
            for tweet in self.tweets_data
        ]

    async def get_data_to_db(self) -> None:
        """Controller to insert the data into the DB.

        Returns
        -------
        `None`

        Raises
        ------
        HttpException
        """
        try:
            await self.db_controller.insert_sentiment_classificted_tweet(
                hashtag_data=self.hashtag_query,
                tweets_data=self.tweets_data,
                sentiments_data=self.tweets_analyzed,
            )
        except Exception as error:
            print("There was an exception while inserting in DB %s", error)
            raise HTTPException("There was an exception while inserting in DB")

    async def process_data(self, *args, **kwargs) -> bool:
        """Main function to process the data.

        Returns
        -------
        `bool`
            If data was processed correctly.
        """
        try:
            self.get_data(*args, **kwargs)
            self.analyze_sentiment_data()
            await self.get_data_to_db()
            return True
        except Exception:
            return False
