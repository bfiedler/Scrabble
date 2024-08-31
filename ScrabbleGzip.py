# penzero_all.log contains the concatenation of 10,000 log files produced
# by a program similar to ScrabbleGames.py
# But those log files also contain some additional text from an option to allow 
# the two robots to use different strategies. But the two robots used the same strategies for
# all experiments. So some additional text is stripped off in writing 
# xoutscore.txt and xoutscore_adjusted.txt, because the text is irrelevant.
# ScrabbleGames.py no longer has the option for the players
# to have different strategies.
import gzip
import io
import re
print("extracting three files from big gzip of log file... wait ~20 seconds")
biglogfile = 'penzero_all.log.gz'
gz = gzip.open(biglogfile, 'rb')
f = io.BufferedReader(gz)
outscore = open('xoutscore.txt','w')
outadjusted = open('xoutscore_adjusted.txt','w')
outwords = open('xwordsplayed.txt','w')
for line in f:
    dline = line.decode(encoding='UTF-8')

    if dline.startswith("@DONE"):
        outscore.write(dline[:35]+"\n") # strip irrelevant pena, penb etc.

    if dline.startswith("words "):
        outwords.write(dline)

    if dline.startswith('rseed'):
        count=0
        first = None
    count += 1
    if count==6:
        if dline.startswith("no play"):
            halfscore=0
        else
            v=dline.split()
            first = int(v[-1])
            if first%2!=0:
                sys.exit("was not even")
            else:
                halfscore=first//2
    if dline.startswith('@DONE'):
        v = re.split('(\s+)',dline)
        newfinalscore = int(v[4])-halfscore
        newfinalscoref = '%3d' % newfinalscore
        v[4] = newfinalscoref
        newline = ''.join(v)
        outadjusted.write(newline[:35]+"\n") # strip irrelevant pena, penb etc.
gz.close()
