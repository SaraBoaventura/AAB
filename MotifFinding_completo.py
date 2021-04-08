# -*- coding: utf-8 -*-
"""

"""

from MySeq import MySeq
from MyMotifs import MyMotifs
 

class MotifFinding:
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self):
        return len(self.seqs)
    
    def __getitem__(self, n):
        return self.seqs[n]
    
    def seqSize (self, i):
        return len(self.seqs[i])
    
    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score
   
    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score     
       
    # EXHAUSTIVE SEARCH
    def nextSol (self, s):
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize: # enqunato nao chegar ao fim
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos):  # vai percorrer o vetor de posiçoes iniciais 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1;
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    # Criar as varias possibilidades das posiçoes iniciais  
    # e avaliar cada um desses vetores de posicoes iniciais
    # de acordo com o score
    def exhaustiveSearch(self):
        melhorScore = -1
        res = [] # guarda as posiçoes iniciais
        s = [0]* len(self.seqs)
        while s is not None:
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res
     
    # BRANCH AND BOUND     
    # se estiver num folha salta para a folha seguinte 
    # se estiver num vertice salta para o vertice seguinte 
    def nextVertex (self, s): # s são posiçoes parciais 
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res
    
    
    def bypass (self, s):
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
    
    
    def branchAndBound (self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size # vetor posicao iniicial (0,0,0)
        while s is not None: # avalia todas as folhas iniciais 
            if len(s) < size: 
                optimScore = self.score(s) + (size-len(s)) * self.motifSize 
                if optimScore < melhorScore: 
                    s = self.bypass(s) # utiliza o bypass
                else: 
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        # procura as posiçoes para o motif nas 2 primeiras sequencias 
        # Procura exaustiva nas duas primeiras sequencias 
        mf = MotifFinding(self.motifSize, self.seqs[:2]) # procura o motif nas duas primeiras sequencias 
        s = mf.exhaustiveSearch() # vetor com as posiçoes iniciais do motif 
        # avalia a melhor posicao para cada uma das sequencias
        # seguintes uma a uma, guardando a melhor posicao (maximiza o score)
        for i in range (2,len(self.seqs)): # percorrer as outras sequencias 
                                      # adicionar a melhor posiçao em cada uma das sequencias 
            s.append(0) # adcionar ao nosso vetor as posiçoes das outras sequencias pois so temos as posicoes para as duas primeiras sequencias
            melhorScore = -1 
            melhorPosicao = 0
            for j in range(self.seqSize(i) - self.motifSize + 1):
                s[i] = j # vetor posiçoes 
                score_atual = self.score(s)
                if score_atual > melhorScore: # adiciona o melhor score e a melhor posicao 
                    melhorScore = score_atual
                    melhorPosicao = j
                s[i] = melhorPosicao
        return s

    # Consensus (heuristic)

    def heuristicStochastic (self):
        from random import randint
        s = [0] * len(self.seqs)
        # passo 1: inicia todas as posiçoes com valores aleatorios 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) # de 0 ate ao tamanho maximo (no randint o maximo ja e incluisve nas lista nao incluem o ultimo numero por isso coloca-se mais um)
         
        best_score = self.score(s) # calcula o score com base nas posiçoes s 
        improve = True  # melhorias
        while improve: # faz o ciclo enquanto ha melhorias quando 
            # passo 2:
            # criar o perfil com base nas posiçoes inicais s    
            motif = self.createMotifFromIndexes(s) # criar o motif 
            motif.createPWM()
            # passo 3:
            # avalia a melhor posicao inicial para cada sequencia
            # com base no perfil 
            for i in range(len(self.seqs)): 
                s[i] = motif.mostProbableSeq(self.seqs[i])
            # passo 4:    
            # verifica se houve melhoria 
            scr = self.score(s)
            if scr > best_score:  
                best_score = scr
            else:# se nao houver melhoria o improve é False e entao o ciclo pára
                improve = False 
        return s

    # Gibbs sampling

    def gibbs (self):
        from random import randint
        s = [0] * len(self.seqs)
        # passo 1: 
        # inicia todas as posiçoes com valores aleatorios 
        for i in range(len(self.seqs)):
            s[i] = randint(0, self.seqSize(i) - self.motifSize) # de 0 ate ao tamanho maximo (no randint o maximo ja e incluisve nas lista nao incluem o ultimo numero por isso coloca-se mais um)
        best_score = self.score(s)
        improve = True 
        while improve:
            # passo 2: 
            # Escolher uma das sequencia aleatoriamente 
            seq_idx = randint(0, len(self.seqs)-1)
            # Passo 3: 
            # criar o perfil sem a sequencia escolhida aleatoriamente     
            # remover a sequencia aleatoria da lista de sequencias
            seq = self.seqs.pop(seq_idx)
            # remover a posicao da sequencia aletatoria no vetor de posicoes iniciais 
            s_partial = s.copy()
            s_partial.pop(seq_idx) 
            # criar o perfil sem a sequencia removida
            motif = self.createMotifFromIndexes(s_partial)
            motif.createPWM()
            # melhor posicao inicial na sequencia considerando o perfil
            s[seq_idx] = motif.mostProbableSeq(seq) 
            # voltar a inserir a sequencia aleatoria 
            self.seqs.insert(seq_idx,seq) 
            # calcula o novo score 
            scr = self.score(s)
            # verifica se houve melhoria     
            if  scr > best_score:
                best_score = scr 
            else:
                improve = False 
        return s


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1

# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    sol2 = mf.gibbs()
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))

test4()
