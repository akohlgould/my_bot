import tweepy
import time


print('this is my twitter bot')

CONSUMER_KEY = 'mnjW8Cwxe6rHPrFYpMJS5HKRy'
CONSUMER_SECRET = 't6qNgO8rYdLxtXP5K91X1o4Hj72bE29nA7xeIIxlSxFBiTYy26'
ACCESS_KEY = '1231627142808637441-akPOx18eHNPkuNWARHXCukPJDwfq4U'
ACCESS_SECRET = 'zgSQefAxvhIvSb56TXukivDXDfkto70MijewwOHXlqdce'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
    # DEV NOTE: use 1060651988453654528 for testing.
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#nomalarkey' in mention.full_text.lower():
            print('found #nomalarkey!', flush=True)
            print('responding back...', flush=True)
            api.update_status('@' + mention.user.screen_name +
                    '#AlltheMalarkey back to you!', mention.id)

while True:
    reply_to_tweets()
    time.sleep(30)
