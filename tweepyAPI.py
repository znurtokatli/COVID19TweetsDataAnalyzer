import tweepy
import pandas as pd

# creating authentication 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# connecting to the Twitter API using the above authentication
api = tweepy.API(auth)

cities_data = {
'Charlotte': {'region': 'Midwest', 'state': 'North Carolina'},
'Raleigh': {'region': 'East', 'state': 'North Carolina'},
}

# we want to see pandemic related tweets
q = 'covid19 OR covid or pandemic'

# define a function to convert a list of tweets into a pandas dataframe
def toDataFrame(tweets):
    df = pd.DataFrame()
    df['tweetID'] = [tweet.id for tweet in tweets]
    df['tweetText'] = [tweet.text for tweet in tweets]
    df['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]
    df['tweetFavoriteCt'] = [tweet.favorite_count for tweet in tweets]
    df['tweetSource'] = [tweet.source for tweet in tweets]
    df['tweetCreated'] = [tweet.created_at for tweet in tweets]
    df['userID'] = [tweet.user.id for tweet in tweets]
    df['userScreen'] = [tweet.user.screen_name for tweet in tweets]
    df['userName'] = [tweet.user.name for tweet in tweets]
    df['userCreateDt'] = [tweet.user.created_at for tweet in tweets]
    df['userDesc'] = [tweet.user.description for tweet in tweets]
    df['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    df['userFollowingCt'] = [tweet.user.friends_count for tweet in tweets]
    df['userLocation'] = [tweet.user.location for tweet in tweets]
    df['userTimezone'] = [tweet.user.time_zone for tweet in tweets]
    df['coordinates'] = [tweet.coordinates for tweet in tweets]
    df['geolocation'] = [tweet.geo for tweet in tweets]
    df['place'] = [tweet.place for tweet in tweets]
    return df

tweets_df = pd.DataFrame() # initialize an empty global dataframe

# loop through the dictionary of cities_data and retrieve the tweets in 
# each city
for city, city_data in cities_data.iteritems():

    # get the city's place_id
    city_id = api.geo_search(
        query='{}'.format(city), 
        wait_on_rate_limit=True, 
        granularity='city'
    )[0].id
    cities_data[city]['id'] = city_id

    city_tweets = [] # create an empty list to contain all the tweets

    # get the tweets in each city
    for tweet in tweepy.Cursor(api.search, q=q + '-filter:retweets', contained_within=city_id, granularity='city', wait_on_rate_limit=True, lang="en").items(10):    
        city_tweets.append(tweet)

    # convert list of tweets into a pandas dataframe of tweets
    city_tweets_df = toDataFrame(city_tweets)

    # append each row with city name, state name, and region.
    city_tweets_df['city'] = city
    city_tweets_df['state'] = city_data['state']
    city_tweets_df['region'] = city_data['region']

    # add city dataframe to global dataframe
    tweets_df = tweets_df.append(city_tweets_df, ignore_index=True)
