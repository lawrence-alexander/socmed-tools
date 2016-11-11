#=========================================================================================#
#                Filter out suspended/deleted Twitter accounts                            #
#           Lawrence Alexander @lawrenceA_UK la2894@my.open.ac.uk                         #
#                                July 2016                                                #
#=========================================================================================#


import requests, json, time, codecs, argparse
import csv
import datetime
import argparse
from requests_oauthlib import OAuth1

# Argument setup
argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-i","--inputfile",required=True,help="File containing usernames or user IDs")
arguments = vars(argument_parser.parse_args())

input_accounts_file = arguments['inputfile']

# Tokens and keys

client_key = ''
client_secret =''
token = ''
token_secret =''

# Base for Twitter calls

base_twitter_url = "https://api.twitter.com/1.1/"

# Auth setup

oauth = OAuth1(client_key,client_secret,token,token_secret)


#
# Function to return Twitter user ID from a user name, or vice versa
#

def twitter_user_lookup(screen_name_id):    
    # If identifier is a user ID, build suitable URL
    
    if screen_name_id[0].isdigit() == True:
        
        # If there's a list of identifiers passed, concatenate them and add to URL
        if type (screen_name_id) == list:                   
            user_string = str(screen_name_id)
            for rem_char in ["[","]","'", " "]:
                user_string=user_string.replace(rem_char,"")
            api_url = "%susers/lookup.json?user_id=" % (base_twitter_url)
            api_url += user_string 
            
        # Or if there's just one, add to the end of url        
        else:            
            api_url = "%susers/lookup.json?user_id=" % (base_twitter_url)
            api_url += screen_name_id
        
    # If the identifier is a username list           
    else:
        if type (screen_name_id) == list:                   
                    user_string = str(screen_name_id)
                    for rem_char in ["[","]","'", " "]:
                        user_string=user_string.replace(rem_char,"")
                        api_url = "%susers/lookup.json?screen_name=" % (base_twitter_url)
                        api_url += user_string 
                        
        # If the identifier is a single username                
        else: 
            api_url = "%susers/lookup.json?screen_name=" % (base_twitter_url)
            api_url += screen_name_id

    
    # Pause to handle Twitter rate limiting
    time.sleep(15)    
    
    # Make POST request inkeeping with Twitter's API preferences
    response = requests.post(api_url, auth=oauth)
    
    if response.status_code == 200:
            user_profiles = json.loads (response.content)
            usernames_ids = {}
            ids_usernames = {}
            
            if 'screen_name' in api_url:
                for user_profile in user_profiles: 
                    usernames_ids[user_profile ['screen_name']] = user_profile ['id']
                return usernames_ids
                    
            else:
                for user_profile in user_profiles:
                    ids_usernames[user_profile ['id']] = user_profile ['screen_name']
                return ids_usernames
    else:
        print "Error accessing Twitter API: returned a %s" % response.status_code
    return None   

#
# Function to output active account usernames/ids to file
#
def write_csv(user_identifier):    
    outputcsv = "%s_active-users.csv" % datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')
    out_csv = codecs.open(outputcsv, 'wb', 'utf-8')
    out_csv.write("Identifier1" + ',' "Identifier2" + u"\n")
    for id1, id2 in user_identifier.iteritems():            
        out_csv.write(str(id1) + ',' + str(id2) + u"\n")
    out_csv.close()     
   

# Load file of account identifiers to process

input_names = []
try:    
    with open(input_accounts_file, 'r') as input_usernames:
            for in_name in input_usernames:
                input_names.append(in_name)                
    input_usernames.close()
except:
    print "Error opening accounts file."

# Make lookup requests
lookup = []
clean_usernames = {}
num = 0
for ind,identifier in enumerate(input_names):
    print "Checking account %d of %d..." % (ind,len(input_names))
    identifier=identifier.rstrip()
    lookup.append(identifier)    
    if len(lookup) == num+95:        
        clean_usernames = twitter_user_lookup (lookup)        
        lookup = []     
num += 1

# Repeat process for any remaining accounts
if lookup:    
    print "Checking account %d of %d..." % (ind+1,len(input_names))
    clean_usernames.update(twitter_user_lookup (lookup))
write_csv(clean_usernames)    
print "Found %d active Twitter accounts out of %d." % (len(clean_usernames),len(input_names))