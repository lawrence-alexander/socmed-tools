# -*- coding: UTF-8 -*-
# Experimental bot detection script to log usernames of first retweeters for target account
# Lawrence Alexander, June 2016

from tweepy import StreamListener
from tweepy import Stream
import tweepy, codecs, sys, time, winsound

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

outputfile = ".csv"
outfile = codecs.open(outputfile, 'a', 'utf-8')

# ID of account to monitor

target =['12345']


print "Waiting for tweets from: " + target[0]

class StdOutListener(StreamListener):   
 
    def on_status(self, status):
        
        sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
        
        username = status.user.screen_name
        timestamp = status.created_at
        text = status.text
        tweet_ident = status.id
        user_id = status.user.id
        retweeted_status = status.retweeted
        
        if retweeted_status == False and 'RT @' not in text and str(user_id) == target[0]:
            print "Tweet posted by " + str(username) + " at " + str(timestamp)
            print "Waiting for retweets..."
            retweeters =[]
            retweeters_time = {}
            
            for x in range(0, 30):                
                retweets = api.retweets(id=tweet_ident)
                num_retweets = len(retweets)
                
                # Get accounts retweeting
                
                for y in range(0,num_retweets):
                            screen_name = (retweets.__getitem__(y).user.screen_name)
                            if x <= 6:
                                a = str(x) + "/" + str(y)
                                retweeters_time[a] = screen_name;
                            retweeters.append(screen_name)
                  
                print "Detected " + str(num_retweets) + " retweets at " + str(x) + " seconds"
                
                # Write time, retweets, username to CSV
                outfile.write(str(x) + ',' + str(num_retweets) + ',' + str(username) + u"\n")                
                time.sleep(1)   
                
            retweeters =set(retweeters)
            retweeters =list(retweeters)
            print retweeters_time
            winsound.Beep(2000,500)
            
            print "Complete. Retweets captured: " + str(len (retweets))
            stream.disconnect()
            outfile.close()                        

        return True
 
    def on_error(self, status_code):
        print('Warning: error code ' + str(status_code))
        return True 
 
    def on_timeout(self):
        print('Request timed out. Check connection.')
        return True 

def terminate():
    stream.disconnect()

if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
 
    stream = Stream(auth, listener)
    stream.filter(follow=target, async=True)