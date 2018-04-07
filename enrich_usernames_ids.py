# -*- coding: UTF-8 -*-

#==========================================================#
# Takes in a list of Twitter identifiers from a text file  #
# and creates a CSV of key metadata fields for each account#
#        Lawrence Alexander @LawrenceA_UK                  #
#==========================================================#

import requests, json, time, codecs, sys
import csv
from requests_oauthlib import OAuth1
import requests_cache

# Set tokens and keys

client_key = ''
client_secret =''
token = ''
token_secret =''

# File names

input_text_file =""

output_csv_file=""


# Base URL for Twitter API calls

base_twitter_url = "https://api.twitter.com/1.1/"

# Auth setup

oauth = OAuth1(client_key,client_secret,token,token_secret)

# Initialise http cache to reduce load on Twitter API
requests_cache.install_cache(cache_name='twit_cache', backend='sqlite', expire_after=1800)

#
# Function to request profile information for username/user ID
#
def get_userdata(twitter_ident):     
    # Build appropriate URL for username or user ID
    api_url = "%s/users/show.json?" % base_twitter_url
    if twitter_ident.isdigit() == True:
        api_url += "user_id=%s&" % twitter_ident
    else:
        api_url += "screen_name=%s&" % twitter_ident
        
    # Send request
    response = requests.get(api_url,auth=oauth)
    time.sleep(1)
    if response.status_code == 200:
        user_data = json.loads(response.content)
        return user_data    
    else:
        print "Error accessing Twitter API: received a code %d." % response.status_code
        return None
    
# Load list of usernames or IDs for enrichment
txt= open(input_text_file, "r")
while 1:
    userident=txt.readline()
    if not userident:
        break         
    userident=userident.strip()
    if len(userident) >=2:
        print "Fetching user data for...%s" % userident
        user_data = get_userdata(userident)
        if user_data != None:
            # Parse required metadata fields into variables
            user_id = user_data['id_str']
            user_name = user_data['screen_name']
            try:
                user_url = user_data['entities']['url']['urls'][0]['expanded_url']                
            except:
                user_url=""                          
            
            creation_date = user_data['created_at']
            try:
                utc_offset = user_data['utc_offset']
            except:
                utc_offset="" 
            try:
                timezone = user_data['time_zone']
            except:
                timezone=""          
            try:
                interface_language = user_data['lang']
            except:
                interface_language=""      
            with open(output_csv_file, 'a') as fl:
                writer = csv.writer(fl,dialect='excel')
                writer.writerow([user_id,user_name,user_url,creation_date,utc_offset,timezone,interface_language])        
        else:
            print "[!] Couldn't retrieve data for tweeter: %s." % userident
fl.close()    
txt.close()
print "|>| Completed. "