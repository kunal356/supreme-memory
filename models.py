"""Pydantic models used for both domain logic and FastAPI I/O."""
from typing import List, Optional
from pydantic import BaseModel, Field


class CostAtNode(BaseModel):
    """A unit of cost attached to a specific node."""
    node_id: int = Field(ge=0, description="Identifier of the node this cost applies to (0-based).")
    cost: int = Field(description="Integer cost value to be summed into traversal totals.")


class Node(BaseModel):
    """A node in a traversal path."""
    id: int = Field(ge=0, description="Unique identifier for the node (0-based).")
    # Populated during computation. Optional to keep request payloads lightweight.
    costs: Optional[List[CostAtNode]] = Field(
        default=None,
        description="List of costs that apply to this node; populated during computation."
    )


class Traversal(BaseModel):
    """A traversal path composed of nodes with an aggregated total cost."""
    nodes: List[Node]
    total_cost: int = Field(
        default=0,
        description="Accumulated sum of costs on nodes in this traversal."
    )
