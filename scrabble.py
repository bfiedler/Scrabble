# I am not sure the following is needed:
# MIT License
# 
# Copyright (c) 2017 Brian Fiedler
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import itertools
import random
import string
import copy
import time


words = [x.rstrip() for x in open('scrabble2.txt')]
wordset=set(words) # a set is faster to search than is a list


letter_values = {"A": 1,
                 "B": 3,
                 "C": 3,
                 "D": 2,
                 "E": 1,
                 "F": 4,
                 "G": 2,
                 "H": 4,
                 "I": 1,
                 "J": 8,
                 "K": 5,
                 "L": 1,
                 "M": 3,
                 "N": 1,
                 "O": 1,
                 "P": 3,
                 "Q": 10,
                 "R": 1,
                 "S": 1,
                 "T": 1,
                 "U": 1,
                 "V": 4,
                 "W": 4,
                 "X": 8,
                 "Y": 4,
                 "Z": 10,
                 "*": 0}



bonusstr="""T--d---T---d--T
            -D---t---t---D-
            --D---d-d---D--
            d--D---d---D--d
            ----D-----D----
            -t---t---t---t-
            --d---d-d---d--
            T--d---D---d--T
            --d---d-d---d--
            -t---t---t---t-
            ----D-----D----
            d--D---d---D--d
            --D---d-d---D--
            -D---t---t---D-
            T--d---T---d--T""".replace(' ','')
bonusbrd = [list(x.strip()) for x in bonusstr.split('\n')]



# prepare a board, with all adjacent squares labeled with @
def alphabrd(brd):
    b=copy.deepcopy(brd)
    for i in range(15):
        for j in range(15):
            if b[i][j] not in '-@': continue
            if i==0:
                if b[1][j] not in '-@' : b[i][j]='@'
            elif i==14:
                if b[13][j] not in '-@' : b[i][j]='@'
            else:
                if (b[i-1][j] not in '-@') or (b[i+1][j] not in '-@'):
                    b[i][j] = '@'
    for j in range(15):
        for i in range(15):
            if b[i][j] not in '-@': continue
            if j==0:
                if b[i][1] not in '-@': b[i][j]='@'
            elif j==14:
                if b[i][13] not in '-@' : b[i][j]='@'
            else:
                if (b[i][j-1] not in '-@') or (b[i][j+1] not in '-@'):
                    b[i][j] = '@'
    if b[7][7] == '-':  # initial board has no letter here, and is valid for first word
        b[7][7] = '@'
    return b        


# for discovering valid plays for a rack of tiles
def getplays(brd,rck,verbose=True):
    playdict={}
    
    qd={}
    
    for k in range(1,8):
        qtuple= list(set(itertools.permutations(rck,k)))
        qd[k] = [''.join(a) for a in qtuple]
          
    brda = alphabrd(brd)
    
    # columns are transposed, making 30 "rows" to attempt fit
    allf = [''.join(x) for x in brda + list(zip(*brda))]

    i=-1
    for fit in allf:
        i+=1
        if verbose: print(fit)
        fminus = fit.count('-')
        fadja  = fit.count('@')
        if fminus == 15: continue
        totopen = fminus + fadja
        for k in range(1,min(8,totopen+1)):
            for a in qd[k]: # for all permutations of your rack
                if totopen==15 and a not in wordset: continue
                playsforfit = rowplays(a,fit,totopen,i) # plays that make a word
                playdict.update(playsforfit)
    return playdict


# tiles is an ordered sequence of up to seven tiles
# fit is a string of length 15 indicating what is in a row or column
# totopen is total number of open spaces in the row
# k is the "row" number of where fit came from
# 0 <= k <= 14 is a row, 15 <=k <= 29 is a column
# Finds all valid ways to place all tiles in a row,
# satisfying adjacent criteria and dictionary word criteria. 

def rowplays(tiles,fit,totopen,k):
    lent = len(tiles)
    stillopen = totopen
    poss={}

    for j in range(15): # j is a attempted starting position of first tile
        if fit[j] not in '-@': continue # no space space for first tile

        tryit = trylay(tiles,fit,j)
        if tryit:

            p = j
            while p-1>=0 and tryit[p-1] not in '-@':
                p -= 1

            q = j+lent-1 # because all tiles plays, q>=j+lent-1
            while q+1<15 and tryit[q+1] not in '-@':
                q += 1

            #if p==q: continue # one-letter word
            news = ''.join(tryit[p:q+1])

            if '*' not in news: 
                if news.upper() in wordset:             
                    key = ( (k,j),tiles ) # ((row or column, place), tiles placed)
                    poss[key] = (''.join(tryit), news) # item will be the word made
            else:
                for v in 'abcdefghijklmnopqrstuvwxyz':
                    newsx = news.replace('*',v,1) # replace only 1 *, so if 2, fail                          
                    if newsx.upper() in wordset:
                        tilesx = tiles.replace('*',v,1)
                        key = ( (k,j),tilesx ) # ((row or column, place), tiles placed)
                        poss[key] = (''.join(tryit), newsx) # item will be the word made
        stillopen -= 1
        if stillopen<lent: return poss # tiles too long to fit in remaining opens
    return poss  


# Attempt to lay tiles at a starting index j in a "row"
# of the board given in fit

def trylay(tiles,fit,j):
    f=list(fit)
    t=tiles
    p=j
    tch=False # True when placed on square that is adjacent

    for n in range(len(t)):
        while p<15 and (f[p] not in '-@'): #skip square if tile is there
            p+=1
        if p > 14:
            return [] #not all tiles could be played
        if fit[p]=='@': tch=True # will place on square labeled @
        f[p] = t[n]
    if not tch:
        return []
    else:
        return f # return fit with newly placed letters


# Will lay a valid fitting play, discovered by getplays,
# onto a board for scoring and checking for more words.
# If it does not fit, an error occurs, so ply must be known
# to fit
def layplay(brd,ply):
    a,b = ply[0]
    lets = ply[1]
    brdc = copy.deepcopy(brd)
    if a>14: # play down
        i,j = b,a-15
        p = i
        for n in range(len(lets)):
            while brdc[p][j] != '-': 
                p += 1
            brdc[p][j]=lets[n]
    else: # play right
        i,j = a,b
        p=j
        for n in range(len(lets)):
            while brdc[i][p] != '-':
                p += 1
            brdc[i][p] = lets[n]
    return brdc


### For scoring #########################


def boarddiff(board1,board2,vacant='-'):
    bd = copy.deepcopy(board2)
    for i in range(15):
        for j in range(15):
            if board2[i][j] == board1[i][j]: bd[i][j]=vacant
    return bd
        

def boardcount(board,let='-'):
    n=0
    for i in range(15):
        for j in range(15):
            if board[i][j]==let: n+=1
    return n
            

def scrabx(b,v):
    s = []
    b2 = b + list(zip(*b)) # the 30 "rows" of letters
    v2 = v + list(zip(*v)) # the uncovered values
    for i in range(len(b2)):
        c = b2[i]
        v = v2[i]
        cv = list(zip(c,v)) # zips the letter and bonus lists
        word = ''
        vvvv = ''
        start = (i,0)
        for n in range(15): # find all the strings in row
            if cv[n][0]=='-' or n==14: #nothing more to append
                if n == 14:
                    word = word + cv[n][0] # "word" is unchecked at this point
                    vvvv = vvvv + cv[n][1] # corresponding bonus 
                if len(word)>1:
                    if word.upper() not in wordset: return []
                    s.append([word,vvvv,start]) # store word, bonus and starting position
                word = '' # get ready for new word
                vvvv = '' # get ready for new bonusses
                start = (i,n+1) # construct new starting position
            else: # a letter is next, so appended to the growing word
                word = word + cv[n][0]
                vvvv = vvvv + cv[n][1]            
    return s


def newwords(a,b):
    c=[]
    for p in a:
        unique=True
        for q in b:
            if p[2]==q[2] and p[0]==q[0]: unique=False
        if unique:
            c.append(copy.deepcopy(p))
    return c
         

def coverbonus(board,bonus):
    for i in range(15):
        for j in range(15):
            if board[i][j] != '-': bonus[i][j]='.'


def scorewords(a):
    playtot = 0
    for lt, bn, loc in a:
        mult = 1
        wordtot = 0
        for i in range(len(lt)):
            letter=lt[i]
            bonus=bn[i]
            v = 0
            if letter in letter_values:
                v = letter_values[letter]
            if bonus=='d':
                v = v*2
            elif bonus=='t':
                v = v*3
            elif bonus=='D':
                mult = mult*2
            elif bonus=='T':
                mult = mult*3
            wordtot += v
        #print(wordtot,mult)
        wordtot = wordtot*mult
        playtot += wordtot
    return playtot              

def score(board1,board2,lets='',bonuss=None,prev=None):
    if not bonuss:
        bonuss = copy.deepcopy(bonusbrd)
        coverbonus(board1,bonuss)
    this=scrabx(board2,bonuss)
    if not this: return -1,[]
    if not prev:
        prev=scrabx(board1,bonuss)
    
    bd = boarddiff(board1,board2)
    nlets = 225 - boardcount(bd) #number of letters played
    
    youmade = newwords(this,prev)
    
    for thing in youmade:
        if thing[0].upper() not in wordset:
#            youscore=-1
            return -1, [] # score is -1, your play made invalid word
              
    youscore = scorewords(youmade)
    
    if nlets==7: youscore += 50
    
    return youscore,youmade


def sortplays(pd,aboard,penalty=0.,verbose=False):
    kys=sorted(pd.keys())
    n=0
    highest=0
    bestkey = None
    bestplays=[]        
    bonuss = copy.deepcopy(bonusbrd)
    coverbonus(aboard,bonuss)
    prev=scrabx(aboard,bonuss)
    
    for k in kys:
        lets=k[1]
        extra=0
        newboard = layplay(aboard,k)
        ks, kwords = score(aboard,newboard,bonuss=bonuss,prev=prev)
        ksp = ks - penalty*evaltiles(lets)
        if ks>0:
            bestplays.append((ksp,k))
        n+=1
    bestplays.sort()
    return bestplays


def evaltiles(tiles):
    total = 0
    for tile in tiles:
        if tile in letter_values:
            total += letter_values[tile]
    return total

### some classes:

class tilebox:
    def __init__(self):
        self.tiles=['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 
                    'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                    'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 
                    'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 
                    'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 
                    'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S',
                    'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 
                    'V', 'W', 'W', 'X', 'Y', 'Y', 'Z', '*', '*']
    def draw(self,num):
        numm = min(num, len(self.tiles) )
        hand = random.sample( self.tiles, numm )
        for tile in hand:
            self.tiles.remove(tile)
        return hand
    def __len__(self):
        return len(self.tiles)
    def count(self):
        return len(self.tiles)


class rack:
    def __init__(self):
        self.tiles=[]
    def fill(self,abag):
        need= 7-len(self.tiles)
        self.tiles += abag.draw(need)
    def play(self,lets):
        for let in lets:
            if let in 'abcdefghijklmnopqrstuvwxyz':
                let='*'
            self.tiles.remove(let)
    def exchange(self,abag,lets):
        for let in lets:
            self.tiles.remove(let)
            abag.tiles.append(let)
            self.tiles += abag.draw(1)       
    def __len__(self):
        return len(self.tiles)
    def count(self):
        return len(self.tiles)


class board:
    def __init__(self,old=None):
        if old==None:
            self.board=[['-']*15 for i in range(15)]
        else:
            self.board=copy.deepcopy(old)
        self.boards=[]
        self.bns =          """T--d---T---d--T
            -D---t---t---D-
            --D---d-d---D--
            d--D---d---D--d
            ----D-----D----
            -t---t---t---t-
            --d---d-d---d--
            T--d---D---d--T
            --d---d-d---d--
            -t---t---t---t-
            ----D-----D----
            d--D---d---D--d
            --D---d-d---D--
            -D---t---t---D-
            T--d---T---d--T""".replace(' ','')
    def show(self):
        for line in self.board:
            print(''.join(line))
            
    def ready(self):
        self.boards.append(copy.deepcopy(self.board))
    
    def lay(self,ply):       
        a,b = ply[0]
        lets = ply[1]
        if not (0<=a<30 and 0<=b<=15 and type(lets)==str) : return [] 
        self.ready()
        if a>14: # play down
            am = a-15
            p = b
            for n in range(len(lets)):
                while self.board[p][am] != '-':
                    if p==14:
                        self.re()
                        return []
                    p+=1
                self.board[p][am]=lets[n]
        else:
            p=b
            for n in range(len(lets)):
                while self.board[a][p] != '-':
                    if p==14:
                        self.re()
                        return []
                    p+=1
                self.board[a][p]=lets[n]
        thescore = score(self.boards[-1],self.board)
        return thescore
     
    def re(self):
        self.board = self.boards.pop()
        
    def ex(self):
        return copy.deepcopy(self.board)


class tilebox:
    def __init__(self):
        self.tiles=['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 
                    'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                    'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 
                    'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M', 
                    'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 
                    'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S',
                    'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 
                    'V', 'W', 'W', 'X', 'Y', 'Y', 'Z', '*', '*']
    def draw(self,num):
        numm = min(num, len(self.tiles) )
        hand = random.sample( self.tiles, numm )
        for tile in hand:
            self.tiles.remove(tile)
        return hand
    def __len__(self):
        return len(self.tiles)
    def count(self):
        return len(self.tiles)



class rack:
    def __init__(self):
        self.tiles=[]
    def fill(self,abag):
        need= 7-len(self.tiles)
        self.tiles += abag.draw(need)
    def play(self,lets):
        for let in lets:
            if let in 'abcdefghijklmnopqrstuvwxyz':
                let='*'
            self.tiles.remove(let)
    def exchange(self,abag,lets):
        for let in lets:
            self.tiles.remove(let)
            abag.tiles.append(let)
            self.tiles += abag.draw(1)       
    def __len__(self):
        return len(self.tiles)
    def count(self):
        return len(self.tiles)



class board:
    def __init__(self,old=None):
        if old==None:
            self.board=[['-']*15 for i in range(15)]
        else:
            self.board=copy.deepcopy(old)
        self.boards=[]
        self.bns =          """T--d---T---d--T
            -D---t---t---D-
            --D---d-d---D--
            d--D---d---D--d
            ----D-----D----
            -t---t---t---t-
            --d---d-d---d--
            T--d---D---d--T
            --d---d-d---d--
            -t---t---t---t-
            ----D-----D----
            d--D---d---D--d
            --D---d-d---D--
            -D---t---t---D-
            T--d---T---d--T""".replace(' ','')
    def show(self):
        for line in self.board:
            print(''.join(line))
            
    def ready(self):
        self.boards.append(copy.deepcopy(self.board))
    
    def lay(self,ply):       
        a,b = ply[0]
        lets = ply[1]
        if not (0<=a<30 and 0<=b<=15 and type(lets)==str) : return [] 
        self.ready()
        if a>14: # play down
            am = a-15
            p = b
            for n in range(len(lets)):
                while self.board[p][am] != '-':
                    if p==14:
                        self.re()
                        return []
                    p+=1
                self.board[p][am]=lets[n]
        else:
            p=b
            for n in range(len(lets)):
                while self.board[a][p] != '-':
                    if p==14:
                        self.re()
                        return []
                    p+=1
                self.board[a][p]=lets[n]
        thescore = score(self.boards[-1],self.board)
        return thescore
     
    def re(self):
        self.board = self.boards.pop()
        
    def ex(self):
        return copy.deepcopy(self.board)


