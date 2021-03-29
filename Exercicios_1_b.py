# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 15:01:42 2021

@author: 35192
"""



class SuffixTree:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        #para cada nó existe um tuplo onde o 1º elemento é o nº do sufixo (para folhas) ou -1 (se
        #não é folha); o 2º elemento é o dicionário da Trie (símbolo -> nº de nó destino)
        self.num = 0
    
    def print_tree(self):
        for k in self.nodes.keys():  # percorre as chaves dos nós, isto é, para cada cada nó 
            if self.nodes[k][0] < 0:
                # se o no for menor que zero, isto é menos um, é porque nao é uma folha  
                print (k, "->", self.nodes[k][1]) # dicionário anterior da trie, o simbolo e o nó de destino 
                # faz print do simbolo -> nº de nó destino 
                
            else: # significa que é uma folha 
                print (k, ":", self.nodes[k][0]) # faz print das folhas 
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1
        self.nodes[origin][1][symbol] = self.num
        self.nodes[self.num] = (leafnum,{})
        
    def add_suffix(self, p, sufnum):
        pos = 0
        node = 0
        while pos < len(p):
            if p[pos] not in self.nodes[node][1].keys():
                if pos == len(p)-1:
                    self.add_node(node, p[pos], sufnum)
                else:
                    self.add_node(node, p[pos])     
            node = self.nodes[node][1][p[pos]]
            pos += 1
    
    def suffix_tree_from_seq(self, text):
        t = text+"$"
        for i in range(len(t)):
            self.add_suffix(t[i:], i)
            print(self.add_suffix(t[i:], i))
  
    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
                pos += 1
            else: return None
        return self.get_leafes_below(node)
    
    ####################################### EX1 b)
    
    # def matches_prefix(self, prefix):
    #     pos = 0
    #     match = ""
    #     node = 0
    #     while pos < len(prefix):
    #         if prefix[pos] in self.nodes[node][1].keys():
    #             node = self.nodes[node][1][prefix[pos]]
    #             print(node)
    #             match += prefix[pos]
    #             if self.nodes[node] == {}: 
    #                 return match
    #             else:
    #                 pos += 1   
    #         else: return None
    #     return None
    
        

    def get_leafes_below(self, node): # diz quais as folhas que estao abaixo de um determinado nó 
        res = []
        if self.nodes[node][0] >= 0: # significa que é uma folha, nao queremos descer mais na arvore e por isso retornamos esse valor 
            res.append(self.nodes[node][0])  # adiciona o valor da folha  
        else: # caso se encontre menos, quer dizer que ainda nao chegamos as folhas da arvore e temos de continuar a descer 
            for k in self.nodes[node][1].keys(): # percorrer todos os nós abaixo do nó que nos enocntramos 
                newnode = self.nodes[node][1][k] # se for um nó continua o ciclo 
                leafes = self.get_leafes_below(newnode) # se for uma folha retorna 
                res.extend(leafes) # adiciona a lista novamente 
        return res
    
   
def test():
    seq = "TACTA"
    st = SuffixTree()
    st.suffix_tree_from_seq(seq)
    #st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))
    print(st.nodes_below(3))
    #print(st.get_leafes_below(7))
    #print(st.matches_prefix("TA"))
    
# def test2():
#     seq = "TACTA"
#     st = SuffixTree()
#     st.suffix_tree_from_seq(seq)
#     print (st.find_pattern("TA"))
#     #print(st.repeats(2,2))
    
    
test()
print()
# test2()



