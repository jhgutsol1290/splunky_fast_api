"""Hashtag model."""
import sqlalchemy
from database.db import metadata


hashtag = sqlalchemy.Table(
    "hashtags",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column(
        "created_at",
        sqlalchemy.DateTime,
        server_default=sqlalchemy.func.now(),
    ),
)
