# Two robots with perfect knowledge of the Scrabble Dictionary and perfect searching
# ability play multiple Scrabble games.
# See the results analyzed in ScrabbleFrequency.py
# and ScrabbleWinners.py

import random
import sys
from scrabble import *
time.clock = time.time

# choose one of these two:
# randomseeds = range(0,1000) # example: range(0,1000), takes a few days
randomseeds = [5683,2982,4787] # 3 interesting games (with Linux random module) 

for rseed in randomseeds:
    print("rseed=",rseed)
    random.seed(rseed)
    t = tilebox()
    arack = rack()
    brack = rack()
    arack.fill(t)
    brack.fill(t)
    q = board()
    ascore=0
    bscore=0
    noplay=0 # will count succesive occurences of no tiles to play, games stops if 2
    
    searchtime =0
    scoretime = 0
    gamestart = time.clock()
    n = 0
    while len(arack)>0 and len(brack)>0 and n<100 and noplay<2:
    # player #1 and player A are synonomous, sorry for the confusion...
    # player #1 and player #2 alternate turns
        if n%2==0:
            player='#1' # player #1 always uses arack of tiles
            crack = arack # crack is the current rack being played 
        else:
            player='#2'
            crack = brack 

        xrack = ''.join(crack.tiles)
        
        print('  tiles in box:',t.count() )
        print(player,"with rack:",xrack," is searching...")
        aboard = q.ex()
        times=[time.clock()]
        ahope = getplays(aboard,xrack,verbose=False)
        sys.stdout.flush()
        times.append(time.clock())
        validplays = sortplays(ahope,aboard,verbose=False)
        vl = len(validplays)
        if vl:
            xbestplay = validplays[-1][1]
            xscore = validplays[-1][0]
            xscf = '{0:6.2f}'.format(xscore)
        else:
            xbestplay=None
        sys.stdout.flush() 
        times.append(time.clock())
        dtimes=[ '{0:6.2f}'.format(x-times[0])  for x in times[1:]]
        print( 'seconds:','  '.join(dtimes),"  for",vl," valid plays" )
        searchtime += times[1] - times[0]
        scoretime += times[2] - times[1]
        print(player,"with rack:",xrack,"will play")
        if not xbestplay:
            print('no play, pass')
            n += 1
            noplay += 1
            continue
        noplay = 0
        out = q.lay(xbestplay)
        crack.play( xbestplay[1] )
        
        print(xscf,xbestplay,"  for score:",out[0])
        print("words made:",out)
#        crack.fill(t)
        if n%2==0:
            ascore += out[0]
        else:
            bscore += out[0]
        print('#1:',ascore,'   #2:',bscore)
        q.show()
        crack.fill(t)
        n+=1
    gameend=time.clock()
    gametime='{0:7.2f}'.format(gameend-gamestart)
    print("game over in",gametime,"seconds")
    print("searchtime:",searchtime,"  scoretime:",scoretime)
    
    q.show()
    
    print("#1:",arack.tiles,"  #2:",brack.tiles)
    print("#1:",ascore,"  #2:",bscore)
    
    a_remain = evaltiles(arack.tiles)
    b_remain = evaltiles(brack.tiles)
    
    if a_remain == 0:
        ascore += b_remain
        bscore -= b_remain
    if b_remain == 0:
        ascore -= a_remain
        bscore += a_remain
    
    print("@DONE #1:",ascore," #2:",bscore," rseed=",rseed)
