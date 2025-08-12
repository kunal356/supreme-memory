from models import Traversal, CostAtNode


def logic_as_is(
    traversals: list[Traversal], pathCosts: list[CostAtNode]
) -> list[Traversal]:
    for traversal in traversals:
        for node in traversal.nodes:
            node.costs = []

        for cost in pathCosts:
            for node in traversal.nodes:
                if node.id == cost.node_id:
                    node.costs.append(cost)

        for node in traversal.nodes:
            if node.costs:
                for cost in node.costs:
                    traversal.total_cost += cost.cost

    return traversals


def improved_logic(
    traversals: list[Traversal], pathCosts: list[CostAtNode]
) -> list[Traversal]:
    # TODO: Implement revised logic
    return traversals
