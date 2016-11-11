# -*- coding: UTF-8 -*-

#============================================================#
# Find variance in term frequency between two text corpora.  #
# by Lawrence Alexander LawrenceA_UK la2984@my.open.ac.uk    #
#                          July 2016                         #
#============================================================#

import re
import numpy as np
import matplotlib.pyplot as plt
import codecs
import md5
import math


def getWordCounts(input_corpus,stopwords_filename,minimum_count,same_case,doPlot,exportCSV):
    
    # Isolate each word and put it in a list
    input_corpus = input_corpus.decode('utf-8')    
    words_list = re.findall(r'[\w]+',input_corpus,re.U)
    
    # Optionally make all words lower case
    if same_case == True:
        for x, in_word in enumerate(words_list):        
            words_list[x] = in_word.lower()        
    word_counts = {}
    word_percentages = {}
    count = 0 
    
    # Load list of stop words 
    stop_words = []    
    with codecs.open(stopwords_filename, 'r','utf-8') as stopwords_file:        
        for stop_word in stopwords_file:            
            if "#" not in stop_word:                
                stop_words.append(stop_word)
                
    stopwords_file.close() 
    
    # Remove newline, whitespace or formatting characters from stop words file 
    for x, theword in enumerate(stop_words):    
        stop_words[x] = theword.strip()        
        
    for theword in stop_words:        
        if theword == '':
            stop_words.remove(theword)
    
    # Build a dictionary of word counts and percentages for the input corpus
    
    for the_word in words_list:    
        if the_word not in stop_words:            
            for countword in words_list:
                if countword == the_word:
                    count = count + 1 
                    
            if count >= minimum_count:                
                word_percentages[the_word] = 100.0 * count / len (words_list)
                word_counts[the_word] = count                           
            count =0 
    return word_counts, word_percentages


# Function taking in the two comparison texts as a list

def compare_texts(corpus_texts):
    freq_compare = {}
    for i in range(0,2): 
        word_counts,freq_compare[i]=word_percentages = getWordCounts(str(corpus_texts[i]),stop_words_file,minimum_count=1,same_case = True,doPlot= False,exportCSV=False)        
    diffs = []
    
    # Look for frequency differences in common words between texts
    for word_1, percentage_1 in freq_compare[0].iteritems():
        for word_2, percentage_2 in freq_compare[1].iteritems():
            if word_2 == word_1:            
                diffs.append(2**(percentage_1-percentage_2))    
    variance = 0
    # If there's any similarity between the texts, return the ratio - otherwise return none
    if diffs:
        for number in diffs:
            variance += number
        variance = variance / len (diffs)
        variance = math.sqrt(variance)
        return variance
    else:
        return None 
        
# Name of stop words file
stop_words_file = "stopwords_english.txt"
    
# Texts to compare
corpus_texts = ['','']
    
corpus_texts[0] = ""

corpus_texts[1] = ""

# Call the main comparison function 
ratio = compare_texts(corpus_texts)
if ratio is not None:    
    print "Frequency similarity ratio: %s" % ratio
else:
    print "No similarity found."