import random
from copy import deepcopy
from funcs import logic_as_is, improved_logic
from models import Traversal, Node, CostAtNode


def gen_case(seed=123, traversalsN=5, nodesPerTraversalN=7, pathCostsN=25):
    rnd = random.Random(seed)
    traversals = [Traversal(nodes=[Node(id=i) for i in range(nodesPerTraversalN)])
                  for _ in range(traversalsN)]
    costs = [CostAtNode(node_id=rnd.randint(0, nodesPerTraversalN - 1),
                        cost=rnd.randint(1, 10)) for _ in range(pathCostsN)]
    return traversals, costs


def test_improved_matches_as_is_on_random():
    for seed in range(10):
        trs, costs = gen_case(seed=seed)
        a = deepcopy(trs)
        b = deepcopy(trs)
        outA = logic_as_is(a, costs)
        outB = improved_logic(b, costs)
        assert [t.total_cost for t in outA] == [t.total_cost for t in outB]


def test_edge_empty_inputs():
    assert improved_logic([], []) == []
    t = [Traversal(nodes=[])]
    out = improved_logic(t, [])
    assert out[0].total_cost == 0
