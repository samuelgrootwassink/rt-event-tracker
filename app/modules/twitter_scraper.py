import tweepy
import itertools

class TwitterQuery():
    
    def __init__(self, query_entities):
        """
        Initialises a a TwitterQuery instance with the ability to store all related tweet objects

        Args:
            query (frozenset): Frozenset of query that is then converted into a usable format for the tweepy api
        """
        self._query =' '.join(entity for entity in query_entities )
        self._tweets = []
        

    @property
    def query(self):
        return self._query
    
    
    def add_tweet(self, tweet:dict):
        """
        Adds Tweet() instance to current instance

        Args:
            tweet (dict): The contents of the tweet scraped 
        """
        self._tweets.append(Tweet(**tweet))
    
    
    @property 
    def tweets(self):        
        return self._tweets

    
    def query_variations(self):
        
        query = itertools.combinations(self._query.split(), r)
        
    def __str__(self):
        return f'query:{self._query}, tweets:{len(self._tweets)}'


class Tweet():
    
    URL_PREFIX = 'https://twitter.com/twitter/statuses/'
    
    def __init__(self, id:int, content:str, query:TwitterQuery):
        self._id = id
        self._content = content
        self._query = query
        self._sentiment = None
        self._url = f'{Tweet.URL_PREFIX}{str(id)}'.strip()
        
        
    @property
    def sentiment(self):
        """
        Using NLTK's VADER determine the compound sentiment of a tweet. 
        A float value between 1 and -1 that is stored and returned

        Returns:
            float: The sentiment of this instances content, a value between 1 and -1 (positive - negative)
        """
        if self._sentiment is None:
            # Function not yet written, will cause an error
            self._sentiment = function.sentiment(self._content)
        return self._sentiment
    
    
    @property
    def content(self):
        return self._content
    
    
    @property
    def query(self):
        return self._query
        
    
    def __str__(self):
        return self._content
        
        
class TwitterScraper():
    
    def __init__(self):
        """
        Initialises instance and reads the secret bearer token from a text file stored in modules/files directory.
        """
        with open('modules/files/twitter_bearer_token.txt', 'r') as f:
          self._bearer_token= str(f.readline()).strip()
        self._client =  tweepy.Client(self._bearer_token)
       
        
    
    def search_tweets(self, queries:list):
        """
        Creates queries and searches for tweets using tweepy's API calls. Stores them in TwitterQuery() and Tweet() objects respectively. When all queries have been ran, returns a list with all the queries and subsequent tweets. 
    

        Args:
            queries (list): List of frozensets() containing named entities to look for on twitter

        Returns:
            list: List with TwitterQuery() objects
        """
        query_objects = []
        for query in queries:
            twitter_query = TwitterQuery(query)
            my_query = twitter_query.query
            response = self._client.search_recent_tweets(f"({my_query} ) -is:retweet lang:en" , max_results = 100)
            tweets = response.data
            
            for tweet in tweets:
                tweet_dict = {
                    'id' : tweet.id,
                    'content': tweet.text,
                    'query': self
                }
                twitter_query.add_tweet(tweet_dict)
            query_objects.append(twitter_query)
            
            # testing
            for tweet in [str(tweet) for tweet in twitter_query.tweets]:
                print(tweet)
        
        return query_objects
    


        
    