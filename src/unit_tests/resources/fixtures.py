import os, sys
from faker import Faker
fake = Faker()
Faker.seed(0)

# sys.path.append(os.getcwd()+"/src")
# print(os.getcwd()+"/src")
#/home/fabricio.chungo/github_globant/mentor_study/splunky_fast_api/src/unit_tests/resources


mock_hashtags_count = {
        "verso": 1,
        "sarasa": 4,
        "chamuyo": 1
    }


class MockTweet():

    obj_id = 0
    id_exists = False
    
    def __init__(self) -> None:
        MockTweet.obj_id += 1
        self.obj_id = MockTweet.obj_id
        self.tweet_text = fake.paragraph(nb_sentences=1)
        self.id_str = str(MockTweet.obj_id)
        self.user_screen_name = fake.simple_profile()['username']
        self.created_at = "01/01/2022"
        self.hashtag_id = 2
        self.retweets = 1

    def __repr__(self) -> str:
        return f"\nMock Tweet:\n - id: {self.obj_id}\n - text: {self.tweet_text}\n - user: {self.user_screen_name}\n - created at: {self.created_at}\n - hashtag id: {self.hashtag_id}\n - retweets: {self.retweets}"


mock_tweet_query = [MockTweet() for _ in range(4)]

if __name__ == "__main__":
    print(mock_tweet_query)