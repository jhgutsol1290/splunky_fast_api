"""Tweet model."""
import sqlalchemy
from database.db import metadata

tweet = sqlalchemy.Table(
    "tweets",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("tweet_text", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("id_str", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column(
        "user_screen_name", sqlalchemy.String(255), nullable=False
    ),
    sqlalchemy.Column("created_at", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column(
        "hashtag_id",
        sqlalchemy.ForeignKey("hashtags.id"),
        nullable=True,
    ),
)
