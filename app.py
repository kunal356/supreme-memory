"""FastAPI service exposing the traversal cost computation."""
from typing import List
from fastapi import FastAPI, HTTPException
from models import Traversal, Node, CostAtNode
from funcs import improved_logic

app = FastAPI(title="Traversal Cost API", version="1.0.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/compute", response_model=List[Traversal])
def compute(traversals: List[Traversal], pathCosts: List[CostAtNode]):
    """Compute total_cost per traversal; validates cost.node_id membership."""
    # Validate that each cost points to a node present in submitted traversals
    all_node_ids = {n.id for t in traversals for n in t.nodes}
    bad = [c for c in pathCosts if c.node_id not in all_node_ids]
    if bad:
        raise HTTPException(
            status_code=400,
            detail=f"Found {len(bad)} cost(s) referencing unknown node_id(s). "
                   f"First few: {[c.node_id for c in bad[:5]]}"
        )

    return improved_logic(traversals, pathCosts)
