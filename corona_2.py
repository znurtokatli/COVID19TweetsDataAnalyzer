#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "1357146000423596032-qS09h1eCqAj6YOwQ2urIg42hdFTdHk"
access_token_secret = "rl2Bz6BrVFBMhuQGQlcaND3zWyKBFQ8VKGejt1tKuissE"
consumer_key = "TowbEZZ6M8nByxO1c3HsGMcKc"
consumer_secret = "z7t0Z8AcgsODOKGYiiD8I5slVpKsNOMnP3YY5JxIw84dR5vWzq"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['covid19', 'covid', 'coronavirus', 'pandemic'])


    api = tweepy.API(auth)
    page = 1
    # api = tweepy.API(auth)
    places = api.geo_search(query="USA",granularity="country")
    place_id = places[0].id
    tweets = api.search(q="place:%s" % place_id)
    stop_loop = False
    while not stop_loop:
        tweets = api.user_timeline(username, page=page)
        if not tweets:
            break
            for tweet in tweets:
                if datetime.date(2021, 2, 1) < tweet.created_at:
                    stop_loop = True
                    break
        # Do the tweet process here
        page+=1
        time.sleep(500)
