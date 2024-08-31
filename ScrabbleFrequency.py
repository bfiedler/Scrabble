# Uses a concatentation of log files of 10,000 games played by identical robots in
# https://repl.it/@metrpy/ScrabbleGames 
# The  frequency of the words played in the Scrabble games is here examined.
#
# A file like wordsplay10000.txt can be obtained by: grep ^words allgames.log,
# where allgames.log is a concatenation of some log files produces by https://repl.it/@metrpy/ScrabbleGames 
# See also https://repl.it/@metrpy/ScrabbleGzip 
# The output file can also be seen at http://12characters.net/word_frequency.txt
#
# YOU MAY NEED TO WAIT 140 SECONDS BEFORE ANYTHING HAPPENS

import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

print("Patience.  Will read big file.")

lines = open('wordsplayed10000.txt').readlines()

wp = {} # keys will be words, the will be the number of times played

print()
print("analyzing words played, wait ~10 seconds...")

for line in lines:
    v=line.split(':')
    t=eval(v[1])
    l=t[1]
    for i in l:
        word = i[0].upper()
        if word in wp:
            wp[word] += 1
        else:
            wp[word] = 1

wpn=len(wp) #number of distinct words player

wpl = list(wp.items()) # convert dictionary to list of tuples

wpl.sort(key=lambda boomer: boomer[1]) # sort by value

wpl.reverse()

ndwords = 178690 # number of valid Scrabble words in scrabble2.txt
outfilename='word_frequency.txt'
wfile = open(outfilename,'wt')
#ouf=sys.stdout # or dump to monitor, when debugging short files  
ouf = wfile
tot=0 # counter to confirm wpn, the number of distinct words 
cut=9 # words played more than cut times will be printed
print("Valid words in Scrabble dictionary:",ndwords,file=ouf)
print(wpn,"different words were used in 10,000 computerized games",file=ouf)
print("Here is the frequency of some words:",file=ouf)
for m in range(2,16):
    if m>8: cut=1
    if m>9: cut=0
    print("\nwords of length",m,"used more than",cut, "times in 10,000 games:",file=ouf)
    count=0
    pcount=0
    for w,n in wpl:
        if len(w)==m:
            if n>cut:
                pcount+=1
                print(w,n,file=ouf)
            count+=1
            tot+=1
    ncount=count-pcount # number of words not printed
    print("...and", ncount,"more words used less than",cut+1,"times",file=ouf)
wfile.close()
print("confirm the same number:",tot,wpn,tot==wpn)
print(outfilename,"was written")

