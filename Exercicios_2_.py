# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 14:44:08 2021

@author: 35192
"""

class SuffixTree_2:
    
    def __init__(self):
        self.nodes = { 0:(-1,{}) } # root node
        #para cada nó existe um tuplo onde o 1º elemento é o nº do sufixo (para folhas) ou -1 (se
        #não é folha); o 2º elemento é o dicionário da Trie (símbolo -> nº de nó destino)
        self.num = 0
        self.seq1 = ''
        self.seq2 = ''
        
        
    # def print_tree(self):
    #     for k in self.nodes.keys():  # percorre as chaves dos nós, isto é, para cada cada nó 
    #         if self.nodes[k][0] < 0:
    #             # se o no for menor que zero, isto é menos um, é porque nao é uma folha  
    #             print (k, "->", self.nodes[k][1]) # dicionário anterior da trie, o simbolo e o nó de destino 
    #             # faz print do simbolo -> nº de nó destino 
                
    #         else: # significa que é uma folha 
    #             print (k, ":", self.nodes[k][0]) # faz print das folhas 
                
    def add_node(self, origin, symbol, leafnum = -1):
        self.num += 1 # dá o numero ao nó
        self.nodes[origin][1][symbol] = self.num # adiciona o numero do no ao dicionario 
        self.nodes[self.num] = (leafnum,{}) # tuplo que guarda as proximas posiçoes
        
    def add_suffix(self, p, sufnum):# padrao e posiçao no padrao
        pos = 0
        node = 0
        while pos < len(p): # Enquanto a posiçao for menor que o tamanho do padrao 
            if p[pos] not in self.nodes[node][1].keys(): # Se a letra na posição do padrao não estiver no nó[1] vai buscar o dicionário dentro do tuplo
                if pos == len(p)-1: # Se estiver no último caracter da sequência
                    self.add_node(node, p[pos], sufnum) # adiciona o nó e o numero
                else:
                    self.add_node(node, p[pos])   # adiciona o nó   
            node = self.nodes[node][1][p[pos]] # localizaçao do nó
            pos += 1 # incrementar a posiçao ate chegar ao tamanho do padrao que é quando pára
    
    def suffix_tree_from_seq(self, seq1,seq2):
        seq1 = seq1+"$" # sequencia 1 que termina com $
        seq2 = seq2+"#" # sequencia 2 que termina com # 
        for i in range(len(seq1)):
            self.add_suffix(seq1[i:], i)
            print(self.add_suffix(seq1[i:], i))
        for i in range(len(seq2)):
            self.add_suffix(seq2[i:], i)
            print(self.add_suffix(seq2[i:], i))
  
    def find_pattern(self, pattern):
        pos = 0
        node = 0
        for pos in range(len(pattern)):
            if pattern[pos] in self.nodes[node][1].keys():
                node = self.nodes[node][1][pattern[pos]]
                pos += 1
            else: return None
        return self.get_leafes_below(node)
    
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
    
   
    
    
    def largestCommonSubstring(self):
        seq1 = self.seq1
        seq2 = self.seq2
        substring = ''
        for i in range(len(seq1)): # percorre a sequencia 1
            for j in range(len(seq2)): # percorre a sequencia 2 
                k = 1
                # condiçao ate encontrarmos uma subrtring com comprimento menor que seq1 e seq2 
                while i+k <= len(seq1) and j+k <= len(seq2) and seq1[i:i+k] == seq2[j:j+k]:
                    if len(substring) <= len(seq1[i:i+k]): # permite encontrar a maior substring 
                        substring = seq1[i:i+k] # adiciona
                    k = k+1
        return substring
    
        
def test():
    seq1 = "TAC"
    seq2 = "ATA"
    #st = SuffixTree()
    st.suffix_tree_from_seq(seq1,seq2)
    #st.print_tree()
    #print (st.find_pattern("TA"))
    #print (st.find_pattern("ACG"))
    #print(st.get_leafes_below(7))
    #print(st.matches_prefix("TA"))
    print(st.largestCommonSubstring)
    
# def test2():
#     seq = "TACTA"
#     st = SuffixTree()
#     st.suffix_tree_from_seq(seq)
#     print (st.find_pattern("TA"))
#     #print(st.repeats(2,2))
    
    
test()
print()
# test2()
    