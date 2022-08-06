"""DB connection."""
import databases
import sqlalchemy
from decouple import config


DATABASE_URL = (
    f"postgresql://{config('DB_USER')}:"
    f"{config('DB_PASSWORD')}@{config('DB_HOST')}:"
    f"{config('DB_PORT')}/{config('DB_NAME')}"
)
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()
