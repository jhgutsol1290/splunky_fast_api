"""Tweet API resources."""

from controllers.tweets.tweets_db import DBTweetController
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from controllers.tweets.tweets_sentiment_data import (
    ProcessTwitterSentimentData,
)
from schemas.base import ResponseBase
from schemas.requests import HashtagIn, SentimentClassificatorIn
from schemas.responses.tweet import (
    ResponseClassificatedTweetsHashtag,
    ResponseCountTweets,
    ResponseTweetNoHashtagOut,
    ResponseTweetsNoHashtagOut,
)
from services.sentiment_analyzer.vader_sentiment_analyzer import (
    VaderSentimentAnylyzer,
)
from services.twitter.twitter_data import TwitterDataCollector
from utils.tweet.tweet_http_utils import (
    verify_hashtag,
)

router = APIRouter(tags=["Tweets"])


@router.get(
    "/tweets/",
    response_model=ResponseTweetsNoHashtagOut,
    responses={200: {"model": ResponseTweetsNoHashtagOut}},
)
async def get_tweets_without_hashtag():
    """Retrieve tweets ONLY, without hashtag."""
    tweets = await DBTweetController.get_tweets_without_hashtag()
    return ResponseTweetsNoHashtagOut(
        detail="Data retrieved successfully", data=tweets
    )


@router.get(
    "/tweets/{tweet_id}/",
    response_model=ResponseTweetNoHashtagOut,
    responses={
        404: {"model": ResponseBase},
        200: {"model": ResponseTweetNoHashtagOut},
    },
)
async def get_tweet_without_hashtag_by_id(tweet_id: int):
    """Retrieve a single tweet ONLY, without hashtag by id."""
    if tweet := (
        await DBTweetController.get_tweet_without_hashtag_by_id(
            tweet_id=tweet_id
        )
    ):
        return ResponseTweetNoHashtagOut(
            detail="Data retrieved successfully", data=tweet
        )
    return JSONResponse(status_code=404, content={"detail": "Not found"})


@router.post(
    "/tweets/sentiment-classification/",
    status_code=201,
)
async def create_tweet_with_sentiment_classification(hashtag_query: HashtagIn):
    """Create tweet with sentiment classification."""
    if _ := (
        await ProcessTwitterSentimentData(
            data_collector=TwitterDataCollector(),
            sentiment_analyzer=VaderSentimentAnylyzer(),
            db_controller=DBTweetController(),
        ).process_data(query=hashtag_query)
    ):
        return ResponseBase(detail="Data processed successfully")
    return JSONResponse(
        status_code=500, content={"detail": "Error when processing data"}
    )


@router.get(
    "/tweets/sentiment-classification/{hashtag_query}",
    status_code=200,
    response_model=ResponseClassificatedTweetsHashtag,
    responses={200: {"model": ResponseClassificatedTweetsHashtag}},
    dependencies=[Depends(verify_hashtag)],
)
async def get_tweets_with_classification_by_hashtag(hashtag_query: str):
    """Retrieve tweets with sentiment classification using a given hashtag."""
    classificated_tweets = (
        await DBTweetController().get_classificated_tweets_by_hashtag(
            hashtag_query=hashtag_query
        )
    )
    return ResponseClassificatedTweetsHashtag(
        detail="Data retrieved successfully", data=classificated_tweets
    )


@router.get(
    "/tweets/sentiment-classification/count/{sentiment_classificator_query}/",
    status_code=200,
    responses={200: {"model": ResponseCountTweets}},
)
async def get_count_by_sentiment_classificator(
    sentiment_classificator_query: SentimentClassificatorIn,
):
    """Retrieve count of records of the given sentiment_classificator."""
    data = await DBTweetController.get_count_by_sentiment_classificator(
        sentiment_classificator_query=sentiment_classificator_query
    )
    return ResponseCountTweets(detail="Data retrieved successfully", data=data)


@router.get(
    "/tweets/sentiment-classification/count/",
    status_code=200,
    responses={200: {"model": ResponseCountTweets}},
)
async def get_total_count_sentiment_classification():
    """Retrieve count of records of the given sentiment_classificator."""
    data = await DBTweetController.get_total_count()
    return ResponseCountTweets(detail="Data retrieved successfully", data=data)
