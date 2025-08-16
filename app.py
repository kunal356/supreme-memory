"""FastAPI service exposing the traversal cost computation."""
from typing import List
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from models import Traversal, Node, CostAtNode
from funcs import improved_logic

logger = logging.getLogger("trackbase.app")
if not logger.handlers:
    # Keep basic config minimal; let hosting env override as needed.
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(title="Traversal Cost API", version="1.0.0")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("HTTP %s %s", request.method, request.url.path)
    try:
        response = await call_next(request)
        logger.info("HTTP %s %s -> %s", request.method,
                    request.url.path, response.status_code)
        return response
    except Exception as e:
        logger.exception("Unhandled error processing %s %s",
                         request.method, request.url.path)
        raise e


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exception: RequestValidationError):
    logger.warning("Request validation error at %s: %s",
                   request.url.path, exception)
    return JSONResponse(status_code=442, content={"detail": exception.errors()})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exception: Exception):
    logger.exception("Unhandled exception at %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/compute", response_model=List[Traversal])
def compute(traversals: List[Traversal], pathCosts: List[CostAtNode]):
    """Compute total_cost per traversal; validates cost.node_id membership."""

    logger.info("Compute called with %d traversal(s) and %d cost(s)",
                len(traversals or []), len(pathCosts or []))

    # Validate that each cost points to a node present in submitted traversals
    all_node_ids = {n.id for t in traversals for n in t.nodes}
    bad = [c for c in pathCosts if c.node_id not in all_node_ids]
    if bad:
        sample = [c.node_id for c in bad[:5]]
        logger.warning(
            "Unkown node_id(s) in payload: %s (showing up to 5)", sample)
        raise HTTPException(
            status_code=400,
            detail=f"Found {len(bad)} cost(s) referencing unknown node_id(s). "
            f"First few: {[c.node_id for c in bad[:5]]}"
        )

    try:
        result = improved_logic(traversals, pathCosts)
        logger.info("Compute completed successfully")
        return result
    except HTTPException:
        raise
    except Exception as exception:
        logger.exception("Failure during computation")
        raise HTTPException(
            status_code=500, detail="Failure during Computation") from exception
