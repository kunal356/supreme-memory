from dataclasses import dataclass


@dataclass
class CostAtNode:
    node_id: int
    cost: int


@dataclass
class Node:
    id: int
    costs: list[CostAtNode] | None = None


@dataclass
class Traversal:
    nodes: list[Node]
    total_cost = 0
