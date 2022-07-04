"""Bind each and every router."""
from fastapi import APIRouter
from resources import tweet

api_router = APIRouter()

api_router.include_router(tweet.router)
