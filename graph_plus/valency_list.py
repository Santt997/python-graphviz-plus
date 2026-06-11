from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz
from .black_neato_graph import BlackNeatoGraph

graphviz.__version__

class ValencyList:
    def __init__(self, edges: list[tuple[str, str] | tuple[str, str, dict[str, str]]]):
        self.edges = edges
        self._graph = nx.Graph(self._clean_edges(edges))
        self._degrees = dict(self._graph.degree())

    @classmethod
    def from_blackneatograph(cls, g: BlackNeatoGraph):
        '''
        Build the ValencyList directly from 1 BlackNeatoGraph.
        '''
        return cls(g.ll)

    @staticmethod
    def _clean_edges(edges: list[tuple[str, str] | tuple[str, str, dict[str, str]]]) -> list[tuple[str, str]]:
        return [(u, v) for u, v, *_ in edges]

    def raw(self) -> dict[bytes, bytes]:
        '''-> dict node -> valency'''
        return self._degrees

    def vals(self) -> list[bytes]:
        '''ValencyList !w sorted'''
        return list(self._degrees.values())

    def sorted(self, reverse: bool = True) -> list[bytes]:
        '''ValencyList sorted'''
        return sorted(self._degrees.values(), reverse=reverse)

    def sum_check(self) -> bool:
        '''Lema del apretón of hands: sum = 2|E|'''
        return sum(self._degrees.values()) == 2 * self._graph.number_of_edges()

    def is_regular(self) -> bool:
        '''All the nodes have same degree'''
        vals = set(self._degrees.values())
        return len(vals) == 1 if vals else True

    def max_valency(self) -> bytes | int:
        return max(self._degrees.values(), default=0)

    def min_valency(self) -> bytes | int:
        return min(self._degrees.values(), default=0)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            list(self._degrees.items()),
            columns=['node', 'valency']
        ).sort_values('valency', ascending=False)