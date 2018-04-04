from __future__ import division

#==========================================================================================
# Generate CSV of text classification measures for input file of usernames.
# Calculates Shannon entropy, string length, vowel-consonant pattern as binary to decimal,
# and vowel-consonant ratio.
# By L Alexander @LawrenceA_UK
#==========================================================================================

import csv
import math
import re

# Set input and output file names

input_text_file = ""
output_csv_file = ''

# Optional Regex filtering
regex = False
regex_pattern = ""

def calc_entropy(in_string):
    count = 0
    letter_probabilities = []
    entropy = []  
    # Count letter frequencies
    for the_letter in in_string:       
        for countletters in in_string:
            if countletters == the_letter:
                count = count + 1 
        letter_probabilities.append(float(count) / len (in_string)) 
        count =0        
    # Calculate entropy 
    for probability in letter_probabilities:    
        entropy.append(probability * math.log(probability,2))
    entropy = -sum(entropy)
    return entropy

def vowel_consonant_binary(in_text):
    vowels = ['a','e','i','o','u']
    binary_word=""     
    # Iterate through input string building binary V/C word    
    for letter in in_text:
        letter=letter.lower()
        if letter.isalpha():
            if letter in vowels:
                binary_word+="1"
            else:
                binary_word+="0"
    if binary_word:            
        return str(int(binary_word,2))
    else:
        return None

def vowel_consonant_ratio(in_text):
    vowels = ['a','e','i','o','u']
    vowel_count = 0
    consonant_count = 0
    # Iterate through input string counting vowels and consonants
    for letter in in_text:
        letter=letter.lower()
        if letter.isalpha():
            if letter in vowels:
                vowel_count+=1
            else:
                consonant_count+=1
    try:            
        vcr = float(vowel_count / consonant_count)        
        return vcr    
    except ZeroDivisionError:
        return 0
    
# Return sum and count of digits in input string   
def digit_count_sum(in_text):    
    digit_count = 0
    digit_sum = 0    
    for letter in in_text:
        letter=letter.lower()
        if letter.isdigit():
            digit_count+=1
            digit_sum+=(int(letter))            
    return [str(digit_count),str(digit_sum)]

    
# Load from text file
with open(output_csv_file, 'a') as fl:
    print "[*] Processing file %s..." % input_text_file
    txt= open(input_text_file, "r")
    counter = 0
    while 1:
        userident=txt.readline()
        if not userident:
            break         
        userident=userident.strip()
        
        # Optional regular expression filtering
        regex_filter = re.match(regex_pattern,userident)        
        if regex==True and not regex_filter:
            continue
            
            
        if len(userident) >=2:         
                writer = csv.writer(fl,dialect='excel')
                
                if counter == 0:
                    writer.writerow(["Username", "Username Entropy", "Username Length", "VC-bin-dec","VCR",
                                     "Digit Count","Digit Sum"])
                entropy = calc_entropy(in_string = userident)
                username_length=str(len(userident))
                vowel_consonant_bitmask=vowel_consonant_binary(in_text=userident)
                vowel_con_ratio=vowel_consonant_ratio(in_text=userident)
                digit_count = digit_count_sum(in_text=userident)[0]
                digit_sum = digit_count_sum(in_text=userident)[1]
                writer.writerow([userident,entropy,username_length,vowel_consonant_bitmask,vowel_con_ratio,
                                 digit_count,digit_sum]) 
                counter+=1
       
fl.close()    
txt.close()
print "[>] Complete. File written as %s." % output_csv_file