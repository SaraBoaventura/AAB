# -*- coding: utf-8 -*-
"""
@author: miguelrocha
"""

def createMatZeros (nl, nc):
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:

    def __init__(self, seqs):
        self.size = len(seqs[0])
        self.seqs = seqs # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doPseudoCounts()
        self.createPWM_pseudoCounts()
        
    def __len__ (self):
        return self.size        
   
    
    def doPseudoCounts(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs: # percorre cada sequencia
            for i in range(self.size): # o tamanho da sequencia s 
                lin = self.alphabet.index(s[i]) # linha
                self.counts[lin][i] += 1 # adiciona as contagens
        # adicionar mais um a todas as contagens 
        for i in range(len(self.counts)):
            for j in range(len(self.counts[0])):
                self.counts[i][j] += 1
          
            
    def createPWM_pseudoCounts(self):
        if self.counts == None: self.doCounts()
        sum = 0 
        # somatorio das colunas
        for i in range(len(self.counts)):
            sum += self.counts[i][0]
        self.pwm = createMatZeros(len(self.alphabet), self.size)    
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / sum
    
    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq):
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res
    
    def probAllPositions(self, seq):
        res = []
        for k in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq):
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat (motifs.counts) # pseudo-contagens 
    printMat (motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
