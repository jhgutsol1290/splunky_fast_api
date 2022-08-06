"""Twitter exceptions."""


class TwitterInvalidCredentialsException(Exception):
    """Invalid creadential exception for Twtter."""


class HashtagRequiredException(Exception):
    """Hashtag is required exception."""


class MissingDataTweetException(Exception):
    """Attribute Error missing in tweet data."""


class MaxBotAccountsPerRequets(Exception):
    """Max bot twitter accounts per request exception."""