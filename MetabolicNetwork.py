# -*- coding: utf-8 -*-

from MyGraph import MyGraph

# Rede de metabolitos, onde nós são os compostos e reações são
# representadas pelos arcos do grafo

# Rede de reações, onde nós são reações e arcos representam ligações
# entre reações por metabolitos comuns

# Rede de metabolitos e reações, onde nós são compostos e reações,
# sendo os arcos indicativos da participação dos compostos em reações
# como substratos ou produtos


class MetabolicNetwork (MyGraph): # sub classe da classe Mygraph 
    
    # atributos da classe 
    def __init__(self, network_type = "metabolite-reaction", split_rev = False):
        MyGraph.__init__(self, {})
        self.net_type = network_type # tipo de rede “metabolite-reaction”, “reaction”, “metabolite”
        self.node_types = {}         # tipo de nós. um dicionario
        if network_type == "metabolite-reaction": # se for deste tipo ha dois tipos de nos 
            self.node_types["metabolite"] = [] 
            self.node_types["reaction"] = []
        self.split_rev =  split_rev  # as reações reversivas se sao ou nao separadas (por exemplo R3-a  e R3-b)(True ou False)
    
    def add_vertex_type(self, v, nodetype): # adiciona um vertice/no
        self.add_vertex(v)
        self.node_types[nodetype].append(v) # ao adicionar o no diz qual o tipo de no (metabolito ou reaçao)
    
    def get_nodes_type(self, node_type): # obter o tipo de nos 
        if node_type in self.node_types: # vai ao dicionario de todos os nos 
            return self.node_types[node_type] # e retorna o tipo de no  
        else:  # se o no nao existir na lista 
            return None # retorna none 
    
    def load_from_file(self, filename): # le um ficheiro onde cada reçao é definida numa linha 
        rf = open(filename)
        gmr = MetabolicNetwork("metabolite-reaction") # grafo bipartido 
        for line in rf:
            if ":" in line:
                tokens = line.split(":")
                reac_id = tokens[0].strip()
                gmr.add_vertex_type(reac_id, "reaction")
                rline = tokens[1]
            else: raise Exception("Invalid line:")                
            if "<=>" in rline:
                left, right = rline.split("<=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_vertex_type(reac_id+"_b", "reaction")
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id+"_b", met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    if self.split_rev:
                        gmr.add_edge(met_id, reac_id+"_b")
                        gmr.add_edge(reac_id, met_id)
                    else:
                        gmr.add_edge(met_id, reac_id)
                        gmr.add_edge(reac_id, met_id)
            elif "=>" in line:
                left, right = rline.split("=>")
                mets_left = left.split("+")
                for met in mets_left:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(met_id, reac_id)
                mets_right = right.split("+")
                for met in mets_right:
                    met_id = met.strip()
                    if met_id not in gmr.graph:
                        gmr.add_vertex_type(met_id, "metabolite")
                    gmr.add_edge(reac_id, met_id)
            else: raise Exception("Invalid line:")    

        
        if self.net_type == "metabolite-reaction": 
            self.graph = gmr.graph
            self.node_types = gmr.node_types
        elif self.net_type == "metabolite-metabolite":
            self.convert_metabolite_net(gmr)
        elif self.net_type == "reaction-reaction": 
            self.convert_reaction_graph(gmr)
        else: self.graph = {}
        
    # converter uma rede to tipo metabolitos para reaction    
    def convert_metabolite_net(self, gmr):     # gmr é o grafo existente 
        for m in gmr.node_types["metabolite"]: # vai ao nós do tipo metabolito 
            self.add_vertex(m)                 # adiciona no grafo o vertice 
            sucs = gmr.get_successors(m)       # o vertice sucessor (sao do tipo reactions)
            for s in sucs:                     # vais aos sucessores 
                sucs_r = gmr.get_successors(s) # sucessores dos sucessores  (que sao os metabolitos)
                for s2 in sucs_r:   
                    if m !=s2:                 # se o vertice sucessor nao for igual ao vertice em questão
                        self.add_edge(m,s2)    # liga o vertice aos seus sucessores, cria a "aresta"
            pass

    # converter uma rede to tipo reaçoes para metabolito    
    def convert_reaction_graph(self, gmr): 
        for r in gmr.node_types["reaction"]:
            self.add_vertex(r)
            sucs = gmr.get_successors(r)
            for s in sucs:
                sucs_r = gmr.get_successors(s)
                for s2 in sucs_r:
                    if r !=s2:
                        self.add_edge(r,s2)
            pass

# faz a rede de metabolitos e reaçoes slide 6 
def test1():
    m = MetabolicNetwork("metabolite-reaction")
    m.add_vertex_type("R1","reaction")
    m.add_vertex_type("R2","reaction")
    m.add_vertex_type("R3","reaction")
    m.add_vertex_type("M1","metabolite")
    m.add_vertex_type("M2","metabolite")
    m.add_vertex_type("M3","metabolite")
    m.add_vertex_type("M4","metabolite")
    m.add_vertex_type("M5","metabolite")
    m.add_vertex_type("M6","metabolite")
    m.add_edge("M1","R1")
    m.add_edge("M2","R1")
    m.add_edge("R1","M3")
    m.add_edge("R1","M4")
    m.add_edge("M4","R2")
    m.add_edge("M6","R2")
    m.add_edge("R2","M3")
    m.add_edge("M4","R3")
    m.add_edge("M5","R3")
    m.add_edge("R3","M6")
    m.add_edge("R3","M4")
    m.add_edge("R3","M5")
    m.add_edge("M6","R3")
    m.print_graph()
    print("Reactions: ", m.get_nodes_type("reaction") )
    print("Metabolites: ", m.get_nodes_type("metabolite") )

def test2():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("example-net.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("example-net.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("example-net.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("example-net.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("example-net.txt")
    rrsn.print_graph()
    print()


# aplicaçao a ecoli         
def test3():
    print("metabolite-reaction network:")
    mrn = MetabolicNetwork("metabolite-reaction")
    mrn.load_from_file("ecoli.txt")
    mrn.print_graph()
    print("Reactions: ", mrn.get_nodes_type("reaction") )
    print("Metabolites: ", mrn.get_nodes_type("metabolite") )
    print()
    
    print("metabolite-metabolite network:")
    mmn = MetabolicNetwork("metabolite-metabolite")
    mmn.load_from_file("ecoli.txt")
    mmn.print_graph()
    print()
    
    print("reaction-reaction network:")
    rrn = MetabolicNetwork("reaction-reaction")
    rrn.load_from_file("ecoli.txt")
    rrn.print_graph()
    print()
    
    print("metabolite-reaction network (splitting reversible):")
    mrsn = MetabolicNetwork("metabolite-reaction", True)
    mrsn.load_from_file("ecoli.txt")
    mrsn.print_graph()
    print()
    
    print("reaction-reaction network (splitting reversible):")
    rrsn = MetabolicNetwork("reaction-reaction", True)
    rrsn.load_from_file("ecoli.txt")
    rrsn.print_graph()
    print()
    
    # GRAUS
    print (mrn.mean_degree("out")) # media do grau calculada sobre todos os nos 
    d = mrn.prob_degree("out")     # ?? 
    for x in sorted(d.keys()):
        print (x, "\t", d[x] ) # da a probabilidade grau de cada no ?
        
    # metricas de centralidade 
    # for x in mrn.graph.keys(): # percorre todos os no do grafo?
    #     print(" Clonesss centrality:", mrsn.closeness_centrality(x))
    #     print(" Highest closeness:", mrsn.highest_closeness)
    #     print(" betweenness centrality:", mrsn.betweenness_centrality(x))


#test1()
print()
#test2()
test3()

    
                  
# CLUSTERING
#Para medir até que ponto cada nó está inserido num grupo
#coeso, é definido o coeficiente de clustering, que se define para
#cada nó como:
#nº de arcos existentes entre vizinhos do nó /nº total de arcos que poderiam existir entre vizinhos do nó    
gr = MyGraph( {1:[2], 2:[3], 3:[2,4], 4:[2]} )
print (gr.clustering_coef(1))
print (gr.clustering_coef(2))
gr2 = MyGraph( {1:[2,3], 2:[4], 3:[5], 4:[], 5:[]} )
print (gr2.clustering_coef(1))
gr3 = MyGraph( {1:[2,3], 2:[1,3], 3:[1,2]} )
print (gr3.clustering_coef(1))
  
# ha medida que o grau aumenta o coeficente de clustering é mais pequeno 

# metricas de centralidade 
print("Clonesss centrality:", gr.closeness_centrality(1))
print("Highest closeness:", gr.highest_closeness)
print("betweenness centrality:", gr.betweenness_centrality(1))








