# -*- coding: UTF-8 -*-

#================================================================================================#
#     Log potential Twitter bots based on username entropy and use of non-dictionary words       #
#             Lawrence Alexander @LawrenceA_UK la2894@my.open.ac.uk                              #
#                                      October ‎2016                                              #
#================================================================================================#

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from bs4 import BeautifulSoup
import json
import math
import codecs

client_key = ''
client_secret =''
token = ''
token_secret =''


watchphrases = ['#example1','#example2']


# File to write out results
outputfile = ""
outfile = codecs.open(outputfile, 'a', 'utf-8')


#
# Check whether input string contains natural language phrases
#
def check_dictionary_words(username):
    # Ensure username is lower case
    username=username.lower()
    
    # Path to dictionary file - used file found here https://github.com/dwyl/english-words
    
    dict_file = ""
    # Scan through file, stripping any whitespace and making each word lower case
    try:
        with open(dict_file) as dictfile:        
            for dict_word in dictfile:
                dict_word=dict_word.lower()
                dict_word=dict_word.strip()
                dict_word=dict_word.replace(" ","")            
                if dict_word in username:                
                    contains_dict_word=True
                    break
                else:
                    contains_dict_word=False                
        dictfile.close()
    except:
        print "Failed to open dictionary file."
    return contains_dict_word
#
# Calculate Shannon entropy
#

def calc_entropy(in_sequence):
    count = 0
    item_probabilities = []
    entropy = []
    # Build alphabet (unique characters)
    alphabet = ""
    for char in in_sequence:    
        if char not in alphabet:
            alphabet=alphabet+char
           
    # Count frequencies of unique characters
    for the_item in alphabet:       
        for countletters in in_sequence:
            if countletters == the_item:
                count += 1 
        item_probabilities.append(float(count) / float(len (in_sequence))) 
        count =-0
        
    # Calculate entropy 
    for probability in item_probabilities:    
        entropy.append(math.log(probability,2)*probability)
    entropy = -sum(entropy)       
    return entropy

class StdOutListener(StreamListener):
    # Receive Twitter messages
    def on_data(self,data):
        # Parse tweet JSON into dictionary
        tweet = json.loads(data)        
        try:      
            username = tweet ['user'] ['screen_name']
            timestamp = tweet ['created_at']    
            client_parsed = BeautifulSoup(tweet['source'], 'html.parser')
            for client in client_parsed.findAll('a'):
                            client_url= client.attrs['href']                            
                            client_name= client.contents[0]            
            
            entropy=calc_entropy(in_sequence=username)
            
            # Detection threshold: between 3.9-3.7 seems suitably selective
            entropy_threshold = 3.7
            if entropy >= entropy_threshold:
                dict_check=check_dictionary_words(username=username)
                if dict_check == False:                    
                    print ">> Detection: %s | %s | %s | %s" % (username,client_name,client_url,str(timestamp))
                    outfile.write(timestamp + ',' + username + ',' + client_name + ',' + client_url + u"\n")
        except:
            pass        
        return True
    # Process any error messages
    def on_error(self,status):
        print "Warning- error: %s" % status

def stop():
    stream.disconnect()
    outfile.close()
    print "Streaming halted, file closed."
    

print "> Listening to Twitter stream. Type stop() to halt."   
l = StdOutListener()
auth = OAuthHandler(client_key, client_secret)
auth.set_access_token(token, token_secret)
stream= Stream(auth,l)
stream.filter(track=watchphrases,async=True)
