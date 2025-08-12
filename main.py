import random
import copy

from helpers import profile_call
from funcs import logic_as_is, improved_logic
from models import Traversal, Node, CostAtNode


######################################################################################################
paramSets = [
    (250, 150, 250),
    (500, 150, 250),
    (1000, 150, 250),
    (2000, 150, 250),
]
######################################################################################################

for traversalN, nodesPerTraversalN, pathCostsN in paramSets:
    print(f"Traversal Count: {traversalN}")

    # Generate Input Data
    Traversals = [
        Traversal(nodes=[Node(id=Node_id) for Node_id in range(nodesPerTraversalN)])
        for _ in range(traversalN)
    ]

    PathCosts = [
        CostAtNode(
            node_id=random.randint(0, nodesPerTraversalN), cost=random.randint(0, 9)
        )
        for _ in range(pathCostsN)
    ]

    # Execute and profile
    result_sets = {
        "improved": {"durations": [], "results": [], "func": improved_logic},
        "asIs": {"durations": [], "results": [], "func": logic_as_is},
    }

    for _ in range(5):
        for key, data in result_sets.items():
            outcome = profile_call(
                data["func"], [copy.deepcopy(Traversals), copy.deepcopy(PathCosts)]
            )
            data["results"].append(outcome[0])
            data["durations"].append(outcome[1])

    # Report outcome
    for key, data in result_sets.items():
        durations = data["durations"]
        avg_duration = sum(durations) / len(durations)
        print(f"\t Mean (ms)[{key.rjust(8)}]: {avg_duration:.2f} ms [{durations}]")

    if result_sets["asIs"]["results"] != result_sets["improved"]["results"]:
        print("\t(!) Algorithms don't return the same output (!)")

    print("")
