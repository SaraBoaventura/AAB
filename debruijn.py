# -*- coding: utf-8 -*-

from MyGraph import MyGraph

# Representação alternativa do problema 

# os fragmentos k-mers sõa arcos do grafo
# os nos sao seequencias de tamanho k-1 correspondendo a prefixos/sufixos destes fragmentos 
class DeBruijnGraph (MyGraph):  # subclasse da classe MyGraph 
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d): # admite arcos repetidos 
        if o not in self.graph.keys(): # adiciona o no de origem 
            self.add_vertex(o)
        if d not in self.graph.keys(): # adiciona o no de destino 
            self.add_vertex(d)
        self.graph[o].append(d) # adiciona o arco, podendo haver arcos repetidos 

    def in_degree(self, v):
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res
    
    # cria um grafo deBruijn 
    def create_deBruijn_graph(self, frags): # fragmentos 
        for seq in frags:
            suf = suffix(seq) 
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)
        

    def seq_from_path(self, path):
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq): 
    return seq[1:]
    
def prefix(seq):
    return seq[:-1]

def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res



def test1():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    
    
def test2():
    frags = ["ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    print (dbgr.check_nearly_balanced_graph())
    print (dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    db = DeBruijnGraph(frags)
    db.print_graph



test1()
print()
#test2()
#print()
#test3()
    
