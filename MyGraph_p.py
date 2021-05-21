# -*- coding: utf-8 -*-

## Graph represented as adjacency list using a dictionary
## keys are vertices
## values of the dictionary represent the list of adjacent vertices of the key node

class MyGraph_p:
    
    def __init__(self, g = {}):
        ''' Constructor - takes dictionary to fill the graph as input; default is empty dictionary '''
        self.graph = g    

    def print_graph(self):
        ''' Prints the content of the graph as adjacency list '''
        for v in self.graph.keys():
            print (v, " -> ", self.graph[v])

    ## get basic info

    def get_nodes(self):
        ''' Returns list of nodes in the graph '''
        return list(self.graph.keys())
        
    def get_edges(self): 
        ''' Returns edges in the graph as a list of tuples (origem,destino,peso) '''
        edges = []
        for v in self.graph.keys(): # nós , origem 
            for dest in self.graph[v]: # destino daquele nó  
                p,d = dest # peso
                edges.append((v,d),p) ## peso numerico associado a cada arco 
        return edges  # retorna um tuplo ccom a origem destino e o peso associado a cada arco 
      
    def size(self):
        ''' Returns size of the graph : number of nodes, number of edges '''
        return len(self.get_nodes()), len(self.get_edges())
      
    ## add nodes and edges    
    
    def add_vertex(self, v):
        ''' Add a vertex to the graph; tests if vertex exists not adding if it does '''
        if v not in self.graph.keys():
            self.graph[v] = [ ]
    
    # uma aresta é uma ligação entre dois vertices     
    def add_edge(self, o, d, p):
        ''' Add edge to the graph; if vertices do not exist, they are added to the graph ''' 
        if o not in self.graph.keys():   # se o vertice o (vrestice de origem) nao existir
            self.add_vertex(o)           # adiciona 
        if d not in self.graph.keys():   # se o vertice d (vertice de destino) nao existir
            self.add_vertex(d)           # adiciona
        if d not in self.graph[o]:       # se o grafo nao existir 
            self.graph[o].append((d,p))  # adiciona o grafo à lista que contem os grafosc com o peso associado  
    
    ## successors, predecessors, adjacent nodes
            
    def get_successors(self, v): # da lista de nós sucessores do nó v 
        return list(self.graph[v])     # needed to avoid list being overwritten of result of the function is used
             
    def get_predecessors(self, v): # dá lista de nós antecessores do nó v 
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res
         
    def get_adjacents(self, v): # dá lista de nós adjacentes do nó v 
        suc = self.get_successors(v) # sucessores 
        pred = self.get_predecessors(v) # predecessores 
        res = pred
        for p in suc: # procura na lista dos sucessores 
            if p not in res: # se ainda nao foi adicionado 
                res.append(p) # adiciona 
        return res
    
    ## degrees    
    
    def out_degree(self, v): # calcula grau de saída do nó v 
        #return len(self.get_successors(v))
        return len(self.graph[v])
    
    def in_degree(self, v): # calcula o grau de entrada do nó v
        return len(self.get_predecessors(v))
        
    def degree(self, v): #calcula grau do nó v (todos os nós Adjacentes quer percursores quer sucessores)
        return len(self.get_adjacents(v))
        
    
    # BFS and DFS searches    
    # nós atingíveis são aqueles para os quais existe um caminho com origem em v 
    # e final nesse mesmo nó
    
    # começa pelo nó origem, depois explora todos os seus
    # sucessores, depois os sucessores destes, e assim sucessivamente
    # até todos os nós atingíveis terem sido explorados
    def reachable_bfs(self, v): # travessia em largura 
        l = [v]  # nos que se vai visitar, procurar 
        res = [] # lista que guarda todos os nos atingiveis 
        while len(l) > 0: # para quando tiver percorrido todos os nos na lista l
            node = l.pop(0) # por onde se começa a procurar, pelo primeiro elemento. vai-se eliminando da lista l a medida que se procura ate nao restar nenhum
            if node != v: # o v nao conta
                res.append(node)
            for elem in self.graph[node]: # percorre os nós de destido (procura o destino do no de origem, v)
                if elem[0] not in res and elem[0] not in l and elem[0] != node: # se nao estiverem na lista res e na lista l e diferente de do node em questao 
                    l.append(elem[0]) # adiciona  a lista l 
        return res
    
    # começa pelo nó origem e explora o 1º
    # sucessor, seguido pelo 1º sucessor deste e assim sucessivamente
    # até não haver mais sucessores e ter que se fazer “backtracking”    
    def reachable_dfs(self, v): # travessia em profundidade 
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v:
                res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem[0] not in res and elem[0] not in l:
                    l.insert(s, elem[0]) # so insere o primeiro antecessor 
                    s += 1
        return res    
    
    def distance(self, s, d): # s é o no inicial d é o destino
        if s == d: 
            #return 0
            print("A distancia é zero")
        else:
            l = [(s,0)]
            visited = [s]
            while len(l) > 0:
                node, dist = l.pop(0)
                for elem in self.graph[node]: # percorrer os nós 
                    n = elem[0]               # no de destino 
                    p = elem[1]               # peso
                    if n == d:                # quando chegar ao destino 
                        return (dist + p)     # retorna a distancia que é a soma dos pesos 
                    if n not in visited and n not in l and n != node:
                        l.append((n,dist+p)) # adiciona ao caminho o nó que estamos a ver 
                        visited.append(n)           
        return None
        
    # algoritmo djiskra
    def shortest_path(self, s, d):
        if s == d: 
            return [s,d]  # o camiho mais curto sao os respetivos nos 
        else:
            l = [(s,[]),1000000] # s é o vertice de origem, [] os vertices que serao visitados, infinito 
            visited = [s]       # guarda os nos que ja foram visitados 
            while len(l) > 0:   # enquanto houver elementos na lista l
                node, preds, p = l.pop(0) # preds  sao os nos qie precedem aquele no 
                for elem in self.graph[node]: # pesquisa os nos na lista 
                    n = elem[0] #  no de destino  
                    peso = elem[1] # peso
                    if n == d:     # se o n for o no de origem, signifca que ja chegou ao destino 
                        return preds+[(node,n)], p+peso   # retorna a lista com os nos que percorre e a distancia, isto e, o peso total. Node sao todos os nos percorridos, n é o ultimo
                    if peso < p: # verificar se o peso é menos que o anterior 
                        p = peso # se sim aceita-se,
                        n_n = n     # guarda-se o no numa nova variavel 
                        if n_n not in visited:  # se nao estiver na lista visited, ou seja, nao foi visitado 
                            l.append((n_n,preds+[node,n_n]),p+peso) # adiciona o elemento e o no ao caminho 
                            visited.append(node) # adiciona a lista dos nos visitados 
        return None
    
    #como modificar este algoritmo de forma a nao termos problemas de memeoria pois guarda todas as listas 
    #guardar so o no anterior e assim consgeuir recuperar o caminho para cada no 
    
        
    def reachable_with_dist(self, s):
        res = [] # todos os nos e as distancias <<
        l = [(s,0)]
        while len(l) > 0:
            node, dist, p = l.pop(0) # acrescentar o peso 
            if node != s: 
                res.append((node,dist),p) 
            for elem in self.graph[node]:
                n = elem[0]
                p = elem[1]
                if not is_in_tuple_list(l,elem) and not is_in_tuple_list(res,n): 
                    l.append((n,dist+p))
        return res

## cycles
    def node_has_cycle (self, v):
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem[0] == v: 
                    return True
                elif elem[0] not in visited:
                    l.append(elem[0])
                    visited.append(elem[0])
        return res

    def has_cycle(self):
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): 
                return True
        return res


def is_in_tuple_list (tl, val):
    res = False
    for (x,y) in tl:
        if val == x: 
            return True
    return res


def test1():
    gr = MyGraph_p( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
    gr.print_graph()
    print (gr.get_nodes())
    print (gr.get_edges())
    

def test2():
    gr2 = MyGraph_p()
    gr2.add_vertex(1)
    gr2.add_vertex(2)
    gr2.add_vertex(3)
    gr2.add_vertex(4)
    
    gr2.add_edge(1,2)
    gr2.add_edge(2,3)
    gr2.add_edge(3,2)
    gr2.add_edge(3,4)
    gr2.add_edge(4,2)
    
    gr2.print_graph()
    
# teste com os pesos associados   
def test3():
    gr = MyGraph_p( {1:[(2,1)], 2:[(3,1)], 3:[(2,1),(4,1)], 4:[(2,1)]} )
    gr.print_graph()

    print (gr.get_successors(2))
    print (gr.get_predecessors(2))
    print (gr.get_adjacents(2))
    print (gr.in_degree(2))
    print (gr.out_degree(2))
    print (gr.degree(2))
    print(gr.reachable_bfs(2))
    print(gr.reachable_dfs(2))
 
# com pesos    
def test4():
    gr = MyGraph_p( {1:[(2,2)], 2:[(3,3)], 3:[(2,1),(4,1)], 4:[(2,3)]} )
    
    print (gr.distance(1,4))
    print (gr.distance(4,3))

    print (gr.shortest_path(1,4))
    print (gr.shortest_path(4,3))

    print (gr.reachable_with_dist(1))
    print (gr.reachable_with_dist(3))

    #gr2 = MyGraph_p( {1:[(2,1),(3,1)], 2:[(4,1)], 3:[(5,1)], 4:[], 5:[]} )
    gr2 = MyGraph_p({1:[(2,1)], 2:[(3,1)], 3:[(2,1),(4,1)], 4:[(2,1)]})
    print (gr2.distance(2,1))
    print (gr2.distance(1,5))
    
    # print (gr2.shortest_path(1,5))
    # print (gr2.shortest_path(2,1))

    # print (gr2.reachable_with_dist(1))
    # print (gr2.reachable_with_dist(5))

def test5():
    gr = MyGraph_p( {1:[(2,1)], 2:[(3,1)], 3:[(2,2),(4,4)], 4:[(2,3)]} )
    print (gr.node_has_cycle(2))
    print (gr. node_has_cycle(1))
    print (gr.has_cycle())

    # gr2 = MyGraph_p( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
    # print (gr2. node_has_cycle(1))
    # print (gr2.has_cycle())


if __name__ == "__main__":
    #test1()
    #test2()
    #test3()
    test4()
    #test5()
