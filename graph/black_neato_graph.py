from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz

graphviz.__version__

class BlackNeatoGraph(Graph):
    def __init__(self, ll: list[tuple[str, str] | tuple[str, str, dict[str, str]]], lp: list[tuple[str, str]] = [], name : str='G'):
        super().__init__(name, engine='neato')
        self.attr(overlap='false', outputorder='edgesfirst')
        self.attr('node', shape='circle', fixedsize='true', width='.21', height='.21', fontsize='12', color='white', fontcolor='white')
        self.attr(bgcolor='black')
        self.attr('edge', color='white', penwidth='1.5')
        self.ll = ll

        for i in lp:
            self.node(i[0], pos=i[1])

        for i in ll:
            self.edge(i[0], i[1], **({} if len(i) == 2 else i[2]))
    
    @classmethod
    def from_dict_of_tuples(cls, 
                            data_dict: dict[str, tuple[str, ...]], 
                            lp: list[tuple[str, str]] = [], 
                            name: str = 'G'):
        '''Constructor extra: genera el grafo directly from 1 dict[tuple].'''
        edges_list: list[tuple[str, str] | tuple[str, str, dict[str, str]]] = []
        
        for nodo_origen, vecinos in data_dict.items():
            for nodo_destino in vecinos:
                # Evita duplicar aristas simples en el grafo no dirigido
                if (nodo_destino, nodo_origen) not in [(e[0], e[1]) for e in edges_list]:
                    edges_list.append((nodo_origen, nodo_destino))
                    
        return cls(ll=edges_list, lp=lp, name=name)

    # Getters & Setters
    def list_of_adyacency(self) -> pd.DataFrame:
        # 1. Creamos the DataFrame from the dict of form secure
        # 2. w .T lo damos vuelta 4q the keys pasen a be cols
        print('List of adyacency')
        df : pd.DataFrame = pd.DataFrame.from_dict(nx.to_dict_of_lists(nx.Graph(self.ll)), orient='index').T

        # 3. Sort the cols alphabeticly & refill the void of node E
        return df.reindex(columns=sorted(df.columns)).fillna('-')
    
    def get_valency_max(self) -> int:
        '''Retorna the grade (valency) max present in the graph.'''
        # 1. Limpiamos las aristas para NetworkX (tomando solo los dos primeros elementos)
        clean_edges = [(i[0], i[1]) for i in self.ll]
        graph = nx.Graph(clean_edges)
        
        # 2. graph.degree devuelve tuplas (nodo, grado). Buscamos el valor máximo.
        grados = [grado for nodo, grado in graph.degree()]
        return max(grados) if grados else 0

    def get_valency_min(self) -> int:
        '''Retorna el grado (valencia) mínimo presente in el graph.'''
        # 1. Limpiamos las aristas para NetworkX
        clean_edges = [(i[0], i[1]) for i in self.ll]
        graph = nx.Graph(clean_edges)
        
        # 2. Buscamos el valor mínimo entre todos los grados calculados
        grados = [grado for nodo, grado in graph.degree()]
        return min(grados) if grados else 0
    
    def is_regular(self) -> bool:
        '''Determina si el grafo es regular (todos los nodos tienen el mismo grado).'''
        clean_edges = [(i[0], i[1]) for i in self.ll]
        graph = nx.Graph(clean_edges)
        
        grados = [grado for nodo, grado in graph.degree()]
        return len(set(grados)) == 1 if grados else True  # Si no hay nodos, consideramos que es regular