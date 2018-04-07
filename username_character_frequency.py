from __future__ import division
from collections import Counter
import csv
import math
import re
import numpy as np
import matplotlib.pyplot as plt
import codecs

#===============================================================================
# Outputs CSV of total character frequencies from input file of user identifiers
# @LawrenceA_UK
#===============================================================================


# Set input and output file names

input_text_file = ""
output_csv_file = ''

# Initialise term counter
char_freq = Counter()

# Optional regular expression filter
regex=False
regex_pattern =""

# Process usernames from text file and build character-count dictionary
txt = open(input_text_file, "r")
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
    for character in userident:
        char_freq[character]+=1               
txt.close()


# Plot character frequencies
print "Creating plot..."
plot_fig = plt.figure()  
plt.title(input_text_file)
plt.ylabel('Char count')
width = .15
ind = np.arange(len(char_freq))
plt.bar(ind, char_freq.values(), width=width)
plt.xticks(ind + width / 2, char_freq.keys())
plt.show()

# Output character frequencies to CSV
print "Creating CSV..."
out_csv = codecs.open(output_csv_file, 'wb', 'utf-8')
out_csv.write("Character" + ',' "Frequency Count" + u"\n")
for thechar, thecount in char_freq.iteritems():            
    out_csv.write(thechar + ',' + str(thecount) + u"\n")
out_csv.close() 
print "[>] CSV file written as %s." % output_csv_file