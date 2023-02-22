import snscrape.modules.twitter as sntwitter
import pymongo
import datetime 

def scrape_tweets(keyword, start_date, end_date, max_tweets):
    """
    Scrape tweets using the snscrape library.

    Args:
        keyword: Keyword or hashtag to search for.
        start_date: Start date to search for tweets.
        end_date: End date to search for tweets.
        max_tweets: Maximum number of tweets to scrape.

    Returns:
        List of dictionaries representing the scraped tweets.
    """
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= max_tweets:
            break
        tweets.append({
            'date': tweet.date,
            'id': tweet.id,
            'url': tweet.url,
            'content': tweet.content,
            'user': tweet.user.username,
            'reply_count': tweet.replyCount,
            'retweet_count': tweet.retweetCount,
            'language': tweet.lang,
            'source': tweet.sourceLabel,
            'like_count': tweet.likeCount
        })
    return tweets

def store_tweets_in_mongodb(keyword,tweets):
    """
    Store scraped tweets in MongoDB.

    Args:
        keyword: Keyword or hashtag used to scrape the tweets.
        tweets: List of dictionaries representing the scraped tweets.
    """
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['twitter']
    collection = db['tweets']
    collection.insert_one({"Scraped Word" : keyword,
                           "Scraped Date" : str(datetime.date.today()),
                           "Scraped Data":tweets})
