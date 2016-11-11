# -*- coding: UTF-8 -*-


#=================================================================================#
#    Return term frequencies (excl. stop words) for a given corpus of text        #
#          Lawrence Alexander @LawrenceA_UK la2894@my.open.ac.uk                  #
#                             July 2016                                           #
#=================================================================================#


import re
import numpy as np
import matplotlib.pyplot as plt
import codecs
import md5


def getWordCounts(input_corpus,stopwords_filename,minimum_count,same_case,doPlot,exportCSV):
    # Isolate each term and put it in a list
    print "Analyzing term frequencies..."
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
    
    # Build a dictionary of term counts for the input corpus    
    for the_word in words_list:    
        if the_word not in stop_words:            
            for countword in words_list:
                if countword == the_word:
                    count += 1 
            if count >= minimum_count:                
                word_percentages[the_word] = 100.0 * count / len (words_list)
                word_counts[the_word] = count                           
            count =0
    
    # Optionally plot term frequencies
    if doPlot == True:
        print "Creating plot..."
        plot_fig = plt.figure()   
        width = .15
        ind = np.arange(len(word_counts))
        plt.bar(ind, word_counts.values(), width=width)
        plt.xticks(ind + width / 2, word_counts.keys())
        plt.show()
        
    # Optionally create CSV of term frequencies    
    if exportCSV == True:
        print "Creating CSV..."
        hashtext = md5.new()        
        hashtext.update(input_corpus.encode('utf-8')) 
        outputcsv = "word_frequency-%s.csv" % str(hashtext.hexdigest())
        out_csv = codecs.open(outputcsv, 'wb', 'utf-8')
        out_csv.write("Term" + ',' "Frequency" + u"\n")
        for theword, thecount in word_counts.iteritems():            
            out_csv.write(theword + ',' + str(thecount) + u"\n")
        out_csv.close() 
        
    print "Finished processing %s words" % len(words_list)    
    return word_counts, word_percentages

stop_words_file = "stopwords_english.txt"

input_corpus =""


word_counts,word_percentages = getWordCounts(input_corpus,stop_words_file,minimum_count=2,same_case = True,doPlot= True,exportCSV=False)


