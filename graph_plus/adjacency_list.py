from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz

graphviz.__version__

class AdjacencyList:
    def __init__(self, edges_list: list[tuple[str, str]]):
        '''MainConstructor based in 1 list[edges] (ll).'''
        self.edges = edges_list

    @classmethod
    def from_dict_of_tuples(cls, data_dict: dict[str, tuple[str, ...]]):
        '''Constructor extra: genera the class a partir of 1 dict[tuple].'''
        edges_from_dict = []
        # Iterate the dict 4build the list[edges] traditionals (ll)
        for nodo_origen, vecinos in data_dict.items():
            for nodo_destino in vecinos:
                # Avoid duplicate edges invirtiendo the order (ex: if ya is B-A, no add A-B)
                if (nodo_destino, nodo_origen) not in edges_from_dict:
                    edges_from_dict.append((nodo_origen, nodo_destino))
        
        # cls(...) call 2constructor __init__ original passing the list that recently builded
        return cls(edges_list=edges_from_dict)
    
    def get_ll(self) -> list[tuple[str, str]]:
        '''-> list[edges] (ll) of graph.'''
        return self.edges

    def to_dataframe(self) -> pd.DataFrame:
        '''Tu mtd exact of conversion based in NetworkX w support for .T'''
        graph = nx.Graph(self.edges)
        dict_lists = nx.to_dict_of_lists(graph)
        df = pd.DataFrame.from_dict(dict_lists, orient='index').T
        return df.reindex(columns=sorted(df.columns)).fillna('-')