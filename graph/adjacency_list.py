from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz

graphviz.__version__

class AdjacencyList:
    def __init__(self, edges_list: list[tuple[str, str]]):
        '''Constructor principal basado en una lista de aristas (ll).'''
        self.edges = edges_list

    @classmethod
    def from_dict_of_tuples(cls, data_dict: dict[str, tuple[str, ...]]):
        '''Constructor extra: genera la clase a partir de un dict de tuplas.'''
        edges_from_dict = []
        # Recorremos el diccionario para armar la lista de aristas tradicionales (ll)
        for nodo_origen, vecinos in data_dict.items():
            for nodo_destino in vecinos:
                # Evitamos duplicar aristas invirtiendo el orden (ej: si ya está B-A, no agregamos A-B)
                if (nodo_destino, nodo_origen) not in edges_from_dict:
                    edges_from_dict.append((nodo_origen, nodo_destino))
        
        # cls(...) llama al constructor __init__ original pasándole la lista que acabamos de armar
        return cls(edges_list=edges_from_dict)
    
    def get_ll(self) -> list:
        '''Retorna la lista de aristas (ll) del grafo.'''
        return self.edges

    def to_dataframe(self) -> pd.DataFrame:
        '''Tu método exacto de conversión basado en NetworkX con soporte para .T'''
        graph = nx.Graph(self.edges)
        dict_lists = nx.to_dict_of_lists(graph)
        df = pd.DataFrame.from_dict(dict_lists, orient='index').T
        return df.reindex(columns=sorted(df.columns)).fillna('-')