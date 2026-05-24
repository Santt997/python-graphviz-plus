from graphviz import Graph
import networkx as nx
import pandas as pd
import graphviz

graphviz.__version__

class ValencyList:
    def __init__(self, edges: list[tuple[str, str]]):
        self.edges = edges
        self._graph = nx.Graph(self._clean_edges(edges))
        self._degrees = dict(self._graph.degree())

    @classmethod
    def from_blackneatograph(cls, g: "BlackNeatoGraph"):
        """
        Construye la ValencyList directamente desde un BlackNeatoGraph.
        """
        return cls(g.ll)

    @staticmethod
    def _clean_edges(edges):
        return [(u, v) for u, v, *_ in edges]

    def raw(self) -> dict[str, int]:
        """Retorna dict nodo -> valencia"""
        return self._degrees

    def values(self) -> list[int]:
        """Lista de valencias sin ordenar"""
        return list(self._degrees.values())

    def sorted(self, reverse: bool = True) -> list[int]:
        """Lista de valencias ordenada"""
        return sorted(self._degrees.values(), reverse=reverse)

    def sum_check(self) -> bool:
        """Lema del apretón de manos: suma = 2|E|"""
        return sum(self._degrees.values()) == 2 * self._graph.number_of_edges()

    def is_regular(self) -> bool:
        """Todos los nodos tienen mismo grado"""
        vals = set(self._degrees.values())
        return len(vals) == 1 if vals else True

    def max_valency(self) -> int:
        return max(self._degrees.values(), default=0)

    def min_valency(self) -> int:
        return min(self._degrees.values(), default=0)

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(
            list(self._degrees.items()),
            columns=["node", "valency"]
        ).sort_values("valency", ascending=False)