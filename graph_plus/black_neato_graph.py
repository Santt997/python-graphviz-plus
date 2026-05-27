from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz

graphviz.__version__

class BlackNeatoGraph(Graph):
    def __init__(
        self,
        name : str,
        ll: list[tuple[str, str] | tuple[str, str, dict[str, str]]],
        lp: list[tuple[str, str]] = [],
        engine: str = 'neato',
    ):
        super().__init__(name, engine=engine)
        self.attr(overlap='false', outputorder='edgesfirst')
        self.attr('node', shape='circle', fixedsize='true', width='.21', height='.21', fontsize='12', color='white', fontcolor='white')
        self.attr(bgcolor='black')
        self.attr('edge', color='white', penwidth='1.5')
        self.attr(start='eigen') 
        self.ll = ll

        for i in lp:
            self.node(i[0], pos=i[1])

        for i in ll:
            self.edge(i[0], i[1], **({} if len(i) == 2 else i[2]))
    
    @classmethod
    def from_dict_of_str_and_tuples_str(
        cls, 
        data_dict: dict[str, tuple[str, ...]], 
        lp: list[tuple[str, str]] = [], 
        name: str = 'G',
        engine: str = 'neato'  # <-- También por defecto 'neato'
    ):
        '''Constructor extra: genera el grafo directamente desde un dict[tuple] 
        de strings garantizando cero cruces si el grafo es planar.'''
        edges_list: list[tuple[str, str]] = []
        
        for nodo_origen, vecinos in data_dict.items():
            for nodo_destino in vecinos:
                ya_existe = any(
                    (e[0] == nodo_origen and e[1] == nodo_destino) or 
                    (e[0] == nodo_destino and e[1] == nodo_origen) 
                    for e in edges_list
                )
                if not ya_existe:
                    edges_list.append((nodo_origen, nodo_destino))
                    
        if not lp:
            graph = nx.Graph(edges_list)
            es_planar, embedding = nx.check_planarity(graph)
            
            if es_planar and embedding is not None:
                posiciones_calculadas = nx.combinatorial_embedding_to_pos(
                    embedding, 
                    fully_triangulate=True
                )
                lp = [
                    (str(nodo), f"{coords[0]*3.5},{coords[1]*3.5}!") 
                    for nodo, coords in posiciones_calculadas.items()
                ]
                    
        return cls(ll=edges_list, lp=lp, name=name, engine=engine)

    
    @classmethod
    def from_dict_of_int_and_tuples_int(cls, 
                          data_dict: dict[int, tuple[int, ...]], 
                          lp: list[tuple[str, str]] = [], 
                          name: str = 'G'):
        '''Constructor extra: genera el grafo desde un dict de enteros.'''
        edges_list: list[tuple[str, str]] = []
        
        for nodo_origen, vecinos in data_dict.items():
            # Convertimos el origen a texto
            origen_str = str(nodo_origen)
            
            for nodo_destino in vecinos:
                # Convertimos el destino a texto
                destino_str = str(nodo_destino)
                
                # Evitamos duplicar aristas en el grafo no dirigido
                ya_existe = any(
                    (e[0] == origen_str and e[1] == destino_str) or 
                    (e[0] == destino_str and e[1] == origen_str) 
                    for e in edges_list
                )
                
                if not ya_existe:
                    edges_list.append((origen_str, destino_str))
                    
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
    
    def is_planar(self) -> bool:
        '''Retorna True si el grafo es planar o False si no lo es.'''
        # 1. Limpiamos las aristas para NetworkX (tomando solo los dos primeros elementos)
        clean_edges = [(i[0], i[1]) for i in self.ll]
        
        # 2. Creamos el objeto Grafo de NetworkX
        graph = nx.Graph(clean_edges)
        
        # 3. Usamos la función nativa de NetworkX para verificar planaridad
        # check_planarity devuelve una tupla: (bool, PlanarEmbedding)
        # Solo nos interesa el primer valor (el booleano)
        es_planar, _ = nx.check_planarity(graph)
        
        return es_planar