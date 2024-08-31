# Uses a concatentation of log files of 10,000 games played by identical robots in
# ScrabbleGames.py  
# The advantages of a player going first is examined.
# Using the usual, official doubling of the word score for the first
# word played, the final score of the first player is an average of 8.8 more points than 
# the second player. If the score for the first word is not doubled, the score
# difference is -5.04. Thus neither method is fair. The P-values are very small.
#
# Even though the robots P and Q  are identical, we can imagine that P and Q alternate in playing
# first. The results show that neither robot has a significant advantage over the other,
# as expected.
#
# scores10000.txt is obtained by: grep ^@DONE allgames.log
# scores10000a.txt requires reading in allgames.log and subtracting
# half the score from the first player from the final score for the first player.
# See ScrabbleGzip.py for details on the data processing.
#
# NOTE THE CHOICE OF A FILE IS MADE BELOW


import matplotlib.pyplot as plt
import sys
from scipy import stats
import math

# NOTE THE CHOICE OF THE WHICH FILE TO USE:
scorefile ='scores10000.txt'
#scorefile ='scores10000a.txt' # uncomment to use adjusted scoring file

lines = open(scorefile).readlines()

if scorefile.endswith('a.txt'):
    scoretype='with no doubling score on first word'
    adjusted=True
else:
    scoretype='with usual doubling score on first word'
    adjusted=False


dscore=[]
ascore=[]
pqscore=[]
n=0
for line in lines:
    if len(line)<20: continue
    v=line.split()
    s1=int(v[2]) # score of player #1 (who goes first)
    s2=int(v[4]) # score of player #2
    ascore.append(s1)
    ascore.append(s2) # append both scores
    diff = s1-s2 # to study score differential
    dscore.append(diff)
    if n%2!=0: diff = -diff # imagine robots P and Q swap who goes first, track P
    pqscore.append(diff) # to study advantage of P over Q (there isn't one)
    n+=1

avgscore = int(sum(ascore)/len(ascore))
maxscore = max(ascore)
minscore = min(ascore)
print("average Scrabble score of equal robots P and Q:", avgscore)
print("max score:", maxscore)
print("min score:", minscore)

# study if list of score differences produces wins and losses
# significantly different from a fair coin
def faircoin(scorelist):
    nw=0
    nt=0
    nl=0
    for y in scorelist:
        if y==0:
            nt+=1
        elif y>0:
            nw+=1
        else:
            nl+=1
    winper= round(100*nw/(nw+nl),2)
    print("lose:",nl,"   tie:",nt,"    win:",nw,"   win percent:",winper)
    n=nl+nw # ignore tie scores
    xbar=nw/n
    q=0.5 # fair coin probability
    z = (xbar - q) * math.sqrt(n / (q*(1-q)))
    pval = 2 * (1 - stats.norm.cdf( abs(z) ))
    info = "win: %d   lost: %d,   z-score: %6.2f,   pval: %10.3e,   win percent: %5.2f%%" % \
             (nw,nl,z,pval,winper)
    return info

ytop=300 # for set_ylim

############################### 1st png
avg1minus2 = sum(dscore)/len(dscore)
avg1minus2f = '%6.2f' % avg1minus2 
print()
print("average 1st player - 2nd player: ",avg1minus2f)
info0 = faircoin(dscore)

quick,simple=plt.subplots(figsize=(15,6))
simple.hist(dscore,bins=list(range(-400,400,5)));
ttest = stats.ttest_1samp(dscore, 0.)
ttstatf = '%6.2f' % ttest.statistic 
ttpvalf = '%10.3e' % ttest.pvalue 
info1="mean: "+avg1minus2f+" ,  "
info2="mean ttest statistic: " + ttstatf + "  pval: "+ttpvalf
longtitle = "score of 1st player minus 2nd player,  "+info1+info2
simple.set_title(longtitle)
simple.set_ylim((0,ytop))
simple.text(0,-.1,info0, transform=plt.gca().transAxes )
simple.text(0.1,.9,scoretype, horizontalalignment='left',transform=plt.gca().transAxes )

outpng = 'player1minus2.png'
if adjusted: outpng = 'player1minus2a.png'
quick.savefig(outpng, dpi=108)
print(outpng+' was saved')

############################### 2nd PNG
avgPminusQ = sum(pqscore)/len(pqscore)
avgPminusQf = '%6.2f' % avgPminusQ 
print()
print("average player P - player Q: " , avgPminusQf )
info0 = faircoin(pqscore)

quick,simple=plt.subplots(figsize=(15,6))
simple.hist(pqscore,bins=list(range(-400,400,5)));
ttest = stats.ttest_1samp(pqscore, 0.)
ttstatf = '%6.2f' % ttest.statistic 
ttpvalf = '%10.3e' % ttest.pvalue 
info1="mean: "+avgPminusQf+" ,  "
info2 = "mean ttest statistic: " + ttstatf + "  pval: "+ttpvalf
longtitle = "score of player P minus player Q,  " + info1 + info2
simple.set_title(longtitle)
simple.text( 0, -.1, info0, transform=plt.gca().transAxes )
simple.text(0.1,.9,scoretype, horizontalalignment='left',transform=plt.gca().transAxes )
simple.set_ylim((0,ytop))
outpng = 'playerPminusQ.png'
if adjusted: outpng = 'playerPminusQa.png'
quick.savefig(outpng, dpi=108)
print(outpng+' was saved')

