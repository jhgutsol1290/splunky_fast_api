from sqlalchemy import Table
import sqlalchemy
from database.db import metadata
from models.enums import SentimentClassificationEnum


sentiment_classificator = Table(
    "sentiment_classificators",
    metadata,
    sqlalchemy.Column(
        "id", sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    ),
    sqlalchemy.Column("sentiment_score", sqlalchemy.Float),
    sqlalchemy.Column(
        "sentiment_classification",
        sqlalchemy.Enum(SentimentClassificationEnum),
    ),
)
